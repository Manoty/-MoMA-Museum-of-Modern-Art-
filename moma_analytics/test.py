import streamlit as st

st.write("Tab 1")

tab1, tab2 = st.tabs(["A", "B"])

with tab1:
    st.write("Content 1")

with tab2:
    st.write("Content 2")