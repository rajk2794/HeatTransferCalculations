import streamlit as st

st.set_page_config(
    page_title="MC"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Mixing Calorimeter Calculation Sheet")

st.write("Under development...")