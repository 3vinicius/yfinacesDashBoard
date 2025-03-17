from matplotlib.pyplot import title
import streamlit as st
import pandas as pd
from sympy import I, Interval
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime




st.set_page_config(layout="wide")



col1= st.columns(1)[0] 
result = "PETR3.SA"
col1.title(result)
st.divider()

col1,col2 = st.columns(2) 

valid_interval = []

tickers_list = [
    "PETR3.SA", "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA",
    "BBDC3.SA", "BBDC4.SA", "ABEV3.SA", "WEGE3.SA", "SUZB3.SA",
    "EQTL3.SA", "RADL3.SA", "GGBR4.SA", "LREN3.SA", "VIVT3.SA",
    "CSNA3.SA", "HAPV3.SA", "NTCO3.SA", "RENT3.SA", "RDOR3.SA",
    "MXRF11.SA", "XPML11.SA", "BTLG11.SA", "HGLG11.SA", "TRXF11.SA"
]




result = st.sidebar.selectbox("Escolha um ticker", tickers_list)


def transformaMinutos(data):
  return data.minute + (60*data.hour)



acao = yf.Ticker(result)



valid_ranges = ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
valid_interval = ["5d", "1wk", "1mo", "3mo"]


periodo = st.sidebar.select_slider(
    "Periodo",
    options=valid_ranges,
    value="1y"
)
interval = st.sidebar.select_slider(
    "Periodo",
    options=valid_interval,
    value="1wk"
)


df = acao.history(period=periodo,interval=interval)


newDf = df.reset_index()


fig = go.Figure(data=[go.Candlestick(x=newDf['Date'],
                open=newDf['Open'],
                high=newDf['High'],
                low=newDf['Low'],
                close=newDf['Close'])])

st.plotly_chart(fig)


df_opCl = df.filter(['Open', 'Close'])

df_reset_opC = df.reset_index()

fig = px.line(df_reset_opC, x='Date', y=['Open', 'Close'], title="Preços de Abertura e Fechamento")
fig.update_traces(line=dict(color='red'), selector=dict(name='Close')) 

col1.plotly_chart(fig)



df_volume = df.filter(['Open', 'High', 'Low', 'Close', 'Volume']).reset_index()


media_volume = df['Volume'].mean()


fig = px.line(df_volume, x='Date', y='Volume', title="Volume de Negócios ao Longo do Tempo", 
              line_shape="linear")  


fig.update_traces(line=dict(color='blue'))


fig.add_hline(y=media_volume, line=dict(color='red', dash='dash'), 
              annotation_text=f'Média Volume: {media_volume:.2f}', 
              annotation_position="top right")


col2.plotly_chart(fig)


st.divider()

divRes = acao.dividends.reset_index()
media_dividendos = divRes['Dividends'].mean()
fig = px.line(divRes, x='Date', y="Dividends")
st.header("Dividendos")
fig.add_hline(y=media_dividendos , line=dict(color='red', dash='dash'), 
              annotation_text=f'Média Dividendos: {media_dividendos :.2f}', 
              annotation_position="top right")

st.plotly_chart(fig)

st.divider()

st.header("Preços dos Analistas")

col1, col2, col3,col4,col5 = st.columns(5)
col1.metric("Atual", round(acao.analyst_price_targets["current"],2), round(acao.analyst_price_targets["current"] - acao.analyst_price_targets["median"],2))
col2.metric("Alto", round(acao.analyst_price_targets["high"],2), round(acao.analyst_price_targets["high"] - acao.analyst_price_targets["median"],2))
col3.metric("Baixo", round(acao.analyst_price_targets["low"],2) , round(acao.analyst_price_targets["low"] - acao.analyst_price_targets["median"],2))
col4.metric("media", round(acao.analyst_price_targets["mean"],2))
col5.metric("meidana", round(acao.analyst_price_targets["median"],2))

st.divider()


col1, col2 = st.columns(2)

data = acao.calendar

col2.markdown("### Detalhes dos Resultados Financeiros:")

col2.markdown(f"**Ex-Dividend Date:** {data['Ex-Dividend Date']}")

earnings_date_str = ", ".join([str(date) for date in data["Earnings Date"]])
col2.markdown(f"**Earnings Date(s):** {earnings_date_str}")

col2.markdown(f"**Earnings High:** {data['Earnings High'] if data['Earnings High'] else 'N/A'}")
col2.markdown(f"**Earnings Low:** {data['Earnings Low'] if data['Earnings Low'] else 'N/A'}")
col2.markdown(f"**Earnings Average:** {data['Earnings Average'] if data['Earnings Average'] else 'N/A'}")

