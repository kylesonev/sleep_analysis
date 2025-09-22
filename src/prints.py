import pandas as pd


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
    print(
        f"Duração: {media_maiores_df['duracao'] - media_menores_df['duracao']:.2f}")
    print(
        f"Sono Leve (%): {media_maiores_df['sono_leve_perc'] - media_menores_df['sono_leve_perc']:.2f}"
    )
    print(
        f"Sono Profundo (%): {media_maiores_df['sono_profundo_perc'] - media_menores_df['sono_profundo_perc']:.2f}"
    )
    print(
        f"REM (%): {media_maiores_df['REM_perc'] - media_menores_df['REM_perc']:.2f}")
    print(
        f"Tempo acordado: {media_maiores_df['tempo_acordado'] - media_menores_df['tempo_acordado']:.2f}"
    )
    print(
        f"Vezes acordado: {media_maiores_df['vezes_acordado'] - media_menores_df['vezes_acordado']:.2f}"
    )
    print("--------------------------------")
