
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import math

# Tabela de IR Regressivo para CDB
def obter_aliquota_ir(dias):
    """ Retorna a alíquota de IR baseada no prazo do investimento """
    if dias <= 180:
        return 0.225  # 22,5%
    elif dias <= 360:
        return 0.20   # 20%
    elif dias <= 720:
        return 0.175  # 17,5%
    else:
        return 0.15   # 15%

def calcular_rentabilidade_mensal(tipo_rentabilidade, taxa, cdi_anual, ipca_anual):
    """ Calcula a rentabilidade mensal baseada no tipo de indexador """
    if tipo_rentabilidade == "Prefixada":
        return (1 + taxa/100) ** (1/12) - 1
    elif tipo_rentabilidade == "Pós-fixada (% CDI)":
        cdi_mensal = (1 + cdi_anual/100) ** (1/12) - 1
        return cdi_mensal * (taxa/100)
    elif tipo_rentabilidade == "Híbrida (IPCA + %)":
        ipca_mensal = (1 + ipca_anual/100) ** (1/12) - 1
        taxa_adicional_mensal = (1 + taxa/100) ** (1/12) - 1
        return ipca_mensal + taxa_adicional_mensal

def simular_investimento(valor_inicial, aporte_mensal, prazo_dias, rentabilidade_mensal, tipo_investimento, isenta_ir=True):
    """ Simula a evolução do investimento mês a mês """
    prazo_meses = prazo_dias // 30
    saldos = []
    saldo_atual = valor_inicial
    for mes in range(prazo_meses + 1):
        if mes == 0:
            saldos.append(saldo_atual)
        else:
            if aporte_mensal > 0:
                saldo_atual += aporte_mensal
            saldo_atual = saldo_atual * (1 + rentabilidade_mensal)
            saldos.append(saldo_atual)
    saldo_bruto = saldos[-1]

    if tipo_investimento == "CDB" or (tipo_investimento in ['LCI', 'LCA'] and not isenta_ir):
        total_investido = valor_inicial + (aporte_mensal * prazo_meses)
        rendimento_bruto = saldo_bruto - total_investido
        aliquota_ir = obter_aliquota_ir(prazo_dias)
        ir_devido = rendimento_bruto * aliquota_ir
        saldo_liquido = saldo_bruto - ir_devido
    else:
        saldo_liquido = saldo_bruto
        ir_devido = 0

    return saldos, saldo_bruto, saldo_liquido, ir_devido, prazo_meses

# Interface principal
st.title("💰 Simulador Comparativo de Renda Fixa")
st.markdown("**Compare CDB, LCI e LCA e encontre o melhor investimento para seu perfil!**")

# Sidebar com informações educativas
with st.sidebar:
    st.header("📚 Guia Rápido")
    st.subheader("CDB (Certificado de Depósito Bancário)")
    st.write("• Garantido pelo FGC até R$ 250 mil")
    st.write("• Tributação: IR regressivo")
    st.write("• Liquidez: Varia conforme produto")
    st.subheader("LCI (Letra de Crédito Imobiliário)")
    st.write("• Garantido pelo FGC até R$ 250 mil")
    st.write("• Tributação: Isento de IR (exceto LCIs híbridas)")
    st.write("• Carência: Mínimo 90 dias")
    st.subheader("LCA (Letra de Crédito do Agronegócio)")
    st.write("• Garantido pelo FGC até R$ 250 mil")
    st.write("• Tributação: Isento de IR (exceto LCAs híbridas)")
    st.write("• Carência: Mínimo 90 dias")
    st.subheader("Tabela de IR - CDB")
    st.write("• Até 180 dias: 22,5%")
    st.write("• 181 a 360 dias: 20%")
    st.write("• 361 a 720 dias: 17,5%")
    st.write("• Acima de 720 dias: 15%")
    st.markdown("---")
    st.markdown('**Nota:** Existem LCIs/LCAs híbridas que não são isentas de IR. Utilize a opção "Isenta de IR?" para informar.')

# Layout principal em colunas
col1, col2 = st.columns(2)

