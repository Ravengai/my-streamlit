import pickle
from pathlib import Path
import pandas as pd
import numpy as np

import fredapi as fd
import plotly.express as px 
from prophet import Prophet 


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")

st.subheader("🔔 Zimbabwe Economic Descriptive Analysis")
st.markdown("##")

hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller","bharath"]
usernames = ["pparker", "rmiller","bharath"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "SIPL_dashboard", "abcdef")

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    st.markdown(hide_bar, unsafe_allow_html=True)

if authentication_status == None:
    st.warning("Please enter your username and password")
    st.markdown(hide_bar, unsafe_allow_html=True)


    

if authentication_status:
    # # ---- SIDEBAR ----
    st.sidebar.title(f"Welcome {name}")
    # st.sidebar.header("select page here :")
    st.write("# Welcome to Streamlit!..")

    ###about ....
    st.subheader("Introduction :")
    

    st.sidebar.success("Select a page above.")

    fred=fd.Fred(api_key='c6575e2b102a38fd5abeea5908ed690c')
    
    data=fred.search('Real Gross Domestic Product for Zimbabwe')
    
    
    
    cpi=fred.get_series('ZWENGDPRPCPPPT')
    cpi.name='values'
    
    
    df=pd.DataFrame(cpi).reset_index()
    
    st.table(df)
    
    
    df2=df[df['index']>'2000-01-01']
    
    fig=px.line(df2,x='index',y='values',title='Real GDP growth Avg. 2001-2024')
    st.write(fig)
    
    df2=df2.rename(columns={'index':'ds','values':'y'})
    
    
    # Create a Prophet model instance
    model = Prophet()
    
    # Train the model with the prepared data
    model.fit(df2)
    
    # Create a dataframe for the future period to be predicted
    future = model.make_future_dataframe(periods=14, freq='MS')
    
    # Perform prediction using the model
    
    forecast = model.predict(future)
    forecast[['ds','yhat','yhat_lower','yhat_upper']].round().tail()
    forecast
    
    fig=model.plot(forecast)
    st.write(fig)
    
    
        ###---- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    authenticator.logout("Logout", "sidebar")
    