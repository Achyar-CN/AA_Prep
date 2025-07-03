# proprep/app.py

import gradio as gr
import pandas as pd
import numpy as np
from .processing import clean_and_encode_dataframe # Relative import
from .visualization import create_comparison_viz_and_stats # Relative import

def launch():
    """Meluncurkan antarmuka pengguna Gradio untuk eksperimentasi data preparation."""
    
    # --- Fungsi Interaksi Gradio ---
    def load_and_update_options(file_obj):
        if file_obj is None: return None, gr.update(choices=[], value=[]), gr.update(choices=[], value=None)
        df = pd.read_csv(file_obj.name)
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        return df, gr.update(choices=cat_cols, value=[]), gr.update(choices=num_cols, value=num_cols[0] if num_cols else None)

    def run_full_process(file_obj, *args):
        (numeric_strategy, numeric_constant, cat_impute_strategy, cat_constant, 
         handle_outliers, cat_encoding_strategy, cols_to_encode, 
         hash_n_components, col_to_eval) = args
        if file_obj is None: raise gr.Error("Mohon unggah file CSV terlebih dahulu!")
        df_raw = pd.read_csv(file_obj.name)
        df_clean = clean_and_encode_dataframe(df_raw, numeric_strategy, numeric_constant, cat_impute_strategy, cat_constant, handle_outliers, cat_encoding_strategy, cols_to_encode, hash_n_components)
        viz, stats, interpretation = create_comparison_viz_and_stats(df_raw, df_clean, col_to_eval)
        return df_raw, df_clean, viz, stats, interpretation, df_raw, df_clean, gr.update(choices=df_clean.select_dtypes(include=np.number).columns.tolist())

    # --- Definisi Antarmuka Gradio ---
    with gr.Blocks(theme=gr.themes.Soft(), title="Aplikasi Data Preparation") as demo:
        gr.Markdown("# 🚀 Aplikasi Data Preparation dengan Evaluasi Statistik")
        
        raw_df_state = gr.State()
        clean_df_state = gr.State()
        
        # ... (Sisa kode UI Gradio sama persis seperti sebelumnya) ...
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 1. Konfigurasi Proses")
                file_input = gr.File(label="Unggah File CSV", file_types=[".csv"])
                with gr.Accordion("Opsi Data Numerik", open=True):
                    numeric_imputation_dd = gr.Dropdown(['Tidak ada', 'Median', 'Mean (Rata-rata)', 'Modus', 'Konstanta', 'End-of-Tail', 'KNN Imputer'], label="Strategi Nilai Hilang Numerik", value='Tidak ada')
                    numeric_constant_input = gr.Number(label="Nilai Konstanta Numerik", value=0, visible=False, interactive=True)
                    outlier_cb = gr.Checkbox(label="Terapkan Capping Outlier (IQR)", value=False)
                with gr.Accordion("Opsi Data Kategorikal", open=True):
                    categorical_impute_dd = gr.Dropdown(['Tidak ada', 'Modus (Paling Sering Muncul)', 'Konstanta'], label="Strategi Nilai Hilang Kategorikal", value='Tidak ada')
                    categorical_constant_input = gr.Textbox(label="String Konstanta Kategorikal", value="Missing", visible=False, interactive=True)
                    categorical_encoding_dd = gr.Dropdown(["Tidak ada", "One-Hot Encoding", "Ordinal Encoding", "Frequency Encoding", "Binary Encoding", "Hashing Encoder"], label="Metode Encoding", value="Tidak ada")
                    hashing_components_input = gr.Number(label="Jumlah Komponen Hash", value=8, visible=False, interactive=True, minimum=2, step=1)
                    categorical_cols_cbg = gr.CheckboxGroup(label="Pilih Kolom untuk Encoding")
                apply_btn = gr.Button("✨ Terapkan & Evaluasi", variant="primary")
            with gr.Column(scale=5):
                gr.Markdown("### 2. Hasil & Evaluasi")
                with gr.Tabs():
                    with gr.TabItem("Pratinjau Data"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("#### Data Mentah"); df_raw_output = gr.DataFrame(interactive=False)
                            with gr.Column():
                                gr.Markdown("#### Data Hasil"); df_clean_output = gr.DataFrame(interactive=False)
                    with gr.TabItem("📊 Evaluasi & Visualisasi"):
                        gr.Markdown("Pilih kolom numerik untuk melihat perbandingan distribusinya.")
                        eval_col_dd = gr.Dropdown(label="Pilih Kolom untuk Evaluasi")
                        plot_output = gr.Plot()
                        stats_output = gr.DataFrame(label="Perbandingan Statistik")
                        interpretation_output = gr.Markdown()
        
        # --- Event Listeners ---
        file_input.upload(fn=load_and_update_options, inputs=[file_input], outputs=[df_raw_output, categorical_cols_cbg, eval_col_dd])
        def toggle_visibility(choice, target_option): return gr.update(visible=(choice == target_option))
        numeric_imputation_dd.change(lambda choice: toggle_visibility(choice, 'Konstanta'), numeric_imputation_dd, numeric_constant_input)
        categorical_impute_dd.change(lambda choice: toggle_visibility(choice, 'Konstanta'), categorical_impute_dd, categorical_constant_input)
        categorical_encoding_dd.change(lambda choice: toggle_visibility(choice, 'Hashing Encoder'), categorical_encoding_dd, hashing_components_input)
        all_inputs = [numeric_imputation_dd, numeric_constant_input, categorical_impute_dd, categorical_constant_input, outlier_cb, categorical_encoding_dd, categorical_cols_cbg, hashing_components_input, eval_col_dd]
        apply_btn.click(fn=run_full_process, inputs=[file_input, *all_inputs], outputs=[df_raw_output, df_clean_output, plot_output, stats_output, interpretation_output, raw_df_state, clean_df_state, eval_col_dd])
        eval_col_dd.change(fn=create_comparison_viz_and_stats, inputs=[raw_df_state, clean_df_state, eval_col_dd], outputs=[plot_output, stats_output, interpretation_output])

    # Jalankan aplikasi
    demo.launch()