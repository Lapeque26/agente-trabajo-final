# Corridas reales

Cada carpeta conserva la entrada y la salida de una ejecución real. El archivo `metadata.json` identifica la fecha, la fuente de datos, los prompts, el modelo y el objetivo de cada corrida.

| Corrida | Fecha | Entrada | Salida | Datos | Objetivo |
|---|---|---|---|---|---|
| [corrida_01](corrida_01/metadata.json) | 2026-09-03 | [entrada.md](corrida_01/entrada.md) | [salida.md](corrida_01/salida.md) | [stock_reposicion.xlsx](../datos/stock_reposicion.xlsx) | Primera ejecución real para detectar problemas de interpretación y evaluar el comportamiento inicial. |
| [corrida_02](corrida_02/metadata.json) | 2026-09-03 | [entrada.md](corrida_02/entrada.md) | [salida.md](corrida_02/salida.md) | [stock_reposicion.xlsx](../datos/stock_reposicion.xlsx) | Validar la corrección de la inconsistencia entre consumo diario y mensual. |
| [corrida_03](corrida_03/metadata.json) | 2026-09-03 | [entrada.md](corrida_03/entrada.md) | [salida.md](corrida_03/salida.md) | [stock_reposicion.xlsx](../datos/stock_reposicion.xlsx) | Validar el criterio explícito de prioridad con horizonte de 20 días. |

Las salidas históricas se preservan sin reescritura. Las diferencias entre corridas están documentadas en [`DECISIONES.md`](../DECISIONES.md).
