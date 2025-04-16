import streamlit as st

# --------------------------
# Cálculo detalhado para TJ/RJ
# --------------------------
def calcular_custas_rj(valor_causa):
    if valor_causa <= 20000:
        taxa_judiciaria = 820.56
    else:
        taxa_judiciaria = 820.56  # Valor fixo temporário

    fundperj = round(taxa_judiciaria * 0.05, 2)
    funperj = round(taxa_judiciaria * 0.05, 2)
    funarpen = round(taxa_judiciaria * 0.06, 2)

    total = round(taxa_judiciaria + fundperj + funperj + funarpen, 2)

    return {
        "Atos Sec. TJ": taxa_judiciaria,
        "FUNDPERJ": fundperj,
        "FUNPERJ": funperj,
        "FUNARPEN": funarpen,
        "TOTAL": total
    }

# --------------------------
# Faixas oficiais TJ/SP (2024)
# --------------------------
def calcular_custas_sp(valor_causa):
    if valor_causa <= 26640.00:
        custas = valor_causa * 0.02
    elif valor_causa <= 88800.00:
        custas = valor_causa * 0.015
    else:
        custas = valor_causa * 0.01

    return round(max(custas, 87.55), 2)

# --------------------------
# Cálculo genérico
# --------------------------
def calcular_custas(uf, tipo_acao, tipo_recurso, valor_causa, gratuidade=False, parte_isenta=False):
    if gratuidade:
        return "✅ Justiça gratuita concedida. Sem custas recursais."
    if parte_isenta:
        return "✅ Parte isenta de custas (MP, Fazenda, Defensoria etc.)."

    if uf == 'RJ' and tipo_acao == 'Cível' and tipo_recurso == 'Apelação':
        return calcular_custas_rj(valor_causa)

    if uf == 'SP' and tipo_acao == 'Cível' and tipo_recurso == 'Apelação':
        custas = calcular_custas_sp(valor_causa)
        return f"💰 Custas: R$ {custas:.2f} (base TJ/SP)"

    # Exemplo básico para PR
    if uf == 'PR':
        custas = max(valor_causa * 0.02, 94.60)
        return f"💰 Custas: R$ {custas:.2f} (base TJ/PR)"

    return "❌ Não há regra cadastrada para essa combinação."

# --------------------------
# Interface do App
# --------------------------
st.set_page_config(page_title="Calculadora de Custas Recursais", layout="centered")
st.title("🧮 Calculadora de Custas Recursais")

# Botão para reiniciar tudo
if st.button("🔄 Novo Cálculo"):
    st.session_state.clear()
    st.experimental_rerun()

ufs = ['RJ', 'SP', 'PR']
tipos_acao = ['Cível']
tipos_recurso = ['Apelação']

uf = st.selectbox("🗺️ Estado (UF):", ufs)
tipo_acao = st.selectbox("📄 Tipo de Ação:", tipos_acao)
tipo_recurso = st.selectbox("📌 Tipo de Recurso:", tipos_recurso)
valor_causa = st.number_input("💰 Valor da Causa (R$):", min_value=0.0, step=100.0)

justica_gratuita = st.checkbox("✅ Justiça Gratuita", key="chk_gratuita")
parte_isenta = st.checkbox("🏛️ Parte Isenta (MP, Fazenda Pública, Defensoria)", key="chk_isenta")

if st.button("Calcular Custas"):
    resultado = calcular_custas(uf, tipo_acao, tipo_recurso, valor_causa, justica_gratuita, parte_isenta)

    if isinstance(resultado, dict):
        st.success(f"💰 Custas totais: R$ {resultado['TOTAL']:.2f}")
        st.markdown("### 📄 Detalhamento:")
        st.write(f"🔹 Atos Sec. TJ: R$ {resultado['Atos Sec. TJ']:.2f}")
        st.write(f"🔹 FUNDPERJ: R$ {resultado['FUNDPERJ']:.2f}")
        st.write(f"🔹 FUNPERJ: R$ {resultado['FUNPERJ']:.2f}")
        st.write(f"🔹 FUNARPEN: R$ {resultado['FUNARPEN']:.2f}")
    elif isinstance(resultado, str):
        st.success(resultado)
    else:
        st.warning("❌ Erro ao calcular as custas. Verifique os dados.")


