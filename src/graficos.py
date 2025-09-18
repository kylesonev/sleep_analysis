import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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


def criar_scatterplot_outliers(outliers: list, dataframe: pd.DataFrame):
    for outlier in outliers:
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

        print(f"\nAnálise de Outliers - {outlier}")
        print(f"• Primeiro Quartil (Q1): {Q1:.2f}")
        print(f"• Terceiro Quartil (Q3): {Q3:.2f}")
        print(f"• IQR: {IQR:.2f}")
        print(f"• Limite Inferior: {limite_inferior:.2f}")
        print(f"• Limite Superior: {limite_superior:.2f}")
        print(f"• Outliers Detected: {len(outliers_df)}")

        plt.figure(figsize=(12, 6))

        media = dataframe[outlier].mean()

        sns.scatterplot(
            x=non_outliers_df.index,
            y=non_outliers_df[outlier],
            color="skyblue",
            label="Normal",
            s=80,
        )
        sns.scatterplot(
            x=outliers_df.index,
            y=outliers_df[outlier],
            color="red",
            label="Outliers",
            s=100,
        )
        plt.axhline(limite_superior, color="red", linestyle="--")
        plt.axhline(limite_inferior, color="red", linestyle="--")
        plt.axhline(media, color="green", linestyle="--")

        plt.title(f"Distribuição de {outlier.capitalize()} com Outliers em destaque")
        plt.xlabel("Index")
        plt.ylabel(outlier)
        plt.legend()
        plt.tight_layout()
        plt.show()


def criar_barplot_stacked(
    dataframe: pd.DataFrame, composicao_sono: list, colormap: str = "viridis"
):
    volume = dataframe.groupby("data")[composicao_sono].sum()

    ax = volume.plot(
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


def imprimir_medias(dataframe: pd.DataFrame):
    print("Média das Maiores 15 Pontuações registradas")
    print("-------------------------------------------")
    print(f"Pontuação: {dataframe['pontuacao']}")
    print(f"Duração: {dataframe['duracao']}")
    print(f"Sono Leve %: {dataframe['sono_leve_perc']}")
    print(f"Sono Profundo %: {dataframe['sono_profundo_perc']}")
    print(f"REM %: {dataframe['REM_perc']}")
    print(f"Tempo acordado: {dataframe['tempo_acordado']}")
    print(f"Vezes acordado: {dataframe['vezes_acordado']}")


def imprimir_diferenca_medias(
    media_maiores_df: pd.DataFrame, media_menores_df: pd.DataFrame
):
    print("Diferença entre as Maiores e Menores")
    print("--------------------------------")
    print(
        f"Pontuação: {media_maiores_df['pontuacao'] - media_menores_df['pontuacao']:.2f}"
    )
    print(f"Duração: {media_maiores_df['duracao'] - media_menores_df['duracao']:.2f}")
    print(
        f"Sono Leve (%): {media_maiores_df['sono_leve_perc'] - media_menores_df['sono_leve_perc']:.2f}"
    )
    print(
        f"Sono Profundo (%): {media_maiores_df['sono_profundo_perc'] - media_menores_df['sono_profundo_perc']:.2f}"
    )
    print(f"REM (%): {media_maiores_df['REM_perc'] - media_menores_df['REM_perc']:.2f}")
    print(
        f"Tempo acordado: {media_maiores_df['tempo_acordado'] - media_menores_df['tempo_acordado']:.2f}"
    )
    print(
        f"Vezes acordado: {media_maiores_df['vezes_acordado'] - media_menores_df['vezes_acordado']:.2f}"
    )
    print("--------------------------------")


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
