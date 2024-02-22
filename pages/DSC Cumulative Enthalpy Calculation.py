import streamlit as st

st.set_page_config(
    page_title="DSC"
)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("DSC Cumulative Enthalpy Calculation Sheet")

st.write("Under development...")