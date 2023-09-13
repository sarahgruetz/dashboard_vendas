import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
    sucesso = st.sucesso('Arquivo baixado com sucesso!', icon = "✅")
    time.sleep(5)
    sucesso.empty()

st.set_page_config(layout = 'wide', page_title = 'Dashboard de vendas', page_icon = ':dart:')

st.title('DADOS BRUTOS :spiral_note_pad:')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produto = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Frete da compra'):
    frete = st.slider('Selecione o frete', 0, 250, (0,250))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecine a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    local = st.multiselect('Selecione os locais', dados['Local da compra'].unique(), dados['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação', 0, 5, (0,5))
with st.sidebar.expander('Tipo de pagamento'):
    pagamento = st.multiselect('Selecione os tipos de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    parcela = st.slider('Selecione a quantidade de parcelas', 0, 24, (0,24))

query = """
Produto in @produto and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local and \
@avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @pagamento and \
@parcela[0] <= `Quantidade de parcelas` <= @parcela[1]
"""

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo')
col1,col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)