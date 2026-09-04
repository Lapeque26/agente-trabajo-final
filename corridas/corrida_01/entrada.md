# Entrada de la corrida 01

- **Fecha de la corrida:** 03/09/2026
- **Archivo de datos utilizado:** `datos/stock_reposicion.xlsx`
- **Ruta del system prompt:** `prompts/system_prompt.md`
- **Ruta del user prompt:** `prompts/user_prompt.md`

## Instrucción de ejecución

Leé la planilla completa `datos/stock_reposicion.xlsx` e identificá los productos que requieren atención para reposición. Priorizá los casos según su urgencia usando las fechas y los cálculos ya existentes en la planilla. Considerá `stock actual + stock en tránsito` dentro de la cobertura y respetá el stock de seguridad como límite mínimo.

Señalá los datos faltantes, las inconsistencias y las posibles anomalías. Entregá la salida exactamente en el formato definido por `prompts/system_prompt.md`. No modifiques la planilla ni ejecutes ninguna acción.
