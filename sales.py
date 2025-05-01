import streamlit as st
import pandas as pd
import plotly.express as px
df=pd.read_csv('df_new',index_col=0)
st.sidebar.header('sidebar for sales analysis')
select=st.sidebar.selectbox('select',['univariate','Bivariate','multivariate'])
st.sidebar.subheader("Filter Options")
cities = st.sidebar.multiselect("Filter by City", df["City"].unique(), default=df["City"].unique())
df['Date'] = pd.to_datetime(df['Date'])
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
df = df[(df["City"].isin(cities)) & (df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]
st.dataframe(df.head())

if select=='univariate':
    col=st.selectbox('select',df.columns)
    chart=st.selectbox('select',['histogram','pie','box'])
    if chart=='histogram':
        st.plotly_chart(px.histogram(data_frame= df, x= col, title= col,text_auto=True))
    elif chart=='pie':
        st.plotly_chart(px.pie(data_frame= df, names= col, title= col))
    elif chart=='box':
        st.plotly_chart(px.box(data_frame= df, x= col, title= col))
        
elif select=='Bivariate': 
    corr=df.corr(numeric_only=True).__round__(2)
    st.plotly_chart(px.imshow(corr,text_auto=True))  
    c_t=df.groupby('City')['Total'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=c_t,x='City',y='Total',text_auto=True,title='total sales per city'))
    p_t=df.groupby('Product line')['Total'].sum().reset_index()
    pr_c=df.groupby('Product line')['cogs'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=pr_c,x='Product line',y='cogs',text_auto=True,title='total cost per product line'))
    st.plotly_chart(px.bar(data_frame=p_t,x='Product line',y='Total',text_auto=True,title='total sales per product line'))
    B_t=df.groupby('Branch')['Total'].sum().reset_index()
    st.plotly_chart(px.pie(data_frame=B_t,names='Branch',values='Total',color='Branch',title='total sales per Branch'))
    m_t=df.groupby(df.Date)['Total'].sum().reset_index()
    st.plotly_chart(px.line(data_frame=m_t,x='Date',y='Total',title='history of total sales'))
    st.plotly_chart(px.histogram(data_frame= df, x='Tax 5%' ,y='Quantity',text_auto=True))
    st.plotly_chart(px.histogram(data_frame= df, x='Customer type' ,y='Quantity',text_auto=True))
    py_t=df.groupby('Payment')['Total'].sum().reset_index()
    st.plotly_chart(px.pie(data_frame=py_t,names=('Payment'),values='Total',title='total sales for each payment method'))
    
else :
    
    p_g=df.groupby(['Product line','Branch'])['gross income'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=p_g,x='Branch',y='gross income',color='Product line', barmode= 'group',text_auto=True,title='gross income for each Branch per each product line'))
    c_g_t=df.groupby(['Customer type','Gender'])['Total'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=c_g_t,x='Customer type',y='Total',color='Gender',barmode='group',text_auto=True,title='total sales for each customer type and gender'))
    P_B_r=df.groupby(['Product line','Branch'])['Rating'].mean().reset_index().__round__(2)
    st.plotly_chart(px.bar(data_frame=P_B_r,x='Product line',y='Rating',color='Branch',barmode='group',text_auto=True))
    
