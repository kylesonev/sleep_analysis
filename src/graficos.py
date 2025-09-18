import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def validar_metricas(dataframe: pd.DataFrame, metricas: list):
    # Validação
    for metrica in metricas:
        if metrica not in dataframe.columns:
            raise ValueError(f"A coluna {metrica} não existe no DataFrame")
        if not pd.api.types.is_numeric_dtype(dataframe[metrica]):
            raise ValueError(f"A coluna {metrica} não é numérica")


def calcular_linhas(metricas: list, ncols: int, nrows=None):
    # Calcular número de linhas se não especificado
    if nrows is None:
        nrows = math.ceil(len(metricas) / ncols)
    if len(metricas) > nrows * ncols:
        raise ValueError(
            f"Número de métricas ({len(metricas)} excede o tamanho da grade ({nrows * ncols})"
        )


def criar_figura(nrows, ncols, figsize):
    # Criar figura
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten() if nrows * ncols > 1 else [axes]

    return fig, axes


def remover_axes_vazio(metricas, fig, axes):
    # Remover eixos não usados
    for j in range(len(metricas), len(axes)):
        fig.delaxes(axes[j])


def criar_boxplot(
    dataframe: pd.DataFrame,
    metricas: list,
    nrows: int = 3,
    ncols: int = 4,
    figsize: tuple = (15, 10),
    color: str = "skyblue",
) -> tuple:
    validar_metricas(dataframe, metricas)
    calcular_linhas(metricas, ncols, nrows)
    fig, axes = criar_figura(nrows, ncols, figsize)

    # Criar boxplots
    for i, metrica in enumerate(metricas):
        ax = axes[i]
        sns.boxplot(x=dataframe[metrica], ax=ax, color=color)
        ax.set_title(metrica)
        ax.set_xlabel("")

    remover_axes_vazio(metricas, fig, axes)
    plt.tight_layout()
    plt.show()


def criar_scatterplot_outliers(
    outliers: list,
    dataframe: pd.DataFrame,
    nrows: int = None,
    ncols: int = 4,
    figsize: tuple = (15, 10),
):
    validar_metricas(dataframe=dataframe, metricas=outliers)
    calcular_linhas(outliers, ncols, nrows)
    fig, axes = criar_figura(nrows, ncols, figsize)

    # Criar boxplots
    for i, outlier in enumerate(outliers):
        ax = axes[i]
        ax.set_title(f"{outlier.capitalize()}")

        Q1 = dataframe[outlier].quantile(0.25)
        Q3 = dataframe[outlier].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers_mask = (dataframe[outlier] < limite_inferior) | (
            dataframe[outlier] > limite_superior
        )
        outliers_df = dataframe[outliers_mask].copy()
        non_outliers_df = dataframe[~outliers_mask].copy()

        media = dataframe[outlier].mean()

        sns.scatterplot(
            x=non_outliers_df.index,
            y=non_outliers_df[outlier],
            color="skyblue",
            label="Normal",
            s=80,
            ax=ax,
        )
        sns.scatterplot(
            x=outliers_df.index,
            y=outliers_df[outlier],
            color="red",
            label="Outliers",
            s=100,
            ax=ax,
        )
        ax.axhline(limite_superior, color="red", linestyle="--")
        ax.axhline(limite_inferior, color="red", linestyle="--")
        ax.axhline(media, color="green", linestyle="--")

        ax.set_xlabel("Index")

    remover_axes_vazio(outliers, fig, axes)
    plt.tight_layout()
    plt.show()

    return fig, axes


def criar_barplot_stacked(
    dataframe: pd.DataFrame, composicao_sono: list, colormap: str = "viridis"
):
    volume = dataframe.groupby("data")[composicao_sono].sum()

    volume.plot(
        kind="bar",
        stacked=True,
        figsize=(20, 10),
        colormap=colormap,
    )
    plt.title("Composição do Sono")
    plt.xlabel("Dia")
    plt.ylabel("Tempo (min)")
    plt.legend(title="Etapas")

    plt.tight_layout()
    plt.show()


def criar_pieplot(dataframe: pd.DataFrame, values: list, labels: list):
    plt.figure(figsize=(16, 8))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.2f%%",
        startangle=90,
    )
    plt.title("Composição Total do Sono Registrado")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def criar_side_by_side(maior_pontuacao: pd.Series, menor_pontuacao: pd.Series):
    categorias = maior_pontuacao.index.tolist()
    maior_vals = maior_pontuacao.values
    menor_vals = menor_pontuacao.values

    x = np.arange(len(categorias))
    width = 0.35

    fig, ax = plt.subplots(figsize=(15, 8))
    bars1 = ax.bar(x - width / 2, maior_vals, width, label="Melhor", color="skyblue")
    bars2 = ax.bar(x + width / 2, menor_vals, width, label="Pior", color="lightcoral")

    ax.set_ylabel("Valores Médios")
    ax.set_title("Comparação de Métricas de Sono: Melhor dia vs. Pior dia")
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=45, ha="right")
    ax.legend()

    ax.bar_label(bars1, padding=3, fmt="%.2f")
    ax.bar_label(bars2, padding=3, fmt="%.2f")

    plt.tight_layout()
    plt.show()


def criar_histograma(
    dataframe: pd.DataFrame,
    metricas: list,
    nrows: int = None,
    ncols: int = 4,
    figsize: tuple = (15, 10),
):
    validar_metricas(dataframe, metricas)
    calcular_linhas(metricas, ncols, nrows)
    fig, axes = criar_figura(nrows, ncols, figsize)

    for i, metrica in enumerate(metricas):
        ax = axes[i]
        sns.histplot(data=dataframe, x=metrica, kde=True, ax=ax)

    remover_axes_vazio(metricas, fig, axes)

    plt.tight_layout()
    plt.show()
