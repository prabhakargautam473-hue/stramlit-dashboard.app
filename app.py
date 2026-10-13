import os
os.system("pip intsall matplotlib pandas  streamlit)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout="wide",page_title="STARTUP FUNDING ANALYSIS")
df=pd.read_csv("star
tup_clean.csv")
df["date"]=pd.to_datetime(df["date"],errors="coerce")
df["month"]=df["date"].dt.month
df["year"]=df["date"].dt.year

def load_overall_analysis():
    st.title("overall analysis")
    col1,col2,col3,col4=st.columns(4)
    with col1:
      total=round(df["amount"].sum())
      st.metric("total",str(total)+"cr")
    with col2:
      max_amount=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
      st.metric("max_amount",str(max_amount)+"cr")
    with col3:
        avearge_funding=df.groupby('startup')["amount"].sum().mean()
        st.metric("average_funding",str(round(avearge_funding))+"cr")

    with col4:
        total_funded_starttup=df["startup"].nunique()
        st.metric("total_funded_starttup",(total_funded_starttup))

    st.header("mom graph")
    selected_option=st.selectbox("select type",["total","count"])
    if selected_option=="total":
      temp_df=df.groupby(["year","month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x_axis"]=temp_df["month"].astype(str)+"-"+ temp_df["year"].astype(str)
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df["x_axis"], temp_df["amount"])
    st.pyplot(fig5)


def load_investor_details(investor):
    st.title(investor)
    last_5df=df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("most recent investment")
    st.dataframe(last_5df)
    col1,col2=st.columns(2)
    with col1:

     big_series=df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
     st.subheader("highest investment")
     fig,ax=plt.subplots()
     ax.bar(big_series.index,big_series.values)
     st.pyplot(fig)
    with col2:
        vertical_series=df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("sector investement in:")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index)
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
      round_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
      st.subheader("round investement in:")
      fig2, ax2 = plt.subplots()
      ax2.pie(round_series, labels=round_series.index)
      st.pyplot(fig2)
    with col4:
      city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
      st.subheader("city investement in:")
      fig3, ax3 = plt.subplots()
      ax3.pie(city_series, labels=city_series.index)
      st.pyplot(fig3)

    df["year"]=df["date"].dt.year
    year_series=df[df['investors'].str.contains(' IDG Ventures')].groupby('year')['amount'].sum()
    st.subheader("year on year investement in:")
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)

st.sidebar.title("STARTUP FUNDING ANALYSIS")
option=st.sidebar.selectbox("select one",["overall analysis","startup analysis","investor analysis"])
if option=="overall analysis":
        load_overall_analysis()

elif option=="startup analysis":
    st.title("startup analysis")
    st.sidebar.selectbox("select startup",sorted(df["startup"].unique().tolist()))
    st.sidebar.button("find startup details")

else:
    investor=st.sidebar.selectbox("select investor",sorted(set(df["investors"].str.split(",").sum())))
    btn2=st.sidebar.button("find investor details")
    if btn2:
        load_investor_details(investor)
