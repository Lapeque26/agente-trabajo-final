import hashlib
import sys
import unittest
from datetime import date
from pathlib import Path
from zipfile import ZipInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agente_reposicion import (
    MAX_MIEMBROS_ZIP,
    MAX_TAMAÑO_MIEMBRO,
    analizar_archivo,
    analizar_registros,
    clasificar_prioridad,
    validar_miembros_zip,
    validar_ruta_entrada,
)


ARCHIVO_REAL = ROOT / "datos" / "stock_reposicion.xlsx"
RUTA_AUTORIZADA = Path("datos/stock_reposicion.xlsx")
FECHA_CORRIDA = date(2026, 9, 3)


def registro_base(**cambios):
    registro = {
        "Producto": "PRUEBA",
        "Stock actual": 10,
        "Stock en tránsito": 5,
        "Consumo promedio Mensual": 3,
        "Stock de seguridad": 2,
        "Fecha estimada de quiebre": "2026-12-01",
        "Fecha límite sugerida de pedido - 90 dias antes": "2026-09-10",
    }
    registro.update(cambios)
    return registro


class ReglasDePrioridadTest(unittest.TestCase):
    def test_prioridad_alta_para_fecha_vencida_o_igual(self):
        self.assertEqual(clasificar_prioridad(date(2026, 9, 2), FECHA_CORRIDA), "Alta")
        self.assertEqual(clasificar_prioridad(FECHA_CORRIDA, FECHA_CORRIDA), "Alta")

    def test_prioridad_media_hasta_20_dias_inclusive(self):
        self.assertEqual(clasificar_prioridad(date(2026, 9, 4), FECHA_CORRIDA), "Media")
        self.assertEqual(clasificar_prioridad(date(2026, 9, 23), FECHA_CORRIDA), "Media")

    def test_prioridad_baja_despues_de_20_dias(self):
        self.assertEqual(clasificar_prioridad(date(2026, 9, 24), FECHA_CORRIDA), "Baja")


class DatosTest(unittest.TestCase):
    def test_stock_de_seguridad_no_se_descuenta_de_la_cobertura(self):
        resultado = analizar_registros([registro_base()], FECHA_CORRIDA)
        self.assertEqual(resultado.productos[0].cobertura_total, 15)

    def test_dato_faltante_se_reporta_sin_inventarlo(self):
        resultado = analizar_registros(
            [registro_base(**{"Stock en tránsito": None})], FECHA_CORRIDA
        )
        self.assertEqual(resultado.productos_analizados, 1)
        self.assertEqual(resultado.productos, ())
        self.assertEqual(len(resultado.anomalías), 1)
        self.assertIn("stock en tránsito", resultado.anomalías[0])


class SeguridadTest(unittest.TestCase):
    def test_ruta_absoluta_es_rechazada(self):
        with self.assertRaisesRegex(ValueError, "no puede ser absoluta"):
            validar_ruta_entrada(ARCHIVO_REAL.resolve())

    def test_ruta_con_traversal_es_rechazada(self):
        with self.assertRaisesRegex(ValueError, "no puede contener"):
            validar_ruta_entrada(Path("datos/../datos/stock_reposicion.xlsx"))

    def test_archivo_distinto_es_rechazado(self):
        with self.assertRaisesRegex(ValueError, "único archivo autorizado"):
            validar_ruta_entrada(Path("datos/otro.xlsx"))

    def test_zip_con_demasiados_miembros_es_rechazado(self):
        miembros = [
            ZipInfo(f"miembro_{índice}.xml")
            for índice in range(MAX_MIEMBROS_ZIP + 1)
        ]
        with self.assertRaisesRegex(ValueError, "máximo"):
            validar_miembros_zip(miembros)

    def test_miembro_zip_demasiado_grande_es_rechazado(self):
        miembro = ZipInfo("xl/workbook.xml")
        miembro.file_size = MAX_TAMAÑO_MIEMBRO + 1
        with self.assertRaisesRegex(ValueError, "límite de 2 MB"):
            validar_miembros_zip([miembro])


class ExcelRealTest(unittest.TestCase):
    def test_excel_real_y_productos_esperados_sin_modificar_archivo(self):
        hash_antes = hashlib.sha256(ARCHIVO_REAL.read_bytes()).hexdigest()
        resultado = analizar_archivo(RUTA_AUTORIZADA, FECHA_CORRIDA)
        hash_después = hashlib.sha256(ARCHIVO_REAL.read_bytes()).hexdigest()

        self.assertEqual(hash_antes, hash_después)
        self.assertEqual(resultado.productos_analizados, 34)
        self.assertEqual(len(resultado.productos), 34)
        self.assertEqual(resultado.anomalías, ())
        prioridades = {p.nombre: p.prioridad for p in resultado.productos}
        self.assertEqual(prioridades["D900"], "Media")
        self.assertEqual(prioridades["H950"], "Media")
        self.assertEqual(prioridades["K950"], "Media")
        self.assertEqual(
            {p.nombre for p in resultado.productos_con_atencion},
            {"D900", "H950", "K950"},
        )
        self.assertNotIn("Alta", prioridades.values())


if __name__ == "__main__":
    unittest.main()
