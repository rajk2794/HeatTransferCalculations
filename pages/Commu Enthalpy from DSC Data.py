import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="CE-DSC"
)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

names = ["R&D Lab","Quality Lab"]
usernames = ["rdlab","qualitylab"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,hashed_passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})
        
authenticator = stauth.Authenticate(credentials, "3LC", "random_key", cookie_expiry_days=30)


name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    file = st.file_uploader("Upload DSC raw file",type=["xlsx"])
    st.download_button(label="Download template file", data=open('template_file_DSC.xlsx', 'rb').read(), file_name='template_file.xlsx',mime='xlsx')
    
    if file  is not None:

        try:
            progress_text = "DSC graph preparation in progress. Please wait..."
            my_bar = st.progress(0, text=progress_text)
            df1 = pd.read_excel(file, usecols='A:C').round(2)
            my_bar.progress(25, text=progress_text)
            new_df1 = df1.dropna()
            my_bar.progress(50, text=progress_text)
                    
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=new_df1["Time"], y=new_df1["Temp"], name="Temperature"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=new_df1["Time"], y=new_df1["Heat Flow"], name="Heat Flow"),
                secondary_y=True,
            )
            fig.update_layout(
                title_text="DSC Graph"
            )
            fig.update_xaxes(title_text="Time in Sec")
            fig.update_yaxes(title_text="Temperature in degree C", secondary_y=False)
            fig.update_yaxes(title_text="Heat Flow in mW", secondary_y=True)
            my_bar.progress(100, text=progress_text)
            st.plotly_chart(fig)
            my_bar.empty()
        except:
            st.error("Please upload the correct file. Make sure columns are correctly labeled as 'Time', 'Temp', 'Heat Flow' from columns 'A' to 'C'.")

        input_values = {} 

        col1, col2, col3 = st.columns(3)
        
        with col1:
            WtSam = st.number_input(":blue[**Enter Sample Weight mg**]", value = 5.00)
            st.markdown('*Weight of Sample is {} mg.*'.format(WtSam))
            input_values['Weight of Sample in mg'] = WtSam

        try:
            sample_temp_list = new_df1['Temp'].tolist()
            sample_HF_list = new_df1['Heat Flow'].tolist()
            
        except:
            sys.exit()

        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        def click_button():
            st.session_state.clicked = True

        st.button('Calculate Commulative Enthalpy', on_click=click_button)

        if st.session_state.clicked:
            progress_text = "The calculation in progress. Please wait..."
            my_bar = st.progress(0, text=progress_text)

            def area(lst):
                area_lst = []
                for num in range(len(lst)):
                    try:
                        area = abs(((lst[num] + lst[num+1])*0.5)/WtSam)
                        area = (round(area, 2))
                        area_lst.append(area)
                    except:
                        continue
                return area_lst
            
            heat_area = area(sample_HF_list)
            my_bar.progress(20, text=progress_text)

            final_temp_lst = [i for n, i in enumerate(sample_temp_list) if i not in sample_temp_list[:n]]
            my_bar.progress(40, text=progress_text)
            
            def areaSum(lst1,lst2,lst3):
                area_sum = {}
                
                for i in range(len(lst1)):
                    area_sum[lst1[i]] = 0
                    try:
                        for j in range(len(lst2)):
                            if lst2[j] == lst1[i]:
                                area_sum[lst1[i]] = (area_sum[lst1[i]] + lst3[j])
                                area_sum[lst1[i]] = round(area_sum[lst1[i]],2)
                    except:
                        continue
                return area_sum
            
                        
            area_sum_sample = areaSum(final_temp_lst,sample_temp_list,heat_area)
            my_bar.progress(60, text=progress_text)
            Test = pd.DataFrame(area_sum_sample.items(), columns=['Temp', 'Enthalpy'])
            
            commu_enthlpy = {}
            sum_enthlpy = 0
            for i in area_sum_sample.keys():
                try:
                    sum_enthlpy = sum_enthlpy + area_sum_sample[i]
                    commu_enthlpy[i] = sum_enthlpy
                except:
                    continue
            Test1 = pd.DataFrame(commu_enthlpy.items(), columns=['Temp', 'Commu Enthalpy'])

          
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=Test["Temp"], y=Test["Enthalpy"], name="Enthalpy"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=Test1["Temp"], y=Test1["Commu Enthalpy"], name="Commu Enthalpy"),
                secondary_y=True,
            )
            fig.update_layout(
                title_text="Commu Enthalpy Graph"
            )
            fig.update_xaxes(title_text="Temperature in degree C")
            fig.update_yaxes(title_text="Heat Flow in mW", secondary_y=False)
            fig.update_yaxes(title_text="Commulative Enthalpy in J/g", secondary_y=True)
            
            my_bar.progress(100, text=progress_text)
            st.plotly_chart(fig)
            output_data = pd.merge(Test,Test1, on = 'Temp')
            
            my_bar.empty()

            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '0.00'}) 
                worksheet.set_column('A:A', None, format1)  
                writer.close()
                processed_data = output.getvalue()
                return processed_data
            
            df_xlsx = to_excel(output_data)
            st.download_button(label='📥 Download Output Data',
                                            data=df_xlsx ,
                                            file_name= 'output_commu_enthalpy_DSC.xlsx')

            