# Parâmetros gerais
st.header("🎯 Parâmetros de Simulação")
col_param1, col_param2, col_param3 = st.columns(3)
with col_param1:
    valor_inicial = st.number_input(
        "Valor inicial (R$)", min_value=100.0, value=10000.0, step=100.0, format="%.2f"
    )
    aporte_mensal = st.number_input(
        "Aporte mensal (R$)", min_value=0.0, value=500.0, step=50.0, format="%.2f"
    )
with col_param2:
    prazo_dias = st.number_input(
        "Prazo (dias)", min_value=30, max_value=7200, value=720, step=30
    )
    prazo_meses = prazo_dias // 30
with col_param3:
    cdi_atual = st.number_input(
        "CDI atual (% a.a.)", min_value=0.1, max_value=30.0, value=10.75, step=0.25, format="%.2f"
    )
    ipca_atual = st.number_input(
        "IPCA atual (% a.a.)", min_value=0.0, max_value=20.0, value=4.5, step=0.1, format="%.1f"
    )

st.markdown("---")

# Simulação comparativa
st.header("📊 Compare até 3 Investimentos")

# Prazos mínimos/máximos por produto
prazos_min_max = {
    'CDB': (30, 7200),
    'LCI': (90, 7200),
    'LCA': (90, 7200)
}

investimentos = []
for i in range(3):
    with st.expander(f"💼 Investimento {i+1}", expanded=(i < 2)):
        col_inv1, col_inv2, col_inv3, col_inv4, col_inv5 = st.columns(5)
        with col_inv1:
            tipo = st.selectbox(
                "Tipo", ["CDB", "LCI", "LCA"], key=f"tipo_{i}"
            )
            min_prazo, max_prazo = prazos_min_max[tipo]
            st.info(f'Prazo disponível para {tipo}: mínimo {min_prazo} dias, máximo {max_prazo} dias.')
            if prazo_dias < min_prazo:
                st.warning(f'O prazo mínimo para {tipo} é {min_prazo} dias.')
        with col_inv2:
            tipo_rent = st.selectbox(
                "Rentabilidade", ["Prefixada", "Pós-fixada (% CDI)", "Híbrida (IPCA + %)"], key=f"rent_{i}"
            )
        with col_inv3:
            if tipo_rent == "Prefixada":
                taxa = st.number_input(
                    "Taxa (% a.a.)", min_value=0.1, max_value=50.0, value=11.0, step=0.1, key=f"taxa_{i}"
                )
            elif tipo_rent == "Pós-fixada (% CDI)":
                taxa = st.number_input(
                    "% do CDI", min_value=50.0, max_value=150.0, value=105.0, step=1.0, key=f"taxa_{i}"
                )
            else:
                taxa = st.number_input(
                    "Taxa adicional (% a.a.)", min_value=0.0, max_value=20.0, value=5.0, step=0.1, key=f"taxa_{i}"
                )
        # Checkbox para isenção de IR em LCI/LCA
        with col_inv4:
            if tipo in ['LCI', 'LCA']:
                is_isenta = st.checkbox('Isenta de IR?', value=True, key=f'isenta_{i}')
            else:
                is_isenta = True
        with col_inv5:
            ativo = st.checkbox(
                "Incluir na comparação", value=(i < 2), key=f"ativo_{i}"
            )

        if ativo:
            rent_mensal = calcular_rentabilidade_mensal(tipo_rent, taxa, cdi_atual, ipca_atual)
            saldos, bruto, liquido, ir, prazo_meses_calc = simular_investimento(
                valor_inicial, aporte_mensal, prazo_dias, rent_mensal, tipo, is_isenta
            )
            total_investido = valor_inicial + (aporte_mensal * prazo_meses_calc)
            if prazo_meses_calc > 0:
                rent_liquida_anual = ((liquido / total_investido) ** (12/prazo_meses_calc) - 1) * 100
            else:
                rent_liquida_anual = 0

            investimentos.append({
                'nome': f"{tipo} - {tipo_rent}",
                'tipo': tipo,
                'tipo_rentabilidade': tipo_rent,
                'taxa': taxa,
                'saldos': saldos,
                'bruto': bruto,
                'liquido': liquido,
                'ir': ir,
                'rent_liquida_anual': rent_liquida_anual,
                'total_investido': total_investido
            })

