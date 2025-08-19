# 🍽️ Sistema de Automação VR

**Sistema desenvolvido para automatizar o processo de compra de VR, garantindo precisão, eficiência e conformidade com as regras estabelecidas.**

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação](#-instalação)
- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Estrutura de Dados](#-estrutura-de-dados)
- [Como Usar](#-como-usar)
- [Funcionalidades](#-funcionalidades)
- [Validações Implementadas](#-validações-implementadas)
- [Arquivos de Saída](#-arquivos-de-saída)
- [Solução de Problemas](#-solução-de-problemas)
- [Manutenção](#-manutenção)
- [Suporte](#-suporte)

## 🎯 Visão Geral

Este sistema automatiza completamente o processo de cálculo e geração de planilhas de Vale Refeição (VR) mensal, processando dados de colaboradores ativos, desligados e aplicando todas as regras de negócio necessárias.

### Principais Benefícios:
- ✅ **Automação Completa**: Elimina processamento manual
- ✅ **Precisão**: Aplicação automática de todas as regras de negócio
- ✅ **Eficiência**: Processamento de milhares de registros em segundos
- ✅ **Conformidade**: Validações automáticas conforme especificações
- ✅ **Auditoria**: Relatórios detalhados de processamento

## 💻 Requisitos do Sistema

### Software Necessário:
- **Python**: Versão 3.7 ou superior
- **Sistema Operacional**: Windows 10/11, macOS, ou Linux
- **Memória RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço em Disco**: 500MB livres

### Verificar Versão do Python:
```bash
python --version
# ou
python3 --version
```

### Instalar Python (se necessário):
- **Windows**: Baixe de [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3` ou baixe de [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

## 🔧 Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/CamilaFreitasX/sistema-vr-automatizado.git
cd sistema-vr-automatizado
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar Instalação
```bash
python -c "import pandas, openpyxl; print('Instalação OK!')"
```

## ⚙️ Configuração do Ambiente

### Estrutura de Pastas Obrigatória:
```
sistema-vr-automatizado/
├── dados/                          # Pasta para planilhas de entrada
│   ├── VR MENSAL 05.2025.xlsx     # Planilha principal com validações
│   ├── COLABORADORES ATIVOS 05.2025.xlsx
│   └── DESLIGADOS 05.2025.xlsx
├── sistema_vr.py                   # Sistema principal
├── validar_resultado.py            # Validação automática
├── requirements.txt                # Dependências
└── README.md                       # Este arquivo
```

### Criar Pasta de Dados:
```bash
# Windows
mkdir dados

# macOS/Linux
mkdir dados
```

## 📊 Estrutura de Dados

### Planilhas de Entrada Necessárias:

#### 1. `VR MENSAL 05.2025.xlsx`
- **Aba "Validações"**: Contém as 14 regras de validação
- **Formato**: Preservado automaticamente no arquivo de saída

#### 2. `COLABORADORES ATIVOS 05.2025.xlsx`
**Colunas obrigatórias:**
- `Matricula`: Número único do colaborador
- `Nome`: Nome completo
- `Admissão`: Data de admissão (formato: DD/MM/AAAA)
- `Sindicato do Colaborador`: Nome do sindicato
- `Situação`: Status do colaborador
- `Férias Início`: Data início férias (se aplicável)
- `Férias Fim`: Data fim férias (se aplicável)

#### 3. `DESLIGADOS 05.2025.xlsx`
**Colunas obrigatórias:**
- `Matricula`: Número único do colaborador
- `Nome`: Nome completo
- `Demissão`: Data de demissão (formato: DD/MM/AAAA)
- `Sindicato do Colaborador`: Nome do sindicato

### Valores de VR por Sindicato:
```python
# Configuração atual no sistema
VALORES_VR = {
    'SINDICATO DOS METALÚRGICOS': 26.00,
    'SINDICATO DOS QUÍMICOS': 26.00,
    'SINDICATO DOS COMERCIÁRIOS': 22.00,
    'SINDICATO DOS VIGILANTES': 22.00,
    'SINDICATO DOS RODOVIÁRIOS': 22.00
}
```

## 🚀 Como Usar

### 1. Preparar os Dados
1. Coloque as 3 planilhas Excel na pasta `dados/`
2. Verifique se os nomes dos arquivos estão corretos
3. Confirme que todas as colunas obrigatórias estão presentes

### 2. Executar o Sistema
```bash
python sistema_vr.py
```

### 3. Acompanhar o Processamento
O sistema exibirá:
```
=== SISTEMA DE AUTOMAÇÃO VR ===
Carregando dados...
Processando colaboradores ativos...
Processando desligados...
Aplicando regras de negócio...
Calculando valores...
Gerando planilha final...

=== RESUMO FINANCEIRO ===
Total de colaboradores processados: 1,792
Total VR: R$ 1,478,400.00
Custo empresa (80%): R$ 1,182,720.00
Desconto colaborador (20%): R$ 295,680.00

✅ Planilha gerada: VR_MENSAL_GERADO.xlsx
```

### 4. Validar Resultados (Opcional)
```bash
python validar_resultado.py
```

### 5. Verificar Arquivo de Saída
O arquivo `VR_MENSAL_GERADO.xlsx` será criado com:
- Dados processados na aba principal
- Aba "Validações" preservada
- Formatação adequada para uso

## 🔧 Funcionalidades

### Processamento Automático:
- ✅ **Leitura de múltiplas planilhas Excel**
- ✅ **Cálculo de dias úteis por mês**
- ✅ **Aplicação de regras de sindicatos**
- ✅ **Processamento de férias e afastamentos**
- ✅ **Regras específicas para desligamentos**
- ✅ **Cálculo de custos (80% empresa / 20% colaborador)**
- ✅ **Geração de planilha final formatada**

### Regras de Negócio Implementadas:

#### Exclusões Automáticas:
- Colaboradores afastados/licenças
- Estagiários e aprendizes
- Colaboradores no exterior
- Situações específicas conforme validações

#### Regras de Desligamento:
- **Até dia 15**: Exclusão completa
- **Após dia 15**: Recarga completa com desconto proporcional

#### Cálculo de Férias:
- Desconto proporcional aos dias de férias no mês
- Manutenção do colaborador na planilha

## ✅ Validações Implementadas

O sistema implementa automaticamente as 14 validações da aba "Validações":

1. **Afastados / Licenças**: Exclusão automática
2. **DESLIGADOS GERAL**: Processamento com regras específicas
3. **Admitidos mês**: Inclusão de novos colaboradores
4. **Férias**: Cálculo proporcional
5. **ESTAGIARIO**: Exclusão automática
6. **APRENDIZ**: Exclusão automática
7. **SINDICATOS x VALOR**: Aplicação de valores por sindicato
8. **DESLIGADOS ATÉ O DIA 15**: Exclusão completa
9. **DESLIGADOS DO DIA 16 ATÉ ULTIMO DIA**: Recarga com desconto
10. **ATENDIMENTOS/OBS**: Campo 'OBS GERAL' incluído
11. **Admitidos mês anterior**: Processamento e inclusão
12. **EXTERIOR**: Exclusão automática
13. **ATIVOS**: Processamento padrão
14. **REVISAR CÁLCULO**: Validação automática com 17 verificações

## 📄 Arquivos de Saída

### `VR_MENSAL_GERADO.xlsx`
**Colunas geradas:**
- `Matricula`: Número do colaborador
- `Admissão`: Data de admissão
- `Sindicato do Colaborador`: Sindicato
- `Competência`: Mês/ano de referência
- `Dias`: Dias úteis calculados
- `VALOR DIÁRIO VR`: Valor por dia
- `TOTAL`: Valor total do VR
- `Custo empresa`: 80% do valor total
- `Desconto profissional`: 20% do valor total
- `OBS GERAL`: Observações (férias, desligamentos, etc.)

### Aba "Validações"
- Preservada automaticamente do arquivo original
- Mantém todas as 14 validações
- Formatação original preservada

## 🔍 Solução de Problemas

### Erro: "Arquivo não encontrado"
```bash
# Verificar se os arquivos estão na pasta correta
ls dados/  # macOS/Linux
dir dados\  # Windows
```

### Erro: "Módulo não encontrado"
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Permissão negada"
- Feche o arquivo Excel se estiver aberto
- Verifique permissões da pasta
- Execute como administrador se necessário

### Dados Inconsistentes:
```bash
# Verificar estrutura das planilhas
python verificar_abas.py

# Analisar dados detalhadamente
python analisar_estrutura.py
```

### Performance Lenta:
- Verifique disponibilidade de RAM
- Feche outros programas
- Use SSD se disponível

## 🔄 Manutenção

### Atualizar Valores de VR:
Edite o arquivo `sistema_vr.py`, seção `VALORES_VR`:
```python
VALORES_VR = {
    'SINDICATO DOS METALÚRGICOS': 28.00,  # Novo valor
    'SINDICATO DOS QUÍMICOS': 28.00,      # Novo valor
    # ... outros sindicatos
}
```

### Adicionar Novo Sindicato:
```python
VALORES_VR = {
    # ... sindicatos existentes
    'NOVO SINDICATO': 25.00  # Adicionar aqui
}
```

### Backup dos Dados:
```bash
# Criar backup antes de processar
cp -r dados/ backup_dados_$(date +%Y%m%d)/  # macOS/Linux
robocopy dados backup_dados_%date:~-4,4%%date:~-10,2%%date:~-7,2% /E  # Windows
```

### Logs de Execução:
O sistema gera logs automáticos durante a execução. Para debug detalhado, edite `sistema_vr.py` e descomente as linhas de debug.

## 📞 Suporte

### Scripts Auxiliares Disponíveis:
- `verificar_abas.py`: Verifica estrutura das planilhas
- `analisar_estrutura.py`: Análise detalhada dos dados
- `validar_resultado.py`: Validação automática dos resultados
- `relatorio_validacoes.py`: Relatório das validações implementadas

### Informações do Sistema:
```bash
# Verificar versões
python --version
pip list

# Testar dependências
python -c "import pandas as pd; print(f'Pandas: {pd.__version__}')"
python -c "import openpyxl; print(f'OpenPyXL: {openpyxl.__version__}')"
```

### Contato:
Para suporte técnico ou dúvidas sobre o sistema, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

---

**📊 Sistema desenvolvido para automatizar o processo de compra de VR, garantindo precisão, eficiência e conformidade com as regras estabelecidas.**

*Última atualização: Janeiro 2025*