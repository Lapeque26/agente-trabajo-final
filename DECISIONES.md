# Decisiones

## Iteración 1 — Primera corrida real

- **Fecha:** 03/09/2026
- **Corrida afectada:** `corridas/corrida_01/`

### Qué falló

La hoja `Stock` usa “Consumo promedio Mensual”, mientras que la hoja `Instrucciones` lo describe como “Consumo promedio diario”. Esta inconsistencia puede generar una interpretación incorrecta de la unidad de consumo, aunque en esta corrida el agente respetó las fechas y los cálculos ya existentes de la planilla.

### Qué se decidió

Mantener como correcta la unidad mensual y corregir la hoja `Instrucciones` para que también diga “Consumo promedio mensual”.

### Qué se cambió

En esta iteración se documentó el hallazgo y la decisión. No se cambiaron fórmulas, valores de stock ni prompts.

### Por qué

Para eliminar la ambigüedad en la fuente de datos antes de ejecutar una segunda corrida.


