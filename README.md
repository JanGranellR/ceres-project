# Penne Predictor

## Estructura
``` mermaid
graph TB;
    A[Dataset 1] --> E;
    B[Dataset 2] --> E;
    C[Dataset 3] --> E;
    D[Test] --> F;
    E[Dataset] --> F;
    F[Clasificador Binario] --> G;
    G[Output];
```