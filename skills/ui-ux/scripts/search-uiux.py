#!/usr/bin/env python3
import csv
import sys
import os

BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def query_dataset(filename, search_term):
    filepath = os.path.join(BASE_DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Dataset {filename} não encontrado.")
        return

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        results = [row for row in reader if any(search_term.lower() in str(val).lower() for val in row.values())]
        
    print(f"--- Resultados em {filename} para '{search_term}' ---")
    for r in results:
        for k, v in r.items():
            print(f"  {k}: {v}")
        print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python search-uiux.py <dataset_csv> <termo_de_busca>")
        print("Exemplo: python search-uiux.py colors.csv saas")
        sys.exit(1)

    query_dataset(sys.argv[1], sys.argv[2])