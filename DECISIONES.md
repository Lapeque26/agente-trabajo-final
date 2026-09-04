Decisiones
Iteración 1 — Primera corrida real
Fecha: 03/09/2026

Corrida afectada: corridas/corrida_01/

Qué falló
La hoja Stock usa “Consumo promedio Mensual”, mientras que la hoja Instrucciones lo describe como “Consumo promedio diario”. Esta inconsistencia puede generar una interpretación incorrecta de la unidad de consumo, aunque en esta corrida el agente respetó las fechas y los cálculos ya existentes de la planilla.

Qué se decidió
Mantener como correcta la unidad mensual y corregir la hoja Instrucciones para que también diga “Consumo promedio mensual”.

Qué se cambió
En esta iteración se documentó el hallazgo y la decisión. No se cambiaron fórmulas, valores de stock ni prompts.

Por qué
Para eliminar la ambigüedad en la fuente de datos antes de ejecutar una segunda corrida.

Iteración 2 — Validación de la corrección
Fecha: 03/09/2026

Corrida afectada: corridas/corrida_02/

Qué se verificó
Que la corrección de la unidad de consumo eliminó la ambigüedad detectada en la corrida 1.

Resultado
La corrida 2 analizó 34 productos y no volvió a reportar la inconsistencia entre consumo diario y mensual.

Qué se decidió
Mantener la corrección y continuar con el mismo criterio de consumo promedio mensual.

Qué se cambió
No se modificaron prompts ni fórmulas en esta iteración; solo se validó el efecto de la corrección realizada en la fuente de datos.

Por qué
Para confirmar que la mejora resolvió el problema antes de realizar la tercera corrida.

Iteración 3 — Definición del horizonte de priorización
Fecha: 03/09/2026

Corrida afectada: corridas/corrida_02/

Qué falló
En la corrida 2 apareció un criterio de 7 días que no estaba definido en el prompt. Esto se consideró una decisión no autorizada del agente.

Qué se decidió
Definir explícitamente un horizonte de 20 días para determinar la prioridad de los productos y reemplazar cualquier horizonte implícito.

Qué se cambió
Se incorporó al system prompt el criterio de prioridad alta, media y baja basado en la fecha sugerida del próximo pedido y en el horizonte explícito de 20 días.

Por qué
Para evitar criterios inventados por el agente y hacer que la priorización sea reproducible.
