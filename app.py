import streamlit as st

def calcular_custas(uf, tipo_acao, tipo_recurso, valor_causa, gratuidade=False, parte_isenta=False):
    # Base de regras simplificada para SP, RJ e PR
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
        'RJ': {
            'Cível': {
                'Apelação': {
                    'valor_fixo': 284.82,
                    'unidade': 'UFERJ',
                    'conversao_hoje': 4.656  # valor fictício para exemplo
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

    if gratuidade:
        return "✅ Justiça gratuita concedida. Sem custas recursais."

    if parte_isenta:
        return "✅ Parte isenta de custas (MP, Fazenda, Defensoria etc.)."

    try:
        regra = regras[uf][tipo_acao][tipo_recurso]
        
        if 'valor_fixo' in regra:
            valor = regra['valor_fixo']
            if regra['unidade'] != 'Real':
                valor *= regra.get('conversao_hoje', 1)
            return f"💰 Custas: R$ {valor:.2f} ({regra['unidade']})"

        elif 'percentual' in regra:
            valor = max(valor_causa * regra['percentual'], regra['valor_minimo'])
            return f"💰 Custas: R$ {valor:.2f} ({regra['percentual']*100:.1f}% sobre R$ {valor_causa:.2f})"

        else:
            return "⚠️ Regra de cálculo não encontrada."

    except KeyError:
        return "❌ Não há regra cadastrada para essa combinação de UF, ação e recurso."


# Streamlit app
st.title("Calculadora de Custas Recursais")

ufs = ['SP', 'RJ', 'PR']
tipos_acao = ['Cível']
tipos_recurso = ['Apelação']

uf = st.selectbox("Selecione o Estado (UF):", ufs)
tipo_acao = st.selectbox("Tipo de Ação:", tipos_acao)
tipo_recurso = st.selectbox("Tipo de Recurso:", tipos_recurso)
valor_causa = st.number_input("Valor da Causa (R$):", min_value=0.0, step=100.0)
justica_gratuita = st.checkbox("✅ Justiça Gratuita", key="justica_gratuita")
parte_isenta = st.checkbox("🏛️ Parte Isenta (MP, Fazenda Pública, Defensoria)", key="parte_isenta")

if st.button("Calcular Custas"):
    resultado = calcular_custas(uf, tipo_acao, tipo_recurso, valor_causa, gratuidade, parte_isenta)
    st.success(resultado)
