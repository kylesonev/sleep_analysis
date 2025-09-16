import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def criar_boxplot(
    dataframe: pd.DataFrame,
    metricas: list,
    nrows: int = None,
    ncols: int = 4,
    figsize: tuple = (15, 10),
    color: str = "skyblue",
) -> tuple:
    # Validação
    for metrica in metricas:
        if metrica not in dataframe.columns:
            raise ValueError(f"A coluna {metrica} não existe no DataFrame")
        if not pd.api.types.is_numeric_dtype(dataframe[metrica]):
            raise ValueError(f"A coluna {metrica} não é numérica")

    # Calcular número de linhas se não especificado
    if nrows is None:
        nrows = math.ceil(len(metricas) / ncols)
    if len(metricas) > nrows * ncols:
        raise ValueError(
            f"Número de métricas ({len(metricas)} excede o tamanho da grade ({nrows * ncols})"
        )

    # Criar figura
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten() if nrows * ncols > 1 else [axes]

    # Criar boxplots
    for i, metrica in enumerate(metricas):
        ax = axes[i]
        sns.boxplot(x=dataframe[metrica], ax=ax, color=color)
        ax.set_title(metrica)
        ax.set_xlabel("")

    # Remover eixos não usados
    for j in range(len(metricas), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
    return fig, axes
