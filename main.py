import streamlit as st
import data
import plotly.express as px
import pandas as pd
import datetime
import logging



st.set_page_config(
    # page_title="PE Score Analysis App",
    # page_icon="π§",
    layout="wide",
    initial_sidebar_state="collapsed",
    )


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s,%(message)s")

teams = ['γ€γΏγͺγ’', 'γγ©γ³γΉ', 'γγ€γ', 'γγ«γγ¬γ«', 'γ’γ«γΌγ³γγ³', 'γγ©γΈγ«', 'γ€γ³γ°γ©γ³γ',
    'γ¦γ―γ©γ€γ', 'γΉγγ€γ³', 'γ¨γ―γ’γγ«', 'γ‘γ­γ·γ³', 'γͺγΌγΉγγ©γͺγ’', 'γΉγ€γΉ', 'γ¬γΌγ',
    'γΉγ¦γ§γΌγγ³', 'γͺγ©γ³γ', 'γ³γΌγγΈγγ’γΌγ«', 'γ³γΉγΏγͺγ«', 'γγ§γ³', 'ιε½', 'γγ₯γγΈγ’',
    'γ΅γ¦γΈγ’γ©γγ’', 'γγΌγ©γ³γ', 'γ€γ©γ³', 'ζ₯ζ¬', 'γ»γ«γγ’ γ’γ³γγγ°γ­', 'γ―γ­γ’γγ’', 'γ’γ³γ΄γ©',
    'γγ©γ°γ’γ€', 'γγΌγ΄', 'γ’γ‘γͺγ«', 'γγͺγγγΌγγγγ³']


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


    # --- pageιΈζγ©γΈγͺγγΏγ³
    page = st.sidebar.radio('γγΌγΈιΈζ', ('γγΌγΏε ε·₯', 'γγΌγΏε―θ¦ε'))
    if page == 'γγΌγΏε ε·₯':
        st.session_state.page = 'deal_data'
        logging.info(',%s,γγΌγΈιΈζ,%s', st.session_state.username, page)
    elif page == 'γγΌγΏε―θ¦ε':
        st.session_state.page = 'vis'
        logging.info(',%s,γγΌγΈιΈζ,%s', st.session_state.username, page)

    # --- pageζ―γεγ
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
        if submitted: # Submit buttonn ζΌγγγζγ«
            if inputname == 'default' or input_name == '': # nameγδΈι©ε½γͺγ
                submitted = False  # Submit εγζΆγ

        
        if submitted:
            st.session_state.username = inputname
            st.session_state.page = 'deal_data'
            st.write("εε: ", inputname)
      

def deal_data():
    st.title("γ΅γγ«γΌγγΌγΏ")

    st.sidebar.markdown('### δ½Ώη¨γγΌγΏγ?ιΈζ')
    st.sidebar.markdown('**ηγγΌγΏ**γ¨γ**1θ©¦εγγγγ«ζη?γγγγΌγΏ**γ?2η¨?ι‘γγγΎγβ')

    which_data = st.sidebar.selectbox(
        'δ½Ώη¨γγγγγΌγ εγιΈζ',
        ['ηγγΌγΏ', '1θ©¦εγγγγ?γγΌγΏ']
    )
    which_team = st.multiselect(
        'δ½Ώη¨γγγγΌγΏγιΈζ',
        teams
    )
    if which_data ==  '1θ©¦εγγγγ?γγΌγΏ':
        logging.info('data per game')
        tmp_se = pd.DataFrame(
            data = [[datetime.datetime.now(), '1θ©¦εγγγγ?γγΌγΏ']],
            columns = ['Time' , 'Task'] 
        )
        logging.info(',%s,δ½Ώη¨γγΌγΏ,%s', st.session_state.username, '1θ©¦εγγγγ?γγΌγΏ')
        df = data.get_data_per_game(which_team)
    else:
        tmp_se = pd.DataFrame(
            data = [[datetime.datetime.now(), 'ηγγΌγΏ']],
            columns = ['Time' , 'Task'] 
        )
        logging.info(',%s,δ½Ώη¨γγΌγΏ,%s', st.session_state.username, 'ηγγΌγΏ')
        df = data.get_data(which_team)

    # dataframe: εηγͺθ‘¨
    st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('ζε€§ε€γι»θ²γγγ€γ©γ€γγγ¦γγΎγ')


def vis():
    df = data.get_data_per_game(teams)
    vals = data.get_label_list()

    x_label = st.sidebar.selectbox(
        'ζ¨ͺθ»ΈγιΈζ',vals, key='x_jiku')

    y_label = st.sidebar.selectbox(
        'ηΈ¦θ»ΈγιΈζ', vals, key='y_jiku')

    logging.info(',%s,xθ»Έ,%s', st.session_state.username, x_label)
    logging.info(',%s,yθ»Έ,%s', st.session_state.username, y_label)

    cor = data.get_corrcoef(x_label, y_label)
    st.write('ηΈι’δΏζ°οΌ' + str(cor))
    
    fig = px.scatter(
        x=df[x_label].values, y=df[y_label].values,
        labels={'x':x_label, 'y':y_label},
        hover_name=df['γγΌγ '].values)
    st.plotly_chart(fig, use_container_width=True)

   
main()
