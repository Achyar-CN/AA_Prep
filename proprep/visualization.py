# proprep/visualization.py

import pandas as pd
import plotly.graph_objects as go
from scipy.stats import shapiro

def create_comparison_viz_and_stats(df_raw, df_clean, col_to_eval):
    """
    Membuat visualisasi perbandingan, tabel statistik, dan teks interpretasi.
    """
    if col_to_eval is None or df_raw is None or df_clean is None:
        return go.Figure(), pd.DataFrame(), ""

    fig = go.Figure()
    stats_data = []

    # Data Mentah
    if col_to_eval in df_raw.columns and pd.api.types.is_numeric_dtype(df_raw[col_to_eval]):
        series_raw = df_raw[col_to_eval].dropna()
        fig.add_trace(go.Histogram(x=series_raw, name='Data Mentah', opacity=0.75, marker_color='#636EFA'))
        if len(series_raw) >= 3:
            stats_data.append({'Versi Data': 'Mentah', 'Variance': f"{series_raw.var():.2f}", 'Skewness': f"{series_raw.skew():.2f}", 'Shapiro-Wilk (p-val)': f"{shapiro(series_raw).pvalue:.4f}"})

    # Data Bersih
    if col_to_eval in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[col_to_eval]):
        series_clean = df_clean[col_to_eval].dropna()
        fig.add_trace(go.Histogram(x=series_clean, name='Data Bersih', opacity=0.75, marker_color='#EF553B'))
        if len(series_clean) >= 3:
            stats_data.append({'Versi Data': 'Bersih', 'Variance': f"{series_clean.var():.2f}", 'Skewness': f"{series_clean.skew():.2f}", 'Shapiro-Wilk (p-val)': f"{shapiro(series_clean).pvalue:.4f}"})

    fig.update_layout(barmode='overlay', title_text=f'Perbandingan Distribusi Kolom "{col_to_eval}"', xaxis_title_text=col_to_eval, yaxis_title_text='Frekuensi', legend_title_text='Legenda')
    fig.update_traces(opacity=0.7)
    
    stats_df = pd.DataFrame(stats_data)
    
    interpretation_text = """
    ### 💡 Interpretasi Statistik
    * **Variance (Varians)**: Mengukur seberapa tersebar data dari nilai rata-ratanya. *Nilai yang lebih tinggi berarti data lebih bervariasi*.
    * **Skewness (Kemiringan)**: Mengukur ketidaksimetrisan distribusi data (Nilai ≈ 0: Simetris; > 0: Ekor ke kanan; < 0: Ekor ke kiri).
    * **Shapiro-Wilk (p-value)**: Uji normalitas data (p-value > 0.05: Cenderung Normal; p-value < 0.05: Cenderung Tidak Normal).
    """
    
    return fig, stats_df, interpretation_text