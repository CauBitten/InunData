import matplotlib.pyplot as plt  # type: ignore
import pandas as pd

def plot_monthly_city_rainfall(
    df,
    month_year: str,
    top_n: int = 10,
    *,
    figsize: tuple = (10, 5),
    cmap_name: str = "viridis",
    tick_labelsize: int = 8,
    rotation: int = 45
) -> plt.Figure:
    """
    Exibe o TOP-N de cidades com maior chuva acumulada em um mês específico.

    --------
    Parâmetros
    --------
    df : pd.DataFrame
        Deve conter as colunas:
            - 'Posto'      : nome da cidade/estação
            - 'Mês/Ano'    : string no formato 'MM/YYYY'
            - 'Acumulado'  : chuva acumulada em mm (numérica ou texto)
    month_year : str
        Mês/Ano no formato 'MM/YYYY', e.g. '06/2025'.
    top_n : int, opcional (padrão = 10)
        Quantidade de cidades a exibir.
    figsize : tuple, opcional
        Tamanho da figura em polegadas.

    --------
    Retorna
    --------
    matplotlib.figure.Figure
        Figura com gráfico de barras.
    """
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    df = df.copy()
    df["Acumulado"] = pd.to_numeric(df["Acumulado"], errors="coerce")

    # Filtra e ordena
    top_cities = (
        df.loc[df["Mês/Ano"] == month_year, ["Posto", "Acumulado"]]
          .sort_values("Acumulado", ascending=False)
          .head(top_n)
          .reset_index(drop=True)
    )

    # Estilo escuro
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#222222")
    ax.set_facecolor("#222222")

    # Gradiente de cor
    cmap = plt.get_cmap(cmap_name)
    norm = plt.Normalize(vmin=top_cities["Acumulado"].min(), vmax=top_cities["Acumulado"].max())
    colors = cmap(norm(top_cities["Acumulado"]))

    # Plot
    bars = ax.bar(top_cities["Posto"], top_cities["Acumulado"], color=colors)
    ax.bar_label(bars,
                 labels=[f"{v:.1f}" for v in top_cities["Acumulado"]],
                 padding=3, color="white", fontsize=9)

    # Títulos e eixos
    ax.set_title(f"Top {len(top_cities)} – Chuva acumulada • {month_year}",
                 color="white", fontsize=14)
    ax.set_xlabel("Cidade", color="white")
    ax.set_ylabel("Chuva (mm)", color="white")

    # Remove apenas a borda superior e direita
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Ajuste de ticks
    plt.setp(ax.get_xticklabels(),
             rotation=rotation, ha="right", rotation_mode="anchor",
             fontsize=tick_labelsize, color="white")
    ax.tick_params(axis="y", labelsize=10, colors="white")

    # Mantém grid, sem alterar as outras bordas
    ax.grid(True, linestyle="--", linewidth=0.5, color="gray", alpha=0.7)

    plt.tight_layout()
    return fig