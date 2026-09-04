# Análisis económico

## Alcance y metodología

Las corridas de desarrollo se realizaron con GPT-5.6 Sol. Codex no expuso metadatos exactos de consumo de tokens; por lo tanto, las cifras son **estimaciones reproducibles**, no registros de facturación ni una factura real de Codex.

La estimación toma como base el contenido conservado de los prompts, los datos procesados y la salida de cada corrida. El costo se obtiene aplicando a los tokens estimados las tarifas API documentadas.

Precios API documentados para GPT-5.6 Sol:

- entrada: USD 4 por millón de tokens;
- salida: USD 20 por millón de tokens.

**Fecha de consulta de precios:** 03/09/2026.

**Fuente oficial:** [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol).

## Tokens y costo por corrida

Las fórmulas aplicadas son:

```text
Costo entrada = (tokens entrada / 1.000.000) × tarifa entrada
Costo salida = (tokens salida / 1.000.000) × tarifa salida
Costo total = costo entrada + costo salida
```

| Corrida | Tokens de entrada | Tokens de salida | Tarifa entrada USD / 1M tokens | Tarifa salida USD / 1M tokens | Costo entrada USD | Costo salida USD | Costo total estimado USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| corrida_01 | 1.800 estimados | 125 estimados | 4 | 20 | 0,0072 | 0,0025 | 0,0097 |
| corrida_02 | 1.800 estimados | 126 estimados | 4 | 20 | 0,0072 | 0,00252 | 0,00972 |
| corrida_03 | 1.950 estimados | 294 estimados | 4 | 20 | 0,0078 | 0,00588 | 0,01368 |

### Naturaleza de la evidencia

- Los conteos de tokens son estimaciones documentadas y no metadata real de facturación.
- Codex no expuso el `usage` real de cada ejecución.
- Por esa razón, el análisis no presenta estos valores como consumo facturado real.
- El costo sí es reproducible matemáticamente a partir de los tokens estimados y las tarifas declaradas.
- Si en una implementación productiva se dispone de metadata de `usage` de la API, estos valores estimados deberían reemplazarse por los tokens reales de cada corrida.

El detalle de los cálculos es:

- **corrida_01:** costo de entrada = 1.800 / 1.000.000 × 4 = USD 0,0072; costo de salida = 125 / 1.000.000 × 20 = USD 0,0025; costo total estimado = USD 0,0097.
- **corrida_02:** costo de entrada = 1.800 / 1.000.000 × 4 = USD 0,0072; costo de salida = 126 / 1.000.000 × 20 = USD 0,00252; costo total estimado = USD 0,00972.
- **corrida_03:** costo de entrada = 1.950 / 1.000.000 × 4 = USD 0,0078; costo de salida = 294 / 1.000.000 × 20 = USD 0,00588; costo total estimado = USD 0,01368.

El promedio estimado por corrida es aproximadamente **USD 0,01103**.

## Proyección operativa

La hipótesis operativa es **1 corrida por semana**:

- costo semanal aproximado con GPT-5.6 Sol: USD 0,01103;
- costo anual aproximado para 52 corridas: USD 0,5737.

## Elección del modelo

Las corridas se realizaron con GPT-5.6 Sol. Para producción se propone probar GPT-5.6 Luna, dado que la tarea consiste en leer una tabla, aplicar reglas explícitas, clasificar productos y generar una salida estructurada.

Precios API documentados para GPT-5.6 Luna:

- entrada: USD 0,20 por millón de tokens;
- salida: USD 1,20 por millón de tokens.

Con las mismas estimaciones de tokens y una corrida semanal:

- costo promedio estimado con Luna: USD 0,0006 por corrida;
- costo semanal estimado: USD 0,0006;
- costo anual aproximado: USD 0,03.

Luna debe validarse con los mismos casos antes de reemplazar a Sol. Si la calidad disminuye, debe mantenerse un modelo superior.

**Fuente oficial general:** [modelos y precios de OpenAI](https://developers.openai.com/api/docs/models/gpt).
