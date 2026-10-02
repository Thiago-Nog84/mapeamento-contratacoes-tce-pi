import pandas as pd
import json

file_path = r'C:\Dev\Mapeamento TCE\licitações.xlsx'
try:
    df = pd.read_excel(file_path)
    print(f"Colunas: {list(df.columns)}")
    print(f"Total de linhas: {len(df)}")
    print("\nPrimeiras 3 linhas:")
    print(df.head(3).to_string())
except Exception as e:
    print(f"Erro ao ler excel: {e}")
