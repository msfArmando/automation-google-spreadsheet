from dotenv import load_dotenv
import os
import pandas as pd
from datetime import date, datetime
import gspread
import time
import streamlit as st
import string
import random
import plotly.express as px
import pyodbc
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from zoneinfo import ZoneInfo

if 'secs_count' not in st.session_state:
    #st.session_state.secs_count = 86400
    st.session_state.secs_count = 10
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

def main():
    driver = os.getenv('driver')
    host = os.getenv('host')
    port = os.getenv('port')
    service = os.getenv('service')
    UID = os.getenv('UID')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    connect_string = f'DRIVER={driver};DBQ={host}:{port}/{service};UID={UID};PWD={DB_PASSWORD};'

    conn = pyodbc.connect(connect_string)
    
    st.set_page_config(page_title="Monitoramento - Google Sheets Vendas", layout="wide")

    def set_metric_font_size(label_size, value_size):
        st.markdown(
            f"""
            <style>
                [data-testid="stMetricLabel"] p {{
                    font-size: {label_size} !important;
                }}
                [data-testid="stMetricValue"] p {{
                    font-size: {value_size} !important;
                }}
            </style>
            """,
            unsafe_allow_html=True,
    )

    col1, col2 = st.columns([4.5, 1])

    with col1:
        placeholder_title = st.empty()
    with col2:
        placeholder_logo = st.empty()
    
    placeholder_title.title("Monitoramento - Google Sheets Vendas")
    placeholder_logo.image("assets/LOGOGOD.png")

    today = date.today()
    
    st.divider()

    col4, col5 = st.columns([1, 2], vertical_alignment='top')

    with col4:
        placeholder = st.empty()

    with col5:
        placeholder_chart = st.empty()
    
    exec_df = pd.read_csv('execs.csv')
    exec_df.columns = ['ID_EXEC', 'DATA_EXEC', 'STATUS_EXEC']

    exec_df['DATA_EXEC'] = pd.to_datetime(exec_df['DATA_EXEC'], format='mixed', dayfirst=True)

    exec_df = exec_df.sort_values('DATA_EXEC')

    exec_df['DATA_EXEC_STR'] = exec_df['DATA_EXEC'].dt.strftime('%m/%Y')

    exec_df_group = exec_df.groupby(exec_df['DATA_EXEC'].dt.strftime('%d/%m/%Y')).size().reset_index(name='QTD_EXEC')
    
    exec_df_group.rename(columns={'DATA_EXEC': 'DATA_EXEC_BR'}, inplace=True)


    fig = px.scatter(
        exec_df, 
        x='DATA_EXEC_STR', 
        y='STATUS_EXEC',
        color='STATUS_EXEC',
        symbol='STATUS_EXEC',
        size=[15] * len(exec_df), 
        title='Histórico de Execuções Mensais',
        labels={'DATA_EXEC_STR': 'Mês de Referência', 'STATUS_EXEC': 'Resultado'},
        color_discrete_map={'Sucesso': 'green', 'Erro': 'red'}, 
        template='plotly_white'
    )
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))

    placeholder_chart.plotly_chart(fig)

    while True:
        mins, secs = divmod(st.session_state.secs_count, 60)
        horas, mins = divmod(mins, 60)

        timer = '{:02d}:{:02d}:{:02d}'.format(horas, mins, secs)
        timer_str = str(timer)
        placeholder.empty()
        set_metric_font_size(label_size="20px", value_size="50px")
        placeholder.metric("Próxima atualização em", timer_str)

        if st.session_state.secs_count == 0:
            if today.day == 2:
                
                with placeholder.status("Atualizando base de dados...", expanded=True) as status:
                    def load_data(file_name):
                        st.write("Carregando dados...")
                        with open(f"/app/secrets/{file_name}.sql", "r") as f:
                            query_main = f.read()
                            query = query_main
                            df = pd.read_sql(query, conn)

                            return df
                    
                    df = load_data("query1")

                    df_sheet = pd.DataFrame(df)

                    fuso_brasil = ZoneInfo("America/Sao_Paulo")
                    agora_brasil = datetime.now(fuso_brasil)

                    mes_var_atual = ''
                    mes_var_anterior = ''

                    if agora_brasil.month == 1:
                        mes_var_atual = 'TOTAL_DEZEMBRO'
                        mes_var_anterior = 'TOTAL_NOVEMBRO'
                    elif agora_brasil.month == 2:
                        mes_var_atual = 'TOTAL_JANEIRO'
                        mes_var_anterior = 'TOTAL_DEZEMBRO'
                    elif agora_brasil.month == 3:
                        mes_var_atual = 'TOTAL_FEVEREIRO'
                        mes_var_anterior = 'TOTAL_JANEIRO'
                    elif agora_brasil.month == 4:
                        mes_var_atual = 'TOTAL_MARCO'
                        mes_var_anterior = 'TOTAL_FEVEREIRO'
                    elif agora_brasil.month == 5:
                        mes_var_atual = 'TOTAL_ABRIL'
                        mes_var_anterior = 'TOTAL_MARCO'
                    elif agora_brasil.month == 6:
                        mes_var_atual = 'TOTAL_MAIO'
                        mes_var_anterior = 'TOTAL_ABRIL'
                    elif agora_brasil.month == 7:
                        mes_var_atual = 'TOTAL_JUNHO'
                        mes_var_anterior = 'TOTAL_MAIO'
                    elif agora_brasil.month == 8:
                        mes_var_atual = 'TOTAL_JULHO'
                        mes_var_anterior = 'TOTAL_JUNHO'
                    elif agora_brasil.month == 9:
                        mes_var_atual = 'TOTAL_AGOSTO'
                        mes_var_anterior = 'TOTAL_JULHO'
                    elif agora_brasil.month == 10:
                        mes_var_atual = 'TOTAL_SETEMBRO'
                        mes_var_anterior = 'TOTAL_AGOSTO'
                    elif agora_brasil.month == 11:
                        mes_var_atual = 'TOTAL_OUTUBRO'
                        mes_var_anterior = 'TOTAL_SETEMBRO'
                    elif agora_brasil.month == 12:
                        mes_var_atual = 'TOTAL_NOVEMBRO'
                        mes_var_anterior = 'TOTAL_OUTUBRO'

                    #Renommear colunas com nome do mes correto dinamico
                    df_sheet.rename(columns={'TOTAL_MES_ANTE_ANTERIOR': mes_var_anterior, 'TOTAL_MES_ANTERIOR': mes_var_atual}, inplace=True)

                    st.write("Conectando ao Google Sheets...")

                    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

                    def obter_credenciais():
                        creds = None
                        if os.path.exists('token.json'):
                            creds = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
                            
                        if not creds or not creds.valid:
                            if creds and creds.expired and creds.refresh_token:
                                creds.refresh(Request())
                            else:
                                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=SCOPES)
                                creds = flow.run_local_server(port=0)
                                
                            with open('token.json', 'w') as token:
                                token.write(creds.to_json())
                                
                        return creds

                    creds = obter_credenciais()

                    gc = gspread.authorize(creds)

                    # Preencha a variável com o id da planilha do sheets
                    spreadsheet_id = ''
                    sh = gc.open_by_key(spreadsheet_id)

                    worksheet_usicoda = sh.worksheet("TOP 20 VENDAS")
                    
                    st.write("Limpando planilha...")
                    worksheet_usicoda.clear()
                    st.write("Inserindo dados na planilha...")
                    worksheet_usicoda.update([df_sheet.columns.values.tolist()] + df_sheet.values.tolist())
                    worksheet_usicoda.format("1", {"textFormat": {"bold": True}})

                    status.update(
                        label="Base de dados atualizada!", state="complete", expanded=False
                    )
                    
                    caracteres = string.ascii_letters + string.digits
                    exec_id = ''.join(random.choices(caracteres, k=4))
                    exec_data = {
                        'id': exec_id,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status' : 'Sucesso'
                    }

                    new_df = pd.DataFrame([exec_data])

                    file = 'execs.csv'

                    file_exists = os.path.isfile(file)
                                                    
                    new_df.to_csv(file,
                                  mode='a',
                                  index=False,
                                  header=not file_exists,
                                  encoding='utf-8')
                    pass
            st.session_state.secs_count = 86400  
        else:
            time.sleep(1)
            st.session_state.secs_count -= 1
            st.rerun()

if __name__ == "__main__":
    main()