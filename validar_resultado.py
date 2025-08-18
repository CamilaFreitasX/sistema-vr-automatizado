#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação do Sistema de VR
Valida se a planilha gerada atende aos requisitos especificados
"""

import pandas as pd
import os
from datetime import datetime

def validar_planilha_vr():
    """
    Valida a planilha VR gerada contra os requisitos
    """
    print("🔍 INICIANDO VALIDAÇÃO DA PLANILHA VR")
    print("=" * 60)
    
    # Verificar se o arquivo foi gerado
    arquivo_gerado = "VR_MENSAL_GERADO.xlsx"
    if not os.path.exists(arquivo_gerado):
        print("❌ Arquivo VR_MENSAL_GERADO.xlsx não encontrado!")
        return False
    
    print(f"✅ Arquivo encontrado: {arquivo_gerado}")
    
    try:
        # Carregar a planilha gerada
        df_gerado = pd.read_excel(arquivo_gerado, sheet_name='VR Mensal')
        print(f"📊 Planilha carregada: {len(df_gerado)} registros")
        
        # Validações básicas
        validacoes = []
        
        # 1. Verificar colunas obrigatórias
        colunas_esperadas = [
            'Matricula', 'Admissão', 'Sindicato do Colaborador', 
            'Competência', 'Dias', 'VALOR DIÁRIO VR', 'TOTAL',
            'Custo empresa', 'Desconto profissional'
        ]
        
        colunas_presentes = df_gerado.columns.tolist()
        print(f"\n📋 Colunas na planilha: {len(colunas_presentes)}")
        
        for col in colunas_esperadas:
            if col in colunas_presentes:
                validacoes.append((f"Coluna '{col}' presente", "✅"))
            else:
                validacoes.append((f"Coluna '{col}' ausente", "❌"))
        
        # 2. Verificar se há dados
        if len(df_gerado) > 0:
            validacoes.append((f"Dados presentes: {len(df_gerado)} registros", "✅"))
        else:
            validacoes.append(("Nenhum dado encontrado", "❌"))
        
        # 3. Verificar cálculos (amostra)
        if 'TOTAL' in df_gerado.columns and 'Dias' in df_gerado.columns and 'VALOR DIÁRIO VR' in df_gerado.columns:
            # Verificar se TOTAL = Dias * VALOR DIÁRIO VR
            df_teste = df_gerado.dropna(subset=['TOTAL', 'Dias', 'VALOR DIÁRIO VR']).head(10)
            calculos_corretos = 0
            
            for idx, row in df_teste.iterrows():
                total_esperado = row['Dias'] * row['VALOR DIÁRIO VR']
                if abs(row['TOTAL'] - total_esperado) < 0.01:  # Tolerância para arredondamento
                    calculos_corretos += 1
            
            if calculos_corretos == len(df_teste):
                validacoes.append((f"Cálculos TOTAL corretos (amostra de {len(df_teste)})", "✅"))
            else:
                validacoes.append((f"Cálculos TOTAL incorretos: {calculos_corretos}/{len(df_teste)}", "❌"))
        
        # 4. Verificar distribuição de custos (80% empresa, 20% colaborador)
        if 'TOTAL' in df_gerado.columns and 'Custo empresa' in df_gerado.columns and 'Desconto profissional' in df_gerado.columns:
            df_teste = df_gerado.dropna(subset=['TOTAL', 'Custo empresa', 'Desconto profissional']).head(10)
            distribuicao_correta = 0
            
            for idx, row in df_teste.iterrows():
                custo_empresa_esperado = row['TOTAL'] * 0.8
                desconto_colaborador_esperado = row['TOTAL'] * 0.2
                
                if (abs(row['Custo empresa'] - custo_empresa_esperado) < 0.01 and 
                    abs(row['Desconto profissional'] - desconto_colaborador_esperado) < 0.01):
                    distribuicao_correta += 1
            
            if distribuicao_correta == len(df_teste):
                validacoes.append((f"Distribuição de custos correta (amostra de {len(df_teste)})", "✅"))
            else:
                validacoes.append((f"Distribuição de custos incorreta: {distribuicao_correta}/{len(df_teste)}", "❌"))
        
        # 5. Verificar se há matrículas duplicadas
        if 'Matricula' in df_gerado.columns:
            matriculas_duplicadas = df_gerado['Matricula'].duplicated().sum()
            if matriculas_duplicadas == 0:
                validacoes.append(("Sem matrículas duplicadas", "✅"))
            else:
                validacoes.append((f"Matrículas duplicadas encontradas: {matriculas_duplicadas}", "⚠️"))
        
        # 6. Verificar valores não nulos em campos críticos
        campos_criticos = ['Matricula', 'Dias', 'VALOR DIÁRIO VR', 'TOTAL']
        for campo in campos_criticos:
            if campo in df_gerado.columns:
                nulos = df_gerado[campo].isnull().sum()
                if nulos == 0:
                    validacoes.append((f"Campo '{campo}' sem valores nulos", "✅"))
                else:
                    validacoes.append((f"Campo '{campo}' com {nulos} valores nulos", "⚠️"))
        
        # Exibir resultados
        print("\n🔍 RESULTADOS DA VALIDAÇÃO:")
        print("-" * 60)
        
        sucessos = 0
        alertas = 0
        erros = 0
        
        for validacao, status in validacoes:
            print(f"{status} {validacao}")
            if status == "✅":
                sucessos += 1
            elif status == "⚠️":
                alertas += 1
            else:
                erros += 1
        
        print("\n📊 RESUMO DA VALIDAÇÃO:")
        print(f"✅ Sucessos: {sucessos}")
        print(f"⚠️  Alertas: {alertas}")
        print(f"❌ Erros: {erros}")
        
        # Estatísticas gerais
        print("\n📈 ESTATÍSTICAS GERAIS:")
        print(f"📊 Total de colaboradores: {len(df_gerado)}")
        
        if 'TOTAL' in df_gerado.columns:
            total_vr = df_gerado['TOTAL'].sum()
            print(f"💰 Valor total VR: R$ {total_vr:,.2f}")
        
        if 'Custo empresa' in df_gerado.columns:
            custo_empresa = df_gerado['Custo empresa'].sum()
            print(f"🏢 Custo empresa: R$ {custo_empresa:,.2f}")
        
        if 'Desconto profissional' in df_gerado.columns:
            desconto_colaborador = df_gerado['Desconto profissional'].sum()
            print(f"👤 Desconto colaboradores: R$ {desconto_colaborador:,.2f}")
        
        # Verificar distribuição por sindicato
        if 'Sindicato do Colaborador' in df_gerado.columns:
            print("\n🏛️  DISTRIBUIÇÃO POR SINDICATO:")
            sindicatos = df_gerado['Sindicato do Colaborador'].value_counts()
            for sindicato, count in sindicatos.head(5).items():
                print(f"  {sindicato}: {count} colaboradores")
        
        print("\n" + "=" * 60)
        
        if erros == 0:
            print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
            return True
        else:
            print("❌ VALIDAÇÃO ENCONTROU PROBLEMAS!")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante a validação: {str(e)}")
        return False

if __name__ == "__main__":
    validar_planilha_vr()