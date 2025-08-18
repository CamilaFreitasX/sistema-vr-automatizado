# Sistema Automatizado de Compra de Vale Refeição (VR)

## Descrição

Este sistema automatiza o processo mensal de compra de VR (Vale Refeição), garantindo que cada colaborador receba o valor correto, considerando ausências, férias, datas de admissão/desligamento e calendário de feriados.

## Funcionalidades Implementadas

### ✅ Processamento de Dados
- **Consolidação de bases**: Unifica informações de 5 planilhas separadas (Ativos, Férias, Desligados, Admissões, Sindicatos)
- **Tratamento de exclusões**: Remove automaticamente diretores, estagiários, aprendizes, afastados e colaboradores no exterior
- **Validação de dados**: Corrige datas inconsistentes e campos faltantes

### ✅ Cálculos Automatizados
- **Dias úteis por colaborador**: Considera sindicatos, férias, afastamentos e desligamentos
- **Regras de desligamento**: Aplicação proporcional baseada na data de comunicação (antes/depois do dia 15)
- **Valores por sindicato**: Cálculo correto baseado nas convenções coletivas
- **Distribuição de custos**: 80% empresa, 20% colaborador

### ✅ Saída Final
- **Planilha formatada**: Gera arquivo Excel no formato especificado
- **Validações**: Implementa todas as verificações necessárias
- **Relatórios**: Estatísticas detalhadas do processamento

## 📁 Arquivos do Sistema

### Scripts Principais
- `sistema_vr.py` - Sistema principal de processamento de VR
- `validar_resultado.py` - Script de validação dos resultados
- `analisar_estrutura.py` - Análise da estrutura dos arquivos Excel
- `relatorio_validacoes.py` - Relatório das validações implementadas
- `verificar_abas.py` - Verificação de abas das planilhas
- `verificar_validacoes.py` - Verificação das validações da aba "Validações"

### Configuração
- `requirements.txt` - Dependências Python necessárias
- `.gitignore` - Arquivos excluídos do controle de versão

### Estrutura de Dados Esperada
O sistema espera uma pasta com os seguintes arquivos Excel:
- `ADMISSÃO ABRIL.xlsx` - Colaboradores admitidos em abril
- `AFASTAMENTOS.xlsx` - Lista de afastados/licenças
- `APRENDIZ.xlsx` - Lista de aprendizes (excluídos)
- `ESTÁGIO.xlsx` - Lista de estagiários (excluídos)
- `EXTERIOR.xlsx` - Colaboradores no exterior (excluídos)
- `DESLIGADOS.xlsx` - Lista de desligamentos
- `FÉRIAS.xlsx` - Colaboradores em férias
- `Base dias uteis.xlsx` - Dias úteis por sindicato
- `Base sindicato x valor.xlsx` - Valores de VR por sindicato
- `VR MENSAL 05.2025.xlsx` - Modelo da planilha final

### Dados de Saída
- `VR_MENSAL_GERADO.xlsx` - Planilha final gerada pelo sistema

## 🚀 Como Usar

### 1. Clonagem do Repositório
```bash
git clone https://github.com/seu-usuario/sistema-vr-automatizado.git
cd sistema-vr-automatizado
```

### 2. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração dos Dados
- Crie uma pasta chamada "Desafio 4 - Dados" (ou ajuste o caminho no código)
- Coloque todos os arquivos Excel necessários nesta pasta
- Certifique-se de que os nomes dos arquivos correspondem aos esperados pelo sistema

### 4. Execução do Sistema
```bash
python sistema_vr.py
```

### 5. Validação dos Resultados
```bash
python validar_resultado.py
```

### 6. Análise de Estruturas (Opcional)
```bash
python analisar_estrutura.py
```

## Resultados do Processamento

### Estatísticas da Última Execução
- **Total de colaboradores processados**: 1.792
- **Valor total VR**: R$ 1.478.400,00
- **Custo empresa (80%)**: R$ 1.182.720,00
- **Desconto colaboradores (20%)**: R$ 295.680,00

### Distribuição por Sindicato
1. **SINDPPD RS**: 1.134 colaboradores
2. **SINDPD SP**: 418 colaboradores
3. **SITEPD PR**: 139 colaboradores
4. **SINDPD RJ**: 101 colaboradores

### Exclusões Aplicadas
- **Aprendizes**: 33 matrículas
- **Estagiários**: 27 matrículas
- **Afastados**: 20 matrículas
- **Exterior**: 4 matrículas
- **Total excluído**: 84 matrículas

## Validações Implementadas

### ✅ Estrutura da Planilha
- Todas as colunas obrigatórias presentes
- Dados consistentes e sem duplicatas
- Campos críticos sem valores nulos

### ✅ Cálculos
- TOTAL = Dias × VALOR DIÁRIO VR
- Custo empresa = TOTAL × 80%
- Desconto profissional = TOTAL × 20%

### ✅ Regras de Negócio
- Exclusões aplicadas corretamente
- Férias consideradas no cálculo
- Desligamentos com regra proporcional
- Valores por sindicato aplicados

## Logs e Monitoramento

O sistema fornece logs detalhados durante a execução:
- ✅ Sucessos (carregamento de dados, processamentos)
- ⚠️ Alertas (abas não encontradas, dados faltantes)
- ❌ Erros (problemas críticos)

## Manutenção

### Atualizações Mensais
1. Substituir os arquivos na pasta "Desafio 4 - Dados" pelos dados do mês atual
2. Executar `python sistema_vr.py`
3. Validar com `python validar_resultado.py`
4. Enviar `VR_MENSAL_GERADO.xlsx` para a operadora

### Ajustes de Valores
- Atualizar "Base sindicato x valor.xlsx" conforme convenções coletivas
- Atualizar "Base dias uteis.xlsx" conforme calendário

## Suporte Técnico

Em caso de problemas:
1. Verificar se todos os arquivos de entrada estão presentes
2. Executar `python analisar_estrutura.py` para diagnosticar
3. Verificar logs de erro no terminal
4. Validar estrutura dos arquivos Excel de entrada

---

**Sistema desenvolvido para automatizar o processo de compra de VR, garantindo precisão, eficiência e conformidade com as regras estabelecidas.**