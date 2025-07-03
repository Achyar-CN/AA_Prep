# Mengekspos fungsi utama ke level atas paket
from .processing import clean_and_encode_dataframe
from .visualization import create_comparison_viz_and_stats
from .app import launch as launch_app

# Mendefinisikan apa yang diimpor saat 'from proprep import *' digunakan
__all__ = [
    'clean_and_encode_dataframe',
    'create_comparison_viz_and_stats',
    'launch_app'
]