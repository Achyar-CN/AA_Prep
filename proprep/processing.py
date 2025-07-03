# proprep/processing.py

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import category_encoders as ce

def clean_and_encode_dataframe(
    df: pd.DataFrame,
    numeric_strategy: str = 'Tidak ada',
    numeric_constant: float = 0,
    categorical_impute_strategy: str = 'Tidak ada',
    categorical_constant: str = 'Missing',
    handle_outliers: bool = False,
    categorical_encoding_strategy: str = 'Tidak ada',
    cols_to_encode: list = None,
    hash_n_components: int = 8
):
    """
    Fungsi utama untuk membersihkan, mengisi nilai hilang, dan melakukan encoding pada DataFrame.
    """
    df_processed = df.copy()
    if cols_to_encode is None:
        cols_to_encode = []

    numeric_cols = df_processed.select_dtypes(include=np.number).columns.tolist()
    categorical_cols_to_impute = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()

    # 1. Penanganan Missing Values Numerik
    if numeric_strategy != 'Tidak ada' and df_processed[numeric_cols].isnull().sum().sum() > 0:
        if numeric_strategy == 'Mean (Rata-rata)':
            impute_values = df_processed[numeric_cols].mean()
        elif numeric_strategy == 'Median':
            impute_values = df_processed[numeric_cols].median()
        elif numeric_strategy == 'Modus':
            impute_values = df_processed[numeric_cols].mode().iloc[0]
        elif numeric_strategy == 'Konstanta':
            impute_values = numeric_constant
        elif numeric_strategy == 'End-of-Tail':
            impute_values = df_processed[numeric_cols].mean() + (3 * df_processed[numeric_cols].std())
        elif numeric_strategy == 'KNN Imputer':
            imputer = KNNImputer(n_neighbors=5)
            df_processed[numeric_cols] = imputer.fit_transform(df_processed[numeric_cols])
            impute_values = None # KNN handled separately
        
        if impute_values is not None:
            df_processed[numeric_cols] = df_processed[numeric_cols].fillna(impute_values)

    # 2. Penanganan Missing Values Kategorikal
    if categorical_impute_strategy != 'Tidak ada' and df_processed[categorical_cols_to_impute].isnull().sum().sum() > 0:
        fill_value = categorical_constant
        if categorical_impute_strategy == 'Modus (Paling Sering Muncul)':
            for col in categorical_cols_to_impute:
                mode_val = df_processed[col].mode().iloc[0]
                df_processed[col] = df_processed[col].fillna(mode_val)
        else: # Konstanta
            df_processed[categorical_cols_to_impute] = df_processed[categorical_cols_to_impute].fillna(fill_value)

    # 3. Penanganan Outlier
    if handle_outliers:
        for col in numeric_cols:
            q1 = df_processed[col].quantile(0.25)
            q3 = df_processed[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            df_processed[col] = df_processed[col].clip(lower=lower_bound, upper=upper_bound)

    # 4. Encoding
    if categorical_encoding_strategy != "Tidak ada" and cols_to_encode:
        df_processed[cols_to_encode] = df_processed[cols_to_encode].fillna('Missing_Internal')
        
        encoder = None
        if categorical_encoding_strategy == "One-Hot Encoding":
            encoder = ce.OneHotEncoder(cols=cols_to_encode, use_cat_names=True)
        elif categorical_encoding_strategy == "Ordinal Encoding":
            encoder = ce.OrdinalEncoder(cols=cols_to_encode)
        elif categorical_encoding_strategy == "Frequency Encoding":
            encoder = ce.CountEncoder(cols=cols_to_encode, normalize=False)
        elif categorical_encoding_strategy == "Binary Encoding":
            encoder = ce.BinaryEncoder(cols=cols_to_encode)
        elif categorical_encoding_strategy == "Hashing Encoder":
            encoder = ce.HashingEncoder(cols=cols_to_encode, n_components=int(hash_n_components))

        if encoder:
            df_processed = encoder.fit_transform(df_processed)
        
        if categorical_encoding_strategy == "Frequency Encoding":
             df_processed.rename(columns={col: f"{col}_freq" for col in cols_to_encode}, inplace=True)
        
        df_processed.replace('Missing_Internal', np.nan, inplace=True)

    return df_processed