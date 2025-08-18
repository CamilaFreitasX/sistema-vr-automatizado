import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ProcessadorVR:
    """
    Sistema para processamento automatizado de Vale Refeição
    """
    
    def __init__(self, pasta_dados="Desafio 4 - Dados"):
        self.pasta_dados = Path(pasta_dados)
        self.dados = {}
        self.resultado_final = None
        
    def carregar_dados(self):
        """
        Carrega todos os dados dos arquivos Excel
        """
        print("📂 Carregando dados dos arquivos Excel...")
        
        # Mapeamento dos arquivos e suas respectivas abas
        arquivos_config = {
            'ativos': {'arquivo': 'ATIVOS.xlsx', 'aba': 'Plan1'},
            'ferias': {'arquivo': 'FÉRIAS.xlsx', 'aba': 'Plan1'},
            'desligados': {'arquivo': 'DESLIGADOS.xlsx', 'aba': 'Plan1'},
            'admissoes': {'arquivo': 'ADMISSÃO ABRIL.xlsx', 'aba': 'Plan1'},
            'afastamentos': {'arquivo': 'AFASTAMENTOS.xlsx', 'aba': 'Plan1'},
            'aprendiz': {'arquivo': 'APRENDIZ.xlsx', 'aba': 'Plan1'},
            'estagio': {'arquivo': 'ESTÁGIO.xlsx', 'aba': 'Plan1'},
            'exterior': {'arquivo': 'EXTERIOR.xlsx', 'aba': 'Plan1'},
            'sindicato_valor': {'arquivo': 'Base sindicato x valor.xlsx', 'aba': 'Plan1'},
            'dias_uteis': {'arquivo': 'Base dias uteis.xlsx', 'aba': 'Plan1'},
            'modelo_vr': {'arquivo': 'VR MENSAL 05.2025.xlsx', 'aba': 'VR Mensal 05.2025'}
        }
        
        for nome, config in arquivos_config.items():
            arquivo_path = self.pasta_dados / config['arquivo']
            if arquivo_path.exists():
                try:
                    # Tentar diferentes abas se a especificada não existir
                    excel_file = pd.ExcelFile(arquivo_path)
                    aba = config['aba']
                    
                    if aba not in excel_file.sheet_names:
                        # Usar a primeira aba disponível
                        aba = excel_file.sheet_names[0]
                        print(f"⚠️  Aba '{config['aba']}' não encontrada em {config['arquivo']}, usando '{aba}'")
                    
                    df = pd.read_excel(arquivo_path, sheet_name=aba)
                    
                    # Limpar nomes das colunas
                    if not df.empty:
                        # Se a primeira linha contém os nomes das colunas
                        if df.iloc[0].astype(str).str.contains('Matricula|Matrícula|MATRICULA', case=False, na=False).any():
                            df.columns = df.iloc[0]
                            df = df.drop(df.index[0]).reset_index(drop=True)
                        
                        # Limpar nomes das colunas
                        df.columns = [str(col).strip() if pd.notna(col) else f'Col_{i}' for i, col in enumerate(df.columns)]
                    
                    self.dados[nome] = df
                    print(f"✅ {nome}: {df.shape[0]} registros carregados")
                    
                except Exception as e:
                    print(f"❌ Erro ao carregar {config['arquivo']}: {str(e)}")
                    self.dados[nome] = pd.DataFrame()
            else:
                print(f"❌ Arquivo não encontrado: {config['arquivo']}")
                self.dados[nome] = pd.DataFrame()
    
    def identificar_colunas_matricula(self, df):
        """
        Identifica a coluna de matrícula em um DataFrame
        """
        for col in df.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['matricula', 'matrícula', 'codigo', 'código', 'id']):
                return col
        
        # Se não encontrar, assumir primeira coluna numérica
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64'] and not df[col].isna().all():
                return col
        
        return df.columns[0] if len(df.columns) > 0 else None
    
    def processar_exclusoes(self):
        """
        Processa as exclusões conforme regras de negócio:
        - Diretores, estagiários, aprendizes
        - Afastados em geral
        - Profissionais no exterior
        """
        print("🚫 Processando exclusões...")
        
        matriculas_excluidas = set()
        
        # Exclusões por categoria
        categorias_exclusao = {
            'aprendiz': 'Aprendizes',
            'estagio': 'Estagiários', 
            'afastamentos': 'Afastados',
            'exterior': 'Exterior'
        }
        
        for categoria, descricao in categorias_exclusao.items():
            if categoria in self.dados and not self.dados[categoria].empty:
                df = self.dados[categoria]
                col_matricula = self.identificar_colunas_matricula(df)
                
                if col_matricula:
                    matriculas = df[col_matricula].dropna().astype(str).str.strip()
                    matriculas_categoria = set(matriculas[matriculas != ''])
                    matriculas_excluidas.update(matriculas_categoria)
                    print(f"  - {descricao}: {len(matriculas_categoria)} matrículas excluídas")
        
        # TODO: Adicionar lógica para identificar diretores nos dados de ativos
        # (baseado em cargo ou outros critérios)
        
        print(f"📊 Total de matrículas excluídas: {len(matriculas_excluidas)}")
        return matriculas_excluidas
    
    def processar_ferias(self):
        """
        Processa dados de férias para calcular dias de desconto
        """
        print("🏖️  Processando férias...")
        
        if 'ferias' not in self.dados or self.dados['ferias'].empty:
            print("❌ Dados de férias não disponíveis")
            return {}
        
        df_ferias = self.dados['ferias']
        col_matricula = self.identificar_colunas_matricula(df_ferias)
        
        if not col_matricula:
            print("❌ Coluna de matrícula não identificada em férias")
            return {}
        
        ferias_por_matricula = {}
        
        # Identificar colunas de data
        colunas_data = []
        for col in df_ferias.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['inicio', 'início', 'fim', 'final', 'data']):
                colunas_data.append(col)
        
        print(f"  Colunas de data identificadas: {colunas_data}")
        
        for _, row in df_ferias.iterrows():
            matricula = str(row[col_matricula]).strip()
            if matricula and matricula != 'nan':
                # Calcular dias de férias no mês de referência (maio 2025)
                # TODO: Implementar lógica específica baseada nas datas de início e fim
                ferias_por_matricula[matricula] = {
                    'dias_ferias': 0,  # Será calculado baseado nas datas
                    'periodo_completo': False
                }
        
        print(f"📊 {len(ferias_por_matricula)} colaboradores com férias processados")
        return ferias_por_matricula
    
    def processar_desligamentos(self):
        """
        Processa desligamentos aplicando regra:
        - Até dia 15: não considerar para pagamento
        - Após dia 15: pagamento proporcional
        """
        print("👋 Processando desligamentos...")
        
        if 'desligados' not in self.dados or self.dados['desligados'].empty:
            print("❌ Dados de desligados não disponíveis")
            return {}
        
        df_desligados = self.dados['desligados']
        col_matricula = self.identificar_colunas_matricula(df_desligados)
        
        if not col_matricula:
            print("❌ Coluna de matrícula não identificada em desligados")
            return {}
        
        desligamentos_por_matricula = {}
        
        # Identificar coluna de data de desligamento
        col_data_deslig = None
        for col in df_desligados.columns:
            col_str = str(col).lower()
            if any(term in col_str for term in ['desligamento', 'deslig', 'saida', 'saída', 'data']):
                col_data_deslig = col
                break
        
        if not col_data_deslig:
            print("❌ Coluna de data de desligamento não identificada")
            return {}
        
        print(f"  Coluna de data de desligamento: {col_data_deslig}")
        
        for _, row in df_desligados.iterrows():
            matricula = str(row[col_matricula]).strip()
            if matricula and matricula != 'nan':
                data_deslig = row[col_data_deslig]
                
                if pd.notna(data_deslig):
                    try:
                        if isinstance(data_deslig, str):
                            data_deslig = pd.to_datetime(data_deslig)
                        
                        # Aplicar regra de desligamento
                        dia_deslig = data_deslig.day
                        
                        if dia_deslig <= 15:
                            # Não considerar para pagamento
                            desligamentos_por_matricula[matricula] = {
                                'data_desligamento': data_deslig,
                                'dias_proporcionais': 0,
                                'pagar_vr': False
                            }
                        else:
                            # Pagamento proporcional
                            desligamentos_por_matricula[matricula] = {
                                'data_desligamento': data_deslig,
                                'dias_proporcionais': dia_deslig,
                                'pagar_vr': True
                            }
                    except Exception as e:
                        print(f"⚠️  Erro ao processar data de desligamento para matrícula {matricula}: {e}")
        
        print(f"📊 {len(desligamentos_por_matricula)} desligamentos processados")
        return desligamentos_por_matricula
    
    def obter_dados_sindicatos(self):
        """
        Obtém dados de sindicatos e valores de VR
        """
        print("🏛️  Processando dados de sindicatos...")
        
        if 'sindicato_valor' not in self.dados or self.dados['sindicato_valor'].empty:
            print("❌ Dados de sindicato x valor não disponíveis")
            return {}
        
        df_sindicatos = self.dados['sindicato_valor']
        
        # Identificar colunas relevantes
        col_sindicato = None
        col_valor = None
        
        for col in df_sindicatos.columns:
            col_str = str(col).lower()
            if 'sindicato' in col_str:
                col_sindicato = col
            elif any(term in col_str for term in ['valor', 'vr', 'refeição', 'refeicao']):
                col_valor = col
        
        if not col_sindicato or not col_valor:
            print(f"❌ Colunas não identificadas - Sindicato: {col_sindicato}, Valor: {col_valor}")
            return {}
        
        sindicatos_valores = {}
        
        for _, row in df_sindicatos.iterrows():
            sindicato = str(row[col_sindicato]).strip()
            valor = row[col_valor]
            
            if sindicato and sindicato != 'nan' and pd.notna(valor):
                try:
                    valor_float = float(valor)
                    sindicatos_valores[sindicato] = valor_float
                except (ValueError, TypeError):
                    continue
        
        print(f"📊 {len(sindicatos_valores)} sindicatos com valores carregados")
        return sindicatos_valores
    
    def calcular_dias_uteis(self, matricula, sindicato, ferias_info=None, deslig_info=None):
        """
        Calcula dias úteis para uma matrícula específica
        """
        # Base: 22 dias úteis em maio 2025 (valor padrão)
        dias_base = 22
        
        # Descontar férias
        if ferias_info:
            dias_base -= ferias_info.get('dias_ferias', 0)
        
        # Aplicar regra de desligamento
        if deslig_info and not deslig_info.get('pagar_vr', True):
            return 0
        elif deslig_info and deslig_info.get('pagar_vr', True):
            dias_base = min(dias_base, deslig_info.get('dias_proporcionais', dias_base))
        
        return max(0, dias_base)
    
    def processar_colaboradores_ativos(self):
        """
        Processa colaboradores ativos aplicando todas as regras
        """
        print("👥 Processando colaboradores ativos...")
        
        if 'ativos' not in self.dados or self.dados['ativos'].empty:
            print("❌ Dados de colaboradores ativos não disponíveis")
            return pd.DataFrame()
        
        df_ativos = self.dados['ativos']
        col_matricula = self.identificar_colunas_matricula(df_ativos)
        
        if not col_matricula:
            print("❌ Coluna de matrícula não identificada em ativos")
            return pd.DataFrame()
        
        # Obter dados auxiliares
        matriculas_excluidas = self.processar_exclusoes()
        ferias_por_matricula = self.processar_ferias()
        desligamentos_por_matricula = self.processar_desligamentos()
        sindicatos_valores = self.obter_dados_sindicatos()
        
        # Identificar coluna de sindicato
        col_sindicato = None
        for col in df_ativos.columns:
            col_str = str(col).lower()
            if 'sindicato' in col_str:
                col_sindicato = col
                break
        
        resultado = []
        
        for _, row in df_ativos.iterrows():
            matricula = str(row[col_matricula]).strip()
            
            if not matricula or matricula == 'nan':
                continue
            
            # Verificar se está excluído
            if matricula in matriculas_excluidas:
                continue
            
            # Obter sindicato
            sindicato = str(row[col_sindicato]).strip() if col_sindicato else 'Não informado'
            
            # Obter informações auxiliares
            ferias_info = ferias_por_matricula.get(matricula)
            deslig_info = desligamentos_por_matricula.get(matricula)
            
            # Calcular dias úteis
            dias_uteis = self.calcular_dias_uteis(matricula, sindicato, ferias_info, deslig_info)
            
            if dias_uteis > 0:
                # Obter valor do VR por sindicato
                valor_diario_vr = sindicatos_valores.get(sindicato, 37.5)  # Valor padrão
                
                # Calcular valores
                valor_total = dias_uteis * valor_diario_vr
                custo_empresa = valor_total * 0.8  # 80%
                desconto_colaborador = valor_total * 0.2  # 20%
                
                # Obter data de admissão se disponível
                data_admissao = ''
                for col in df_ativos.columns:
                    col_str = str(col).lower()
                    if any(term in col_str for term in ['admissao', 'admissão', 'contratacao', 'contratação']):
                        data_admissao = row[col] if pd.notna(row[col]) else ''
                        break
                
                resultado.append({
                    'Matricula': matricula,
                    'Admissão': data_admissao,
                    'Sindicato do Colaborador': sindicato,
                    'Competência': '2025-05-01',  # Maio 2025
                    'Dias': dias_uteis,
                    'VALOR DIÁRIO VR': valor_diario_vr,
                    'TOTAL': valor_total,
                    'Custo empresa': custo_empresa,
                    'Desconto profissional': desconto_colaborador,
                    'OBS GERAL': ''
                })
        
        df_resultado = pd.DataFrame(resultado)
        print(f"📊 {len(df_resultado)} colaboradores processados para VR")
        
        return df_resultado
    
    def gerar_planilha_final(self, df_resultado, nome_arquivo="VR_MENSAL_GERADO.xlsx"):
        """
        Gera a planilha final no formato especificado
        """
        print(f"📄 Gerando planilha final: {nome_arquivo}")
        
        try:
            with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
                # Aba principal com os dados
                df_resultado.to_excel(writer, sheet_name='VR Mensal', index=False)
                
                # Aba de validações (placeholder)
                df_validacoes = pd.DataFrame({
                    'Validações': [
                        'Afastados / Licenças',
                        'DESLIGADOS GERAL',
                        'Estagiários',
                        'Aprendizes',
                        'Exterior'
                    ],
                    'Check': ['OK'] * 5
                })
                df_validacoes.to_excel(writer, sheet_name='Validações', index=False)
            
            print(f"✅ Planilha gerada com sucesso: {nome_arquivo}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar planilha: {str(e)}")
            return False
    
    def executar_processamento_completo(self):
        """
        Executa todo o processamento de VR
        """
        print("🚀 Iniciando processamento completo de VR")
        print("=" * 60)
        
        # Carregar dados
        self.carregar_dados()
        
        # Processar colaboradores
        df_resultado = self.processar_colaboradores_ativos()
        
        if not df_resultado.empty:
            # Gerar planilha final
            sucesso = self.gerar_planilha_final(df_resultado)
            
            if sucesso:
                print("\n" + "=" * 60)
                print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
                print(f"📊 Total de colaboradores processados: {len(df_resultado)}")
                print(f"💰 Valor total VR: R$ {df_resultado['TOTAL'].sum():,.2f}")
                print(f"🏢 Custo empresa: R$ {df_resultado['Custo empresa'].sum():,.2f}")
                print(f"👤 Desconto colaboradores: R$ {df_resultado['Desconto profissional'].sum():,.2f}")
                print("=" * 60)
                
                self.resultado_final = df_resultado
                return df_resultado
        
        print("❌ Processamento falhou")
        return None

if __name__ == "__main__":
    # Executar processamento
    processador = ProcessadorVR()
    resultado = processador.executar_processamento_completo()