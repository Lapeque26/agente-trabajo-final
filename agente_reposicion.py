#!/usr/bin/env python3
"""Agente ejecutable de planificación de reposición de stock."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile, ZipInfo


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "p": PACKAGE_REL_NS}
REPO_ROOT = Path(__file__).resolve().parent
RUTA_AUTORIZADA = Path("datos") / "stock_reposicion.xlsx"
MAX_TAMAÑO_ARCHIVO = 5 * 1024 * 1024
MAX_MIEMBROS_ZIP = 100
MAX_TAMAÑO_MIEMBRO = 2 * 1024 * 1024
MAX_TAMAÑO_TOTAL = 10 * 1024 * 1024
MAX_TAMAÑO_XML = 2 * 1024 * 1024
REQUIRED_COLUMNS = {
    "Producto",
    "Stock actual",
    "Stock en tránsito",
    "Consumo promedio Mensual",
    "Stock de seguridad",
    "Fecha estimada de quiebre",
    "Fecha límite sugerida de pedido - 90 dias antes",
}


@dataclass(frozen=True)
class Producto:
    nombre: str
    stock_actual: float
    stock_transito: float
    consumo_mensual: float
    stock_seguridad: float
    fecha_stock_limite: date
    fecha_proximo_pedido: date
    prioridad: str

    @property
    def cobertura_total(self) -> float:
        """Cobertura física; el stock de seguridad no se descuenta."""
        return self.stock_actual + self.stock_transito


@dataclass(frozen=True)
class Resultado:
    productos_analizados: int
    productos: tuple[Producto, ...]
    anomalías: tuple[str, ...]

    @property
    def productos_con_atencion(self) -> tuple[Producto, ...]:
        return tuple(p for p in self.productos if p.prioridad in {"Alta", "Media"})


def clasificar_prioridad(fecha_pedido: date, fecha_corrida: date) -> str:
    """Clasifica con el horizonte de 20 días definido por el proyecto."""
    if fecha_pedido <= fecha_corrida:
        return "Alta"
    if fecha_pedido <= fecha_corrida + timedelta(days=20):
        return "Media"
    return "Baja"


def _columna(referencia: str) -> str:
    coincidencia = re.match(r"[A-Z]+", referencia)
    if not coincidencia:
        raise ValueError(f"Referencia de celda inválida: {referencia}")
    return coincidencia.group(0)


def validar_ruta_entrada(ruta: Path) -> Path:
    """Acepta únicamente el XLSX autorizado dentro de la raíz del repositorio."""
    if ruta.is_absolute():
        raise ValueError("La ruta del archivo no puede ser absoluta")
    if ".." in ruta.parts:
        raise ValueError("La ruta del archivo no puede contener '..'")
    if ruta.parts != RUTA_AUTORIZADA.parts:
        raise ValueError(f"El único archivo autorizado es {RUTA_AUTORIZADA.as_posix()}")

    ruta_sin_resolver = REPO_ROOT / ruta
    try:
        ruta_resuelta = ruta_sin_resolver.resolve(strict=True)
    except OSError as error:
        raise ValueError(f"No se pudo resolver el archivo autorizado: {error}") from error
    if not ruta_resuelta.is_relative_to(REPO_ROOT):
        raise ValueError("La ruta resuelta queda fuera de la raíz del repositorio")
    if any(
        componente.is_symlink()
        for componente in (REPO_ROOT / "datos", ruta_sin_resolver)
    ):
        raise ValueError("No se permiten enlaces simbólicos en la ruta del archivo")
    if ruta_resuelta != ruta_sin_resolver:
        raise ValueError("La ruta autorizada no puede redirigir a otro archivo")
    if not ruta_resuelta.is_file():
        raise ValueError("El archivo autorizado no es un archivo regular")
    if ruta_resuelta.stat().st_size > MAX_TAMAÑO_ARCHIVO:
        raise ValueError("El archivo Excel supera el límite de 5 MB")
    return ruta_resuelta


def validar_miembros_zip(miembros: Sequence[ZipInfo]) -> None:
    """Valida metadatos ZIP sin extraer ni leer el contenido de los miembros."""
    if len(miembros) > MAX_MIEMBROS_ZIP:
        raise ValueError(
            f"El Excel supera el máximo de {MAX_MIEMBROS_ZIP} miembros ZIP"
        )
    nombres: set[str] = set()
    tamaño_total = 0
    for miembro in miembros:
        nombre = miembro.filename
        ruta = PurePosixPath(nombre)
        if (
            not nombre
            or nombre.startswith(("/", "\\"))
            or "\\" in nombre
            or re.match(r"^[A-Za-z]:", nombre)
            or ".." in ruta.parts
        ):
            raise ValueError(f"Miembro ZIP con ruta sospechosa: {nombre!r}")
        if nombre in nombres:
            raise ValueError(f"Miembro ZIP duplicado: {nombre!r}")
        nombres.add(nombre)
        if miembro.file_size > MAX_TAMAÑO_MIEMBRO:
            raise ValueError(
                f"El miembro ZIP {nombre!r} supera el límite de 2 MB"
            )
        tamaño_total += miembro.file_size
        if tamaño_total > MAX_TAMAÑO_TOTAL:
            raise ValueError("El contenido descomprimido supera el límite total de 10 MB")


def _leer_xml(archivo: ZipFile, ruta: str) -> ET.Element:
    """Lee un XML necesario, con tamaño limitado y sin resolver entidades externas."""
    try:
        miembro = archivo.getinfo(ruta)
    except KeyError as error:
        raise ValueError(f"Falta el componente requerido del Excel: {ruta}") from error
    if miembro.file_size > MAX_TAMAÑO_XML:
        raise ValueError(f"El XML {ruta!r} supera el límite de 2 MB")
    contenido = archivo.read(miembro)
    if len(contenido) > MAX_TAMAÑO_XML:
        raise ValueError(f"El XML {ruta!r} supera el límite de 2 MB")
    mayúsculas = contenido.upper()
    if b"<!DOCTYPE" in mayúsculas or b"<!ENTITY" in mayúsculas:
        raise ValueError(f"El XML {ruta!r} contiene declaraciones no permitidas")
    try:
        return ET.fromstring(contenido)
    except ET.ParseError as error:
        raise ValueError(f"El XML {ruta!r} no es válido: {error}") from error


def _textos_compartidos(archivo: ZipFile) -> list[str]:
    ruta = "xl/sharedStrings.xml"
    if ruta not in archivo.namelist():
        return []
    raíz = _leer_xml(archivo, ruta)
    return [
        "".join(nodo.text or "" for nodo in item.findall(".//m:t", NS))
        for item in raíz.findall("m:si", NS)
    ]


def _ruta_hoja(archivo: ZipFile, nombre: str) -> str:
    libro = _leer_xml(archivo, "xl/workbook.xml")
    relaciones = _leer_xml(archivo, "xl/_rels/workbook.xml.rels")
    destinos = {
        relación.attrib["Id"]: relación.attrib["Target"]
        for relación in relaciones.findall("p:Relationship", NS)
    }
    for hoja in libro.findall("m:sheets/m:sheet", NS):
        if hoja.attrib.get("name") == nombre:
            destino = destinos[hoja.attrib[f"{{{REL_NS}}}id"]].lstrip("/")
            return destino if destino.startswith("xl/") else f"xl/{destino}"
    raise ValueError(f"No se encontró la hoja {nombre!r}")


def _valor_celda(celda: ET.Element, compartidos: list[str]) -> object | None:
    tipo = celda.attrib.get("t")
    valor = celda.find("m:v", NS)
    if tipo == "inlineStr":
        return "".join(n.text or "" for n in celda.findall(".//m:t", NS))
    if valor is None or valor.text is None or valor.text == "":
        return None
    if tipo == "s":
        return compartidos[int(valor.text)]
    if tipo in {"str", "e"}:
        return valor.text
    try:
        return float(valor.text)
    except ValueError:
        return valor.text


def _filas_stock(ruta: Path) -> list[dict[str, object | None]]:
    try:
        with ZipFile(ruta) as archivo:
            validar_miembros_zip(archivo.infolist())
            compartidos = _textos_compartidos(archivo)
            hoja = _leer_xml(archivo, _ruta_hoja(archivo, "Stock"))
    except BadZipFile as error:
        raise ValueError(f"No se pudo leer el archivo Excel: {error}") from error

    filas: list[dict[str, object | None]] = []
    encabezados: dict[str, str] | None = None
    for fila in hoja.findall(".//m:sheetData/m:row", NS):
        por_columna = {
            _columna(celda.attrib["r"]): _valor_celda(celda, compartidos)
            for celda in fila.findall("m:c", NS)
        }
        if encabezados is None:
            candidatos = {str(valor) for valor in por_columna.values() if valor is not None}
            if "Producto" in candidatos:
                encabezados = {
                    columna: str(valor)
                    for columna, valor in por_columna.items()
                    if valor is not None
                }
                faltantes = REQUIRED_COLUMNS - set(encabezados.values())
                if faltantes:
                    raise ValueError(
                        "Faltan columnas requeridas: " + ", ".join(sorted(faltantes))
                    )
            continue
        registro = {
            encabezado: por_columna.get(columna)
            for columna, encabezado in encabezados.items()
        }
        if registro.get("Producto") not in {None, ""}:
            filas.append(registro)
    if encabezados is None:
        raise ValueError("No se encontró la fila de encabezados de la hoja Stock")
    return filas


def _fecha_excel(valor: object, campo: str, producto: str) -> date:
    if isinstance(valor, (int, float)):
        return (datetime(1899, 12, 30) + timedelta(days=float(valor))).date()
    if isinstance(valor, str):
        for formato in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                pass
    raise ValueError(f"{producto}: {campo} no contiene una fecha válida")


def _número(valor: object, campo: str, producto: str) -> float:
    if isinstance(valor, (int, float)):
        return float(valor)
    raise ValueError(f"{producto}: falta {campo} o no es numérico")


def analizar_registros(
    registros: Iterable[dict[str, object | None]], fecha_corrida: date
) -> Resultado:
    productos: list[Producto] = []
    anomalías: list[str] = []
    analizados = 0
    for registro in registros:
        analizados += 1
        nombre = str(registro.get("Producto") or f"fila {analizados}")
        try:
            fecha_pedido = _fecha_excel(
                registro.get("Fecha límite sugerida de pedido - 90 dias antes"),
                "fecha sugerida del próximo pedido",
                nombre,
            )
            producto = Producto(
                nombre=nombre,
                stock_actual=_número(registro.get("Stock actual"), "stock actual", nombre),
                stock_transito=_número(
                    registro.get("Stock en tránsito"), "stock en tránsito", nombre
                ),
                consumo_mensual=_número(
                    registro.get("Consumo promedio Mensual"),
                    "consumo promedio mensual",
                    nombre,
                ),
                stock_seguridad=_número(
                    registro.get("Stock de seguridad"), "stock de seguridad", nombre
                ),
                fecha_stock_limite=_fecha_excel(
                    registro.get("Fecha estimada de quiebre"),
                    "fecha estimada de stock límite",
                    nombre,
                ),
                fecha_proximo_pedido=fecha_pedido,
                prioridad=clasificar_prioridad(fecha_pedido, fecha_corrida),
            )
        except ValueError as error:
            anomalías.append(str(error))
            continue
        productos.append(producto)
    productos.sort(key=lambda p: (p.fecha_proximo_pedido, p.nombre))
    return Resultado(analizados, tuple(productos), tuple(anomalías))


def analizar_archivo(ruta: Path, fecha_corrida: date) -> Resultado:
    ruta_validada = validar_ruta_entrada(ruta)
    return analizar_registros(_filas_stock(ruta_validada), fecha_corrida)


def _cantidad(valor: float) -> str:
    return str(int(valor)) if valor.is_integer() else str(valor)


def generar_salida(resultado: Resultado, fecha_corrida: date) -> str:
    atención = resultado.productos_con_atencion
    líneas = [
        "### Resumen",
        "",
        f"- Productos analizados: {resultado.productos_analizados}",
        f"- Productos que requieren atención: {len(atención)}",
        (
            "- Criterio general: Prioridad alta para fechas sugeridas de pedido "
            f"vencidas o coincidentes con el {fecha_corrida.strftime('%d/%m/%Y')}; "
            "prioridad media para fechas dentro de los próximos 20 días; prioridad "
            "baja para fechas posteriores, sin atención inmediata."
        ),
        "",
        "### Productos que requieren atención",
        "",
        "| Prioridad | Producto | Cobertura considerada | Stock límite estimado | Próximo pedido sugerido | Motivo | Recomendación |",
        "|---|---|---|---|---|---|---|",
    ]
    for producto in atención:
        motivo = (
            "La fecha sugerida del pedido está vencida o coincide con la fecha de la corrida."
            if producto.prioridad == "Alta"
            else "La fecha sugerida del pedido cae dentro de los próximos 20 días."
        )
        cobertura = (
            f"{_cantidad(producto.stock_actual)} unidades actuales + "
            f"{_cantidad(producto.stock_transito)} en tránsito"
        )
        líneas.append(
            "| "
            + " | ".join(
                (
                    producto.prioridad,
                    producto.nombre.replace("|", "\\|"),
                    cobertura,
                    producto.fecha_stock_limite.strftime("%d/%m/%Y"),
                    producto.fecha_proximo_pedido.strftime("%d/%m/%Y"),
                    motivo,
                    "Revisar la planificación del próximo pedido. Sujeto a revisión humana.",
                )
            )
            + " |"
        )
    líneas.extend(
        [
            "",
            "### Datos faltantes o limitaciones",
            "",
            *(f"- {anomalía}" for anomalía in resultado.anomalías),
        ]
    )
    if not resultado.anomalías:
        líneas.append("- Sin datos faltantes relevantes.")
    líneas.extend(
        ["", "**Recomendaciones sujetas a revisión y aprobación humana.**"]
    )
    return "\n".join(líneas)


def _argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analiza una planilla de reposición sin modificarla."
    )
    parser.add_argument("--archivo", type=Path, required=True)
    parser.add_argument(
        "--fecha",
        type=date.fromisoformat,
        required=True,
        help="Fecha de corrida en formato AAAA-MM-DD",
    )
    return parser.parse_args()


def main() -> int:
    argumentos = _argumentos()
    try:
        resultado = analizar_archivo(argumentos.archivo, argumentos.fecha)
    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error
    print(generar_salida(resultado, argumentos.fecha))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
