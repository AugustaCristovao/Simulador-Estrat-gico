# 💰 Simulador Comparativo de Renda Fixa

Um aplicativo web interativo desenvolvido em **Streamlit** para comparar investimentos em renda fixa (CDB, LCI e LCA), ajudando investidores a tomar decisões mais informadas sobre seus investimentos.

## 📋 Índice

- [Características](#-características)
- [Tipos de Investimento Suportados](#-tipos-de-investimento-suportados)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Cálculos Realizados](#-cálculos-realizados)
- [Screenshots](#-screenshots)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Limitações](#-limitações)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Características

- **Interface intuitiva**: Design limpo e fácil de usar
- **Comparação simultânea**: Analise até 3 investimentos lado a lado
- **Cálculos precisos**: Inclui tributação, juros compostos e aportes mensais
- **Visualização gráfica**: Acompanhe a evolução dos investimentos ao longo do tempo
- **Educativo**: Informações detalhadas sobre cada tipo de investimento

## 🏦 Tipos de Investimento Suportados

### CDB (Certificado de Depósito Bancário)
- Garantido pelo FGC até R$ 250.000
- **Tributação**: IR regressivo (22,5% a 15% conforme prazo)
- Liquidez variável conforme produto

### LCI (Letra de Crédito Imobiliário)
- Garantido pelo FGC até R$ 250.000
- **Tributação**: Isento de IR
- Carência mínima de 90 dias

### LCA (Letra de Crédito do Agronegócio)
- Garantido pelo FGC até R$ 250.000
- **Tributação**: Isento de IR
- Carência mínima de 90 dias

## ⚡ Funcionalidades

### Tipos de Rentabilidade
1. **Prefixada**: Taxa fixa anual (ex: 11% a.a.)
2. **Pós-fixada**: Percentual do CDI (ex: 105% do CDI)
3. **Híbrida**: IPCA + taxa adicional (ex: IPCA + 5% a.a.)

### Recursos Principais
- ✅ Simulação com aportes mensais
- ✅ Cálculo automático de IR regressivo para CDB
- ✅ Comparação de até 3 investimentos simultaneamente
- ✅ Gráfico de evolução temporal
- ✅ Tabela resumo com destaque da melhor opção
- ✅ Cálculo de rentabilidade anual equivalente
- ✅ Interface educativa com explicações

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/simulador-renda-fixa.git
cd simulador-renda-fixa
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o aplicativo**
```bash
streamlit run simulador_renda_fixa.py
```

5. **Acesse no navegador**
O aplicativo será aberto automaticamente em `http://localhost:8501`

## 📊 Como Usar

### 1. Configurar Parâmetros Gerais
- **Valor inicial**: Quantia a ser investida no início
- **Aporte mensal**: Valor a ser adicionado mensalmente (opcional)
- **Prazo**: Período do investimento em dias
- **CDI atual**: Taxa CDI de referência (% a.a.)
- **IPCA atual**: Taxa IPCA de referência (% a.a.)

### 2. Definir Investimentos
Para cada investimento (até 3):
- Escolha o tipo: CDB, LCI ou LCA
- Selecione o tipo de rentabilidade
- Informe a taxa oferecida
- Marque para incluir na comparação

### 3. Analisar Resultados
- **Tabela resumo**: Compare valores bruto, líquido e rentabilidade
- **Gráfico**: Visualize a evolução mês a mês
- **Melhor opção**: Identificação automática do melhor investimento
- **Diferença**: Comparação quantitativa entre as opções

## 🧮 Cálculos Realizados

### Juros Compostos
```
Montante = Capital × (1 + taxa_mensal)^meses + Aportes_acumulados
```

### Tributação IR (CDB)
- **Até 180 dias**: 22,5%
- **181 a 360 dias**: 20%
- **361 a 720 dias**: 17,5%
- **Acima de 720 dias**: 15%

### Conversão de Taxas
- **Anual para mensal**: `(1 + taxa_anual)^(1/12) - 1`
- **CDI percentual**: `CDI_mensal × (percentual/100)`
- **IPCA híbrido**: `IPCA_mensal + taxa_adicional_mensal`

## 📷 Screenshots

### Interface Principal
![Interface Principal](screenshots/interface-principal.png)

### Resultados da Simulação
![Resultados](screenshots/resultados.png)

### Gráfico de Evolução
![Gráfico](screenshots/grafico-evolucao.png)

## 🛠 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para aplicações web em Python
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[NumPy](https://numpy.org/)**: Computação científica
- **[Plotly](https://plotly.com/)**: Visualização de dados interativa
- **Python**: Linguagem de programação principal

## ⚠️ Limitações

### Premissas da Simulação
- CDI e IPCA permanecem constantes durante todo o período
- Aportes mensais são realizados no início de cada mês
- IR calculado apenas sobre rendimentos (conforme legislação)
- Não considera IOF (aplicável apenas para resgates em menos de 30 dias)
- Simulação educativa - não constitui recomendação de investimento

### Considerações Importantes
- Rentabilidades passadas não garantem resultados futuros
- Sempre consulte um profissional qualificado antes de investir
- Considere seu perfil de risco e objetivos financeiros
- Verifique as condições específicas de cada produto

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Ideias para Contribuição
- Adicionar novos tipos de investimento (Tesouro Direto, Fundos)
- Implementar simulação de inflação variável
- Adicionar exportação de resultados (PDF, Excel)
- Melhorar responsividade mobile
- Adicionar testes unitários

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

Para dúvidas, sugestões ou reportar problemas:

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/simulador-renda-fixa/issues)
- **Email**: seu-email@exemplo.com
- **LinkedIn**: [Seu Perfil](https://linkedin.com/in/seu-perfil)

---

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/Status-Ativo-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!**

> **Disclaimer**: Este simulador é uma ferramenta educativa e não constitui consultoria financeira. Sempre busque orientação profissional qualificada antes de tomar decisões de investimento.