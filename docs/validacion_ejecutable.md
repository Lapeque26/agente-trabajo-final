# Validación de la implementación ejecutable

## Entorno

La validación se realiza íntegramente en el entorno aislado de Codex con la biblioteca estándar de Python. No requiere macros, ejecutables descargados, permisos de administrador ni cambios en el Excel original.

**Validado únicamente en el entorno aislado de Codex. No requiere ni autoriza ejecución en la PC local.**

## Controles de seguridad incorporados

- solo se acepta la ruta relativa exacta `datos/stock_reposicion.xlsx` dentro de la raíz del repositorio;
- se rechazan rutas absolutas, componentes `..`, archivos alternativos, enlaces simbólicos y resoluciones fuera del repositorio antes de leer el archivo;
- el XLSX se limita a 5 MB, 100 miembros ZIP, 2 MB descomprimidos por miembro y 10 MB descomprimidos en total;
- se rechazan miembros ZIP duplicados o con rutas absolutas, traversal, barras invertidas o prefijos de unidad;
- cada XML se limita a 2 MB antes de parsearse;
- la detección de `DOCTYPE` y `ENTITY` cubre las representaciones XML habituales del archivo validado, pero no constituye un parser de seguridad universal para archivos XLSX no confiables;
- no se extraen miembros al disco: solo se leen en memoria los XML necesarios;
- no se agregaron red, descargas, dependencias de terceros, subprocess, shell, código dinámico, variables de entorno ni escritura de archivos.

## Comandos

Pruebas automáticas:

```bash
python -m unittest discover -s tests -v
```

Ejecución real:

```bash
python agente_reposicion.py --archivo datos/stock_reposicion.xlsx --fecha 2026-09-03
```

## Resultado

Las pruebas finalizaron correctamente:

```text
Ran 11 tests in 0.020s

OK
```

La ejecución real finalizó correctamente y produjo este resumen:

```text
Productos analizados: 34
Productos que requieren atención: 3
Prioridad alta: 0
Prioridad media: 3 (D900, H950 y K950)
Datos faltantes o limitaciones: Sin datos faltantes relevantes.
```

El hash SHA-256 de `datos/stock_reposicion.xlsx` fue idéntico antes y después de las pruebas y de la ejecución:

```text
f909fef019f7fbe2215af79aa35b317e411ee9840f90b24b2f16d8c8b6b29779
```

## Pruebas cubiertas

- clasificación de prioridad alta, media y baja, incluidos los límites temporales;
- cobertura como stock actual más stock en tránsito, sin descontar el stock de seguridad;
- reporte de un dato faltante sin inventar un valor;
- lectura de los 34 productos del Excel real;
- clasificación Media para D900, H950 y K950 al 03/09/2026;
- verificación por hash de que el Excel no se modifica durante el análisis;
- rechazo de rutas absolutas, rutas con `..` y nombres de archivo no autorizados;
- rechazo de archivos ZIP con demasiados miembros o con un miembro demasiado grande;
- aceptación del Excel real después de aplicar todos los controles de seguridad.
