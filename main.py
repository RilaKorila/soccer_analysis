import streamlit as  st
import numpy as  np
import pandas as pd
from PIL import Image
import time
import data
import plotly.express as px
import plotly.figure_factory as ff

teams = ['イタリア', 'フランス', 'ドイツ', 'ポルトガル', 'アルゼンチン', 'ブラジル', 'イングランド',
    'ウクライナ', 'スペイン', 'エクアドル', 'メキシコ', 'オーストラリア', 'スイス', 'ガーナ',
    'スウェーデン', 'オランダ', 'コートジボアール', 'コスタリカ', 'チェコ', '韓国', 'チュニジア',
    'サウジアラビア', 'ポーランド', 'イラン', '日本', 'セルビア モンテネグロ', 'クロアチア', 'アンゴラ',
    'パラグアイ', 'トーゴ', 'アメリカ', 'トリニダードトバコ']

st.title("サッカー可視化 入門")


st.markdown('# 使用したデータ')
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
    df = data.get_data_per_game(which_team)
else:
    df = data.get_data(which_team)

# dataframe: 動的な表
st.dataframe(df.style.highlight_max(axis=0))


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

        

st.markdown('→　全部出しといて、消したいものを選択する形式の方がいいかもしれない')

# table: 静的な表
# st.table(df.style.highlight_max(axis=0))
# 参照：API reference -> Display data




# # slider bar
# condition = st.sidebar.slider('How is your condition?', 0, 100)
# 'condition: ', condition
# # 参照：API reference -> Display interactive widgets

# 2カラムにする
# left_column, right_column = st.beta_columns(2)
# button = left_column.button('右カラムに文字を表示')
# if button:
#     right_column.write('ここは右カラム')

# expander: toggle機能の追加
# expander = st.beta_expander('問い合わせ')
# expander.write('問い合わせ内容をかく')
# markdown記法が使える
# """
# # 章
# ## 節
# ### 項

# ``` python
# import streamlit as  st
# import numpy as  np
# import pandas as pd
# ```
# """
# 参照：API reference -> Display text