col2.markdown(f"**Revenue High:** ${data['Revenue High']:,}")
col2.markdown(f"**Revenue Low:** ${data['Revenue Low']:,}")
col2.markdown(f"**Revenue Average:** ${data['Revenue Average']:,}")

st.divider()





col1.header("Balanço")


def format_currency(val):
  if isinstance(val, (int, float)):
      return f"${val:,.2f}"
  return val

df_formatted = pd.DataFrame(acao.balance_sheet)
df_formatted.fillna(0, inplace=True)
df_formatted = df_formatted.applymap(format_currency)

col1.dataframe(df_formatted)

@st.dialog("Sumario")
def vote():

  st.title("Análise do Balanço Patrimonial")


  st.markdown("""
  <style>
      .big-font {
          font-size: 22px !important;
          color: #2c3e50;
          font-weight: bold;
      }
      .section-header {
          font-size: 18px;
          color: #2980b9;
          font-weight: bold;
      }
      .item-title {
          font-size: 16px;
          color: #8e44ad;
          font-weight: bold;
      }
      .item-description {
          font-size: 14px;
          color: #34495e;
      }
  </style>
  """, unsafe_allow_html=True)


  st.header("Ativos (Assets)")


  with st.expander("Ativos Circulantes"):
      st.markdown("<p class='item-title'>Contas a Receber (Accounts Receivable)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Valor que a empresa tem a receber de clientes, como vendas a crédito.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Ativos para Venda Correntes (Assets Held for Sale Current)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Ativos que a empresa pretende vender no curto prazo.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Títulos Disponíveis para Venda (Available for Sale Securities)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Investimentos em ações ou títulos que podem ser vendidos ou comprados, mas que não são mantidos até o vencimento.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Caixa e Equivalentes de Caixa (Cash and Cash Equivalents)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dinheiro disponível e ativos que podem ser rapidamente convertidos em dinheiro, como depósitos bancários.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Inventário (Inventory)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Produtos e matérias-primas armazenados para venda ou uso na produção.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Ativos Imobiliários Líquidos (Net PPE)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Valor de bens tangíveis, como propriedades e equipamentos, menos a depreciação acumulada.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Produtos Acabados (Finished Goods)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Produtos que foram fabricados e estão prontos para serem vendidos.</p>", unsafe_allow_html=True)

  with st.expander("Ativos Não Circulantes"):
      st.markdown("<p class='item-title'>Ativos Totais (Total Assets)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>O total de todos os ativos da empresa, tanto circulantes quanto não circulantes.</p>", unsafe_allow_html=True)

  st.header("Passivos (Liabilities)")


  with st.expander("Passivos Circulantes"):
      st.markdown("<p class='item-title'>Contas a Pagar (Accounts Payable)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dívidas que a empresa tem com fornecedores ou prestadores de serviços.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Dívida Corrente (Current Debt)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dívidas que precisam ser pagas no curto prazo.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Dividendos a Pagar (Dividends Payable)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dividendos que foram declarados, mas ainda não pagos aos acionistas.</p>", unsafe_allow_html=True)

  with st.expander("Passivos de Longo Prazo"):
      st.markdown("<p class='item-title'>Dívida de Longo Prazo (Long Term Debt)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dívidas que precisam ser pagas após 12 meses.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Provisões de Longo Prazo (Long Term Provisions)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Reservas financeiras para cobrir despesas futuras.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Obrigações de Arrendamento Mercantil de Longo Prazo (Long Term Capital Lease Obligation)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Dívidas de arrendamento que vencem após 12 meses.</p>", unsafe_allow_html=True)


  st.header("Patrimônio Líquido (Equity)")

  with st.expander("Capital Social e Ações"):
      st.markdown("<p class='item-title'>Capital Social (Capital Stock)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>O valor total investido pelos acionistas na empresa.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Ações Ordinárias (Common Stock)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Ações que conferem direito de voto aos acionistas.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Ações Preferenciais (Preferred Shares Number)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Ações preferenciais, que geralmente oferecem prioridade no pagamento de dividendos, mas sem direito de voto.</p>", unsafe_allow_html=True)

  with st.expander("Outros Termos Relevantes"):
      st.markdown("<p class='item-title'>Ágio (Goodwill)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>O valor pago por uma empresa além do valor de mercado dos ativos adquiridos, geralmente associado à marca, reputação ou rede de clientes.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Capital Investido (Invested Capital)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>O total de capital que foi investido na empresa, seja por acionistas ou por financiadores.</p>", unsafe_allow_html=True)

      st.markdown("<p class='item-title'>Arrendamentos (Leases)</p>", unsafe_allow_html=True)
      st.markdown("<p class='item-description'>Contratos de arrendamento de bens móveis ou imóveis.</p>", unsafe_allow_html=True)
    

if "vote" not in st.session_state:
    if col1.button("Sumario"):
        vote()
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"