# Resultados
if investimentos:
    st.markdown("---")
    st.header("📈 Resultados da Simulação")
    melhor = max(investimentos, key=lambda x: x['liquido'])

    st.subheader("📋 Resumo Comparativo")
    dados_tabela = []
    for inv in investimentos:
        rendimento_liquido = inv['liquido'] - inv['total_investido']
        dados_tabela.append({
            'Investimento': inv['nome'],
            'Tipo': inv['tipo'],
            'Taxa': f"{inv['taxa']:.1f}%",
            'Total Investido': f"R$ {inv['total_investido']:,.2f}",
            'Valor Bruto': f"R$ {inv['bruto']:,.2f}",
            'IR Devido': f"R$ {inv['ir']:,.2f}",
            'Valor Líquido': f"R$ {inv['liquido']:,.2f}",
            'Rendimento Líquido': f"R$ {rendimento_liquido:,.2f}",
            'Rentabilidade Anual': f"{inv['rent_liquida_anual']:.2f}% a.a."
        })
    df_resultado = pd.DataFrame(dados_tabela)

    def highlight_melhor(s):
        melhor_valor = max([float(inv['liquido']) for inv in investimentos])
        is_melhor = s['Valor Líquido'] == f"R$ {melhor_valor:,.2f}"
        return ['background-color: lightgreen' if is_melhor else '' for _ in s]

    st.dataframe(
        df_resultado.style.apply(highlight_melhor, axis=1),
        use_container_width=True
    )

    st.subheader("📊 Evolução dos Investimentos")
    fig = go.Figure()
    prazo_meses_grafico = prazo_dias // 30
    meses = list(range(prazo_meses_grafico + 1))

    for inv in investimentos:
        fig.add_trace(go.Scatter(
            x=meses,
            y=inv['saldos'],
            mode='lines+markers',
            name=inv['nome'],
            line=dict(width=3)
        ))

    fig.update_layout(
        title="Evolução do Saldo ao Longo do Tempo",
        xaxis_title="Meses",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        height=500
    )
    fig.update_layout(yaxis=dict(tickformat=",.0f"))
    st.plotly_chart(fig, use_container_width=True)

    col_destaque1, col_destaque2 = st.columns(2)
    with col_destaque1:
        st.success(f"""
        🏆 **MELHOR OPÇÃO** **{melhor['nome']}**
        Valor final: R$ {melhor['liquido']:.2f}
        Rendimento: R$ {melhor['liquido'] - melhor['total_investido']:.2f}
        Rentabilidade: {melhor['rent_liquida_anual']:.2f}% a.a.
        """)
    with col_destaque2:
        if len(investimentos) > 1:
            investimentos_ord = sorted(investimentos, key=lambda x: x['liquido'], reverse=True)
            diferenca = investimentos_ord[0]['liquido'] - investimentos_ord[1]['liquido']
            st.info(f"""
            💡 **COMPARAÇÃO**
            A melhor opção rende **R$ {diferenca:,.2f}** a mais que a segunda melhor.
            Isso representa uma diferença de **{(diferenca/investimentos_ord[1]['liquido']*100):.1f}%** no valor final.
            """)

st.markdown("---")
st.header("ℹ️ Informações Importantes")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info("""
    **Premissas da Simulação:**
    • CDI e IPCA permanecem constantes durante todo o período
    • Aportes mensais são feitos no início de cada mês
    • IR calculado apenas sobre rendimentos (CDB e LCI/LCA não isentas)
    • Não considera IOF (aplicável apenas para resgates em menos de 30 dias)
    """)
with col_info2:
    st.warning("""
    **Atenção:**
    • Esta é uma simulação educativa
    • Rentabilidades passadas não garantem resultados futuros
    • Considere sempre sua estratégia e perfil de risco
    • Consulte um profissional qualificado para decisões de investimento
    """)

st.markdown("---")
