#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar as validações da aba "Validações"
"""

import pandas as pd

def verificar_validacoes():
    try:
        df_validacoes = pd.read_excel('Desafio 4 - Dados/VR MENSAL 05.2025.xlsx', sheet_name='Validações')
        print('📋 VALIDAÇÕES DA ABA "Validações":')
        print('=' * 50)
        
        for idx, row in df_validacoes.iterrows():
            if pd.notna(row['Validações']):
                validacao = str(row['Validações']).strip()
                if validacao:
                    print(f'✅ {validacao}')
        
        print('=' * 50)
        print(f'Total de validações encontradas: {len(df_validacoes)}')
        
    except Exception as e:
        print(f'Erro: {e}')

if __name__ == "__main__":
    verificar_validacoes()