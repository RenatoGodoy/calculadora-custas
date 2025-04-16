import streamlit as st

# --------------------------
# Função de cálculo para o TJ/RJ
# --------------------------
def calcular_custas_rj(valor_causa):
    # Faixa fixa simulada com base no print enviado
    if valor_causa <= 20000:
        taxa_judiciaria = 820.56
    else:
        taxa_judiciaria = 820.56  # Até termos faixas superiores

    # Fundos obrigatórios
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
# Função genérica para SP e PR
# --------------------------
def calcular_custas(uf, tipo_acao, tipo_recurso, valor_causa, gratuidade=False, parte_isenta=False):
    if gratuidade:
        return "✅ Justiça gratuita concedida. Sem custas recursais."

    if parte_isenta:
        return "✅ Parte isenta de custas (MP, Fazenda, Defensoria etc.)."

    if uf == 'RJ' and tipo_acao == 'Cível' and tipo_recurso == 'Apelação':
        return calcular_custas_rj(valor_causa)

    regras = {
        'SP': {
            'Cível': {
                'Apelação': {
                    'percentual': 0.03,
                    'valor_minimo': 87.55,
                    'unidade': 'Real'
                }
            }
        },
        'PR': {
            'Cível': {
                'Apelação': {
                    'percentual': 0.02,
                    'valor_minimo': 94.60,
                    'unidade': 'Real'
                }
            }
        }
    }

    try:
        regra = regras[uf][tipo_acao][tipo_recurso]
        if 'percentual' in regra:
            valor = max(valor_causa * regra['percentual'], regra['valor_minimo'])
            return f"💰 Custas: R$ {valor:.2f} ({regra['percentual']*100:.1f}% sobre R$ {valor_causa:.2f})"
    except KeyError:
        return "❌ Não há regra cadastrada para essa combinação de UF, ação e recurso."


# --------------------------
# Interface Streamlit
# --------------------------
st.set_page_config(page_title="Calculadora de Custas Recursais", layout="centered")
st.title("🧮 Calculadora de Custas Recursais")

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
    else:
        st.success(resultado)
