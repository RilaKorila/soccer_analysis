import streamlit as st
import data
import plotly.express as px
import pandas as pd
import datetime
import logging


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
    # If no, then initialize count to 0
    # # If count is already initialized, don't do anything
    if 'username' not in st.session_state:
        st.session_state.username = 'default'

    # Input username
    inputname = st.text_input('username', 'default')
    if inputname != 'default':
        st.session_state.username = inputname
        st.write('username: ', st.session_state.username)
        st.success("Let's Start!")

        deal_data()



def deal_data():
    st.title("サッカーデータ")

    # data_page = st.sidebar.button('データ加工')
    # if data_page:
    #     print("data_page")

    # vis_page = st.sidebar.button('データ可視化')
    # if vis_page:
    #     print("vis_page")
    #     vis()
    page = st.sidebar.radio('ページ選択', ('データ加工', 'データ可視化'))
    if page == 'データ加工':
        logging.info('%s,ページ選択,%s', st.session_state.username, page)
    elif page == 'データ可視化':
        logging.info('%s,ページ選択,%s', st.session_state.username, page)
        vis()

    

    # st.markdown('# 使用したデータ')
    st.sidebar.markdown('### 使用データの選択')
    st.sidebar.markdown('**生データ**と、**1試合あたりに換算したデータ**の2種類あります↓')


    # # expander: toggle機能の追加
    # expander = st.beta_expander('どのチームのデータを使用するか制限')
    # expander.write('使用したいチーム名を選択')

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
        logging.info('%s,使用データ,%s', st.session_state.username, '1試合あたりのデータ')
        df = data.get_data_per_game(which_team)
    else:
        tmp_se = pd.DataFrame(
            data = [[datetime.datetime.now(), '生データ']],
            columns = ['Time' , 'Task'] 
        )
        logging.info('%s,使用データ,%s', st.session_state.username, '生データ')
        df = data.get_data(which_team)

    # dataframe: 動的な表
    st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('最大値を黄色くハイライトしています')


def vis():
    df = data.get_data_per_game(teams)
    label = data.get_label_list()
    x_label = st.sidebar.selectbox('横軸を選択',label)
    y_label = st.sidebar.selectbox('縦軸を選択',label)
    logging.info('%s,x軸,%s', st.session_state.username, x_label)
    logging.info('%s,y軸,%s', st.session_state.username, y_label)

    cor = data.get_corrcoef(x_label, y_label)
    st.write('相関係数：' + str(cor))
    
    fig = px.scatter(
        x=df[x_label].values, y=df[y_label].values,
        labels={'x':x_label, 'y':y_label},
        hover_name=df['チーム'].values)
    st.plotly_chart(fig, use_container_width=True)

    # # セレクトボックス:  軸の選択
    # st.sidebar.markdown('### 何をしますか？？')

    # menu = st.sidebar.selectbox(
    #     '何をする？',
    #     ['ここから選ぼう','散布図を表示']
    # )


    # if menu == '散布図を表示':
    #     st.sidebar.markdown('### 散布図表示')
    #     st.sidebar.markdown('散布図の軸を変えてみよう↓')

    #     label = data.get_label_list()
    #     x_label = st.sidebar.selectbox('横軸を選択',label)
    #     y_label = st.sidebar.selectbox('縦軸を選択',label)
    #     logging.info('%s,x軸,%s', st.session_state.username, x_label)
    #     logging.info('%s,y軸,%s', st.session_state.username, y_label)

    #     """
    #     # 散布図で確認
    #     確認したい変数を選び、「散布図を表示」にチェック！

    #     上で選択したチームのデータのみ散布図に表示されます
    #     """

    #     # 選択した軸に合わせて散布図を表示
    #     # チェックボックスで表示/非表示
    #     #if st.sidebar.checkbox('散布図を表示'):
    #     cor = data.get_corrcoef(x_label, y_label)
    #     st.write('相関係数：' + str(cor))
        
    #     fig = px.scatter(
    #         x=df[x_label].values, y=df[y_label].values,
    #         labels={'x':x_label, 'y':y_label},
    #         hover_name=df['チーム'].values)
    #     st.plotly_chart(fig, use_container_width=True)

    # if st.sidebar.button("Start Balloon"):
    #     st.balloons()
    #     logging.info('%s,balloon,%s', st.session_state.username, 'clicked')
    # # →　全部出しといて、消したいものを選択する形式の方がいいかもしれない


main()