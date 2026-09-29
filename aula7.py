import streamlit as st
import re
from collections import Counter

# Configuração da página do Streamlit
st.set_page_config(page_title="Análise de Reclamções", page_icon="📊", layout="centered")

st.title("📊 Analisador de Reclamações de Clientes")
st.write("Insira as reclamações abaixo para identificar as palavras mais frequentes.")

# Área de texto para o analista colar as reclamações
texto_usuario = st.text_area(
    "Cole aqui as reclamações (uma por linha):",
    value="O aplicativo está muito lento e trava toda hora.\nNão consigo atualizar o aplicativo. O app trava.\nO serviço é muito lento.",
    height=200
)

# Seletor interativo para a quantidade de palavras no ranking
top_n = st.slider("Quantidade de palavras no ranking:", min_value=3, max_value=10, value=5)

def analisar_palavras_frequentes(texto, top_n):
    texto_completo = texto.lower()
    texto_limpo = re.sub(r'[^\w\s]', '', texto_completo)
    palavras = texto_limpo.split()
    
    stopwords = {'o', 'a', 'os', 'as', 'e', 'do', 'da', 'em', 'no', 'na', 'de', 'para', 'com', 'muito', 'quando', 'toda', 'que', 'está'}
    palavras_filtradas = [p for p in palavras if p not in stopwords and len(p) > 2]
    
    contador = Counter(palavras_filtradas)
    return contador.most_common(top_n)

if st.button("Analisar Palavras"):
    if texto_usuario.strip():
        resultado = analisar_palavras_frequentes(texto_usuario, top_n)
        
        st.subheader(f"🏆 Top {top_n} Palavras Mais Frequentes")
        
        # Exibe os resultados em formato de lista visual
        for posicao, (palavra, frequencia) in enumerate(resultado, start=1):
            st.write(f"**{posicao}º Lugar:** `{palavra}` — Aparece **{frequencia}** vezes")
    else:
        st.warning("Por favor, digite ou cole alguma reclamação para analisar.")
