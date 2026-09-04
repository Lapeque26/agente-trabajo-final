# Decisiones e iteraciones

## Tres decisiones significativas del desarrollo

| Decisión | Problema / contexto | Cambio realizado | Motivo / impacto | Evidencia |
| --- | --- | --- | --- | --- |
| Unidad de consumo | La hoja Stock indicaba consumo promedio mensual y la hoja Instrucciones lo describía como consumo promedio diario. | Se unificó la interpretación a consumo promedio mensual y se corrigió la descripción correspondiente. | Evitar que el agente interpretara incorrectamente la unidad de consumo. | corrida_01 detectó la inconsistencia y corrida_02 confirmó que ya no aparecía. |
| Horizonte de priorización | corrida_02 utilizó un horizonte de 7 días que no estaba autorizado por el prompt. | Se definió explícitamente prioridad Alta, Media y Baja con horizonte de 20 días. | Evitar criterios temporales inventados y hacer reproducible la priorización. | corrida_02 utilizó 7 días y corrida_03 aplicó correctamente 20 días. |
| Stock de seguridad | La documentación podía interpretarse como si el stock de seguridad debiera descontarse de la cobertura. | Se definió que la cobertura es stock actual + stock en tránsito y que el stock de seguridad se usa únicamente como referencia de control. | Alinear la documentación con la lógica real del agente y evitar una interpretación incorrecta de la cobertura. | agente_reposicion.py, tests/test_agente_reposicion.py y docs/validacion_ejecutable.md. |

## Iteración 1 — Ambigüedad en la unidad de consumo

Fecha: 03/09/2026

### Problema / contexto

La hoja **`Stock`** indicaba “Consumo promedio Mensual” mientras que la hoja **`Instrucciones`** lo describía como “Consumo promedio diario”.

### Cambio realizado

Se mantuvo como correcta la unidad mensual y se corrigió la descripción de la hoja **`Instrucciones`** para que también indique consumo promedio mensual.

### Motivo / impacto

Eliminar una ambigüedad que podía llevar al agente a interpretar incorrectamente la unidad de consumo.

### Evidencia

- **`corrida_01`** detectó la inconsistencia.
- **`corrida_02`** ya no volvió a reportarla.

## Iteración 2 — Validación de la corrección

Fecha: 03/09/2026

### Problema / contexto

Era necesario comprobar que la corrección anterior realmente eliminara la ambigüedad.

### Cambio realizado

No se modificaron prompts ni fórmulas. Se realizó una segunda ejecución usando la fuente corregida.

### Motivo / impacto

Confirmar que el problema había sido resuelto antes de continuar iterando.

### Evidencia

- **`corrida_02`** analizó 34 productos.
- No volvió a reportar la inconsistencia entre consumo diario y mensual.

## Iteración 3 — Horizonte temporal no autorizado

Fecha: 03/09/2026

### Problema / contexto

La **`corrida_02`** utilizó un criterio de 7 días que no estaba definido en el prompt.

### Cambio realizado

Se incorporó al system prompt un criterio explícito:

- Alta: fecha vencida o igual a la fecha de corrida.
- Media: dentro de los próximos 20 días.
- Baja: más de 20 días.

### Motivo / impacto

Evitar que el agente invente criterios temporales y hacer reproducible la priorización.

### Evidencia

- **`corrida_02`** utilizó 7 días sin autorización.
- **`corrida_03`** aplicó el horizonte explícito de 20 días.
- **`corrida_03`** identificó **`D900`**, **`H950`** y **`K950`** como prioridad Media.

## Iteración 4 — Regla de stock de seguridad

Fecha: 03/09/2026

### Problema / contexto

La documentación podía interpretarse como si el stock de seguridad debiera descontarse de la cobertura total.

### Cambio realizado

Se definió que la cobertura utilizada por el agente es:

**`stock actual + stock en tránsito`**.

El stock de seguridad se conserva como referencia de control y no se descuenta de la cobertura total.

### Motivo / impacto

Alinear la lógica del agente con la regla de negocio utilizada en las corridas.

### Evidencia

- **`agente_reposicion.py`** calcula la cobertura como stock actual + stock en tránsito.
- **`tests/test_agente_reposicion.py`** incluye una prueba específica que verifica que el stock de seguridad no se descuenta.
- **`docs/validacion_ejecutable.md`** documenta el mismo criterio.

Esta iteración documenta la decisión; no afirma que los prompts o **`README.md`** hayan sido actualizados con esta aclaración.

## Iteración 5 — Feedback del evaluador automático

Fecha: 03/09/2026

### Problema / contexto

El evaluador automático otorgó inicialmente 17,5/100 y señaló deficiencias en funcionamiento demostrable, proceso, reproducibilidad, análisis económico y gobierno/riesgo.

### Cambio realizado

Se incorporaron los siguientes archivos y mejoras que existen en el repositorio:

- implementación ejecutable en **`agente_reposicion.py`**;
- pruebas automáticas en **`tests/test_agente_reposicion.py`**;
- declaración de requisitos en **`requirements.txt`**;
- validación ejecutable en **`docs/validacion_ejecutable.md`**;
- análisis económico en **`docs/analisis_economico.md`**;
- gobierno y riesgos en **`docs/gobierno_riesgo.md`**;
- archivos **`metadata.json`** en **`corridas/corrida_01/`**, **`corridas/corrida_02/`** y **`corridas/corrida_03/`**;
- mejora del índice de corridas en **`corridas/README.md`**.

### Motivo / impacto

Responder directamente al feedback y aumentar funcionamiento verificable, trazabilidad, reproducibilidad, análisis económico y gobernanza.

### Evidencia

- **`agente_reposicion.py`**
- **`tests/test_agente_reposicion.py`**
- **`requirements.txt`**
- **`docs/validacion_ejecutable.md`**
- **`docs/analisis_economico.md`**
- **`docs/gobierno_riesgo.md`**
- **`corridas/corrida_01/metadata.json`**
- **`corridas/corrida_02/metadata.json`**
- **`corridas/corrida_03/metadata.json`**
- **`corridas/README.md`**

## Principio de trabajo

El proyecto conserva los errores reales, documenta las iteraciones y no reescribe las salidas históricas para ocultar fallas. De este modo, prioriza la trazabilidad y la reproducibilidad del proceso.
