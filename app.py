import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# 1. Configuração do App no Streamlit
st.title("🤖 Classificador de Sentimento de Prompts")
st.write(
    "Exemplo simples de IA para prever se a intenção de um texto é Positiva ou"
    " Negativa."
)

# 2. Dicionário de Dados (Base de Treinamento)
# Prompts de exemplo e seus rótulos: 1 = Positivo, 0 = Negativo
dados_prompts = {
    "texto": [
        "Adorei o resultado da resposta",
        "Código excelente e explicativo",
        "Ótima explicação do modelo",
        "A resposta está horrível",
        "Código com erro e sem explicação",
        "Resultado péssimo e confuso",
    ],
    "sentimento": [1, 1, 1, 0, 0, 0],
}

df = pd.DataFrame(dados_prompts)

# 3. Processamento de Texto Simples (Bag of Words)
# Mapeamos palavras-chave para criar a entrada da rede neural
palavras_chave = ["adorei", "excelente", "ótima", "horrível", "erro", "péssimo"]


def vetorizar_texto(texto):
  texto_lower = texto.lower()
  return [1.0 if palavra in texto_lower else 0.0 for palavra in palavras_chave]


X = np.array([vetorizar_texto(t) for t in df["texto"]])
y = np.array(df["sentimento"], dtype=float)

# 4. Construção e Treinamento da Rede Neural com TensorFlow
# Modelo de classificação binária com 1 neurônio e ativação Sigmoid
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[len(palavras_chave)], activation="sigmoid")
])

model.compile(
    optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
)

with st.spinner("Treinando a rede neural..."):
  model.fit(X, y, epochs=500, verbose=0)

# 5. Interface para Teste do Usuário
st.subheader("💬 Teste um Prompt")
prompt_usuario = st.text_input(
    "Digite uma mensagem para a IA analisar:",
    "Código excelente e muito explicativo",
)

if prompt_usuario:
  vetor_entrada = np.array([vetorizar_texto(prompt_usuario)])
  probabilidade = model.predict(vetor_entrada, verbose=0)[0][0]

  st.write("---")
  if probabilidade >= 0.5:
    st.success(f"😊 **Sentimento Positivo** (Confiança: {probabilidade * 100:.1f}%)")
  else:
    st.error(
        f"🙁 **Sentimento Negativo** (Confiança: {(1 - probabilidade) * 100:.1f}%)"
    )

# 6. Exibição da Base de Dados
st.subheader("📊 Base de Dados Utilizada")
st.dataframe(df)