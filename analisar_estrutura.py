import pandas as pd
import os
from pathlib import Path

def analisar_estrutura_excel():
    """
    Analisa a estrutura de todos os arquivos Excel na pasta 'Desafio 4 - Dados'
    """
    pasta_dados = Path("Desafio 4 - Dados")
    
    if not pasta_dados.exists():
        print(f"Pasta {pasta_dados} não encontrada!")
        return
    
    arquivos_excel = list(pasta_dados.glob("*.xlsx"))
    
    print("=" * 80)
    print("ANÁLISE DA ESTRUTURA DOS ARQUIVOS EXCEL")
    print("=" * 80)
    
    for arquivo in arquivos_excel:
        print(f"\n📁 ARQUIVO: {arquivo.name}")
        print("-" * 50)
        
        try:
            # Ler todas as abas do arquivo
            excel_file = pd.ExcelFile(arquivo)
            print(f"Abas disponíveis: {excel_file.sheet_names}")
            
            for aba in excel_file.sheet_names:
                print(f"\n  📋 ABA: {aba}")
                try:
                    df = pd.read_excel(arquivo, sheet_name=aba, nrows=5)
                    print(f"    Dimensões (primeiras 5 linhas): {df.shape}")
                    print(f"    Colunas: {list(df.columns)}")
                    
                    # Mostrar algumas linhas de exemplo
                    if not df.empty:
                        print("    Exemplo de dados:")
                        for idx, row in df.head(2).iterrows():
                            print(f"      Linha {idx + 1}: {dict(row)}")
                            
                except Exception as e:
                    print(f"    ❌ Erro ao ler aba {aba}: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Erro ao processar arquivo {arquivo.name}: {str(e)}")
    
    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)

if __name__ == "__main__":
    analisar_estrutura_excel()