import streamlit as st
import data
import plotly.express as px
import pandas as pd
import datetime
import logging



st.set_page_config(
    # page_title="PE Score Analysis App",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    )


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s,%(message)s")

teams = ['イタリア', 'フランス', 'ドイツ', 'ポルトガル', 'アルゼンチン', 'ブラジル', 'イングランド',
    'ウクライナ', 'スペイン', 'エクアドル', 'メキシコ', 'オーストラリア', 'スイス', 'ガーナ',
    'スウェーデン', 'オランダ', 'コートジボアール', 'コスタリカ', 'チェコ', '韓国', 'チュニジア',
    'サウジアラビア', 'ポーランド', 'イラン', '日本', 'セルビア モンテネグロ', 'クロアチア', 'アンゴラ',
    'パラグアイ', 'トーゴ', 'アメリカ', 'トリニダードトバコ']


# Streamlit runs from top to bottom on every iteraction so
# we check if `count` has already been initialized in st.session_state.

def main():
    # # If username is already initialized, don't do anything
    if 'username' not in st.session_state or st.session_state.username == 'default':
        st.session_state.username = 'default'
        input_name()
        st.stop()
            
    if 'page' not in st.session_state:
        st.session_state.page = 'input_name'


    # --- page選択ラジオボタン
    page = st.sidebar.radio('ページ選択', ('データ加工', 'データ可視化'))
    if page == 'データ加工':
        st.session_state.page = 'deal_data'
        logging.info(',%s,ページ選択,%s', st.session_state.username, page)
    elif page == 'データ可視化':
        st.session_state.page = 'vis'
        logging.info(',%s,ページ選択,%s', st.session_state.username, page)

    # --- page振り分け
    if st.session_state.page == 'input_name':
        input_name()
    elif st.session_state.page == 'deal_data':
        deal_data()
    elif st.session_state.page == 'vis':
        vis()        

def input_name():
    # Input username
    with st.form("my_form"):
        inputname = st.text_input('username', 'default')
        submitted = st.form_submit_button("Submit")
        if submitted: # Submit buttonn 押された時に
            if inputname == 'default' or input_name == '': # nameが不適当なら
                submitted = False  # Submit 取り消し

        
        if submitted:
            st.session_state.username = inputname
            st.session_state.page = 'deal_data'
            st.write("名前: ", inputname)
      

def deal_data():
    st.title("サッカーデータ")

    st.sidebar.markdown('### 使用データの選択')
    st.sidebar.markdown('**生データ**と、**1試合あたりに換算したデータ**の2種類あります↓')

    which_data = st.sidebar.selectbox(
        '使用したいチーム名を選択',
        ['生データ', '1試合あたりのデータ']
    )
    which_team = st.multiselect(
        '使用するデータを選択',
        teams
    )
    if which_data ==  '1試合あたりのデータ':
        logging.info('data per game')
        tmp_se = pd.DataFrame(
            data = [[datetime.datetime.now(), '1試合あたりのデータ']],
            columns = ['Time' , 'Task'] 
        )
        logging.info(',%s,使用データ,%s', st.session_state.username, '1試合あたりのデータ')
        df = data.get_data_per_game(which_team)
    else:
        tmp_se = pd.DataFrame(
            data = [[datetime.datetime.now(), '生データ']],
            columns = ['Time' , 'Task'] 
        )
        logging.info(',%s,使用データ,%s', st.session_state.username, '生データ')
        df = data.get_data(which_team)

    # dataframe: 動的な表
    st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('最大値を黄色くハイライトしています')


def vis():
    df = data.get_data_per_game(teams)
    vals = data.get_label_list()

    x_label = st.sidebar.selectbox(
        '横軸を選択',vals, key='x_jiku')

    y_label = st.sidebar.selectbox(
        '縦軸を選択', vals, key='y_jiku')

    logging.info(',%s,x軸,%s', st.session_state.username, x_label)
    logging.info(',%s,y軸,%s', st.session_state.username, y_label)

    cor = data.get_corrcoef(x_label, y_label)
    st.write('相関係数：' + str(cor))
    
    fig = px.scatter(
        x=df[x_label].values, y=df[y_label].values,
        labels={'x':x_label, 'y':y_label},
        hover_name=df['チーム'].values)
    st.plotly_chart(fig, use_container_width=True)

   
main()
