# Análisis económico

## Alcance y metodología

Las corridas de desarrollo se realizaron con GPT-5.6 Sol. Codex no expuso metadatos exactos de consumo de tokens; por lo tanto, las cifras son **estimaciones reproducibles**, no registros de facturación ni una factura real de Codex.

La estimación toma como base el contenido conservado de los prompts, los datos procesados y la salida de cada corrida. El costo se obtiene aplicando a los tokens estimados las tarifas API documentadas:

```text
costo = (tokens entrada / 1.000.000 × precio entrada) + (tokens salida / 1.000.000 × precio salida)
```

## Estimación por corrida

| Corrida | Tokens de entrada estimados | Tokens de salida estimados | Costo estimado con GPT-5.6 Sol |
|---|---:|---:|---:|
| corrida_01 | ~1.800 | ~125 | ~USD 0,0097 |
| corrida_02 | ~1.800 | ~126 | ~USD 0,0097 |
| corrida_03 | ~1.950 | ~294 | ~USD 0,0137 |
| Promedio | — | — | ~USD 0,011 por corrida |

Precios API documentados para GPT-5.6 Sol:

- entrada: USD 4 por millón de tokens;
- salida: USD 20 por millón de tokens.

**Fecha de consulta de precios:** 03/09/2026.

**Fuente oficial:** [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol).

## Proyección operativa

La hipótesis operativa es **1 corrida por semana**:

- costo semanal aproximado con GPT-5.6 Sol: USD 0,011;
- costo anual aproximado para 52 corridas: USD 0,57.

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
