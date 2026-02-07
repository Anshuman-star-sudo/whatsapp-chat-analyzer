import streamlit as st
import preprocess   

st.sidebar.title("whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    st.text(data)
    df=preprocess.preprocess(data)
    st.dataframe(df)