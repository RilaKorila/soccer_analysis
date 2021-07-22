from pandas.core.frame import DataFrame
import streamlit as st
import data
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from gsheetsdb import connect


# log_df = pd.DataFrame([datetime.datetime.now(), 'Start Analysis!'], columns = ['Time' , 'Task'])
# log_df = pd.DataFrame(columns = ['Time' , 'Task'])
# log_df = log_df.append({'Time' : datetime.datetime.now(), 'Task' : 'Start'} , ignore_index=True)

# -- スプレッドシートの設定 ---
# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
run_query(f'INSERT INTO "{sheet_url}" VALUES ("Tom", "dog")')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")

# ---------------------------

teams = ['イタリア', 'フランス', 'ドイツ', 'ポルトガル', 'アルゼンチン', 'ブラジル', 'イングランド',
    'ウクライナ', 'スペイン', 'エクアドル', 'メキシコ', 'オーストラリア', 'スイス', 'ガーナ',
    'スウェーデン', 'オランダ', 'コートジボアール', 'コスタリカ', 'チェコ', '韓国', 'チュニジア',
    'サウジアラビア', 'ポーランド', 'イラン', '日本', 'セルビア モンテネグロ', 'クロアチア', 'アンゴラ',
    'パラグアイ', 'トーゴ', 'アメリカ', 'トリニダードトバコ']

st.title("サッカーデータ　可視化 入門")

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
    log_df = log_df.append({'Time' : datetime.datetime.now(), 'Task' : '1試合あたりのデータ'} , ignore_index=True)
    # log_df = log_df.append({'Time' : datetime.datetime.now()} , ignore_index=True)
    df = data.get_data_per_game(which_team)
else:
    df = data.get_data(which_team)

# dataframe: 動的な表
st.dataframe(df.style.highlight_max(axis=0))

st.markdown('最大値を黄色くハイライトしています')


# セレクトボックス:  軸の選択
st.sidebar.markdown('### 何をしますか？？')

menu = st.sidebar.selectbox(
    '何をする？',
    ['ここから選ぼう','散布図を表示']
)


if menu == '散布図を表示':
    st.sidebar.markdown('### 散布図表示')
    st.sidebar.markdown('散布図の軸を変えてみよう↓')

    label = data.get_label_list()
    x_label = st.sidebar.selectbox('横軸を選択',label)
    y_label = st.sidebar.selectbox('縦軸を選択',label)

    """
    # 散布図で確認
    確認したい変数を選び、「散布図を表示」にチェック！

    上で選択したチームのデータのみ散布図に表示されます
    """

    # 選択した軸に合わせて散布図を表示
    # チェックボックスで表示/非表示
    #if st.sidebar.checkbox('散布図を表示'):
    cor = data.get_corrcoef(x_label, y_label)
    st.write('相関係数：' + str(cor))
    
    fig = px.scatter(
        x=df[x_label].values, y=df[y_label].values,
        labels={'x':x_label, 'y':y_label},
        hover_name=df['チーム'].values)
    st.plotly_chart(fig, use_container_width=True)


# →　全部出しといて、消したいものを選択する形式の方がいいかもしれない

# # saveボタン
# if st.sidebar.button('Submit'):
#     # df = data.get_data(which_team)
#     log_df.to_csv('./save.csv')
#     st.sidebar.success("Successfully Saved!!")

