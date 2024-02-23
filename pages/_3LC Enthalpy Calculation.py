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
    page_title="3LC"
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

    file = st.file_uploader("Upload 3LC raw file",type=["xlsx"])

    cp_values = {'Water':4.18,'IPA':2.0}
    input_values = {}
    if file  is not None:
        
        df1 = pd.read_excel(file, usecols='A:D').round(2)
        new_df1 = df1.dropna()
        
        fig = px.line(new_df1,x="Time",y=["Sample","Reference","Air Bath"])
        fig.update_layout(
            title="T-History Graph",
            xaxis_title="Time in Sec.",
            yaxis_title="Temperature in degree C",
                font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
            )
        st.plotly_chart(fig)
        #except:
            #st.write(":red[*Error:* Please upload the correct file. Make sure columns are correctly labeled as 'Time', 'Sample', 'Reference', 'Air Bath' from columns 'A' to 'D'.]")

        col1, col2 = st.columns(2)
        
        with col1:

            CpRefMatrSelec = st.selectbox(':blue[**Select the reference material**]',cp_values.keys())
            
            CpRefMatr = cp_values[CpRefMatrSelec]
            st.markdown("*Cp of ref material is {} J/g-K.*".format(CpRefMatr))
            input_values['Cp of ref material in g'] = CpRefMatr

            WtEmptyPouRef = st.number_input(":blue[**Enter weight of empty ref pouches in g**]", value = 4.00)
            st.markdown('*Weight of empty ref pouches is {} g.*'.format(WtEmptyPouRef))
            input_values['Weight of empty ref pouches in g'] = WtEmptyPouRef

            WtPURef = st.number_input(":blue[**Enter weight of PU foam ref in g**]", value = 57.00)
            st.markdown('*Weight of PU foam ref is {} g.*'.format(WtPURef))
            input_values['Weight of PU foam ref in g'] = WtPURef

            WtRefMatr = st.number_input(":blue[**Enter weight of ref material in g**]", value = 40.00)
            st.markdown('*Weight of ref material is {} g.*'.format(WtRefMatr))
            input_values['Weight of ref material in g'] = WtRefMatr

            WtRefAluL = st.number_input(":blue[**Enter weight of aluminium layer ref in g**]", value = 95.00)
            st.markdown('*Weight of aluminium layer ref is {} g.*'.format(WtRefAluL))
            input_values['Weight of aluminium layer ref in g'] = WtRefAluL

            CalFact = st.number_input(":blue[**Enter calibration factor**]", value = 0.00)
            st.markdown('*Calibration factor is {}.*'.format(CalFact))
            input_values['Calibration factor'] = CalFact

        WtRefSetup = WtEmptyPouRef + WtPURef + WtRefAluL

        with col2:

            WtEmptyPouSam = st.number_input(":blue[**Enter weight of empty sample pouches in g**]", value = 4.00)
            st.markdown('*Weight of empty sample pouches is {} g.*'.format(WtEmptyPouSam))
            input_values['Weight of empty sample pouches in g'] = WtEmptyPouSam

            WtPUSam = st.number_input(":blue[**Enter weight of PU foam sample in g**]", value = 57.00)
            st.markdown('*Weight of PU foam sample is {} g.*'.format(WtPUSam))
            input_values['Weight of PU foam sample in g'] = WtPUSam

            WtSamMatr = st.number_input(":blue[**Enter weight of sample material in g**]", value = 40.00)
            st.markdown('*Weight of sample material is {} g.*'.format(WtSamMatr))
            input_values['Weight of sample material in g'] = WtSamMatr

            WtSamAluL = st.number_input(":blue[**Enter weight of aluminium layer sample in g**]", value = 96.00)
            st.markdown('*Weight of aluminium layer sample is {} g.*'.format(WtSamAluL))
            input_values['Weight of aluminium layer sample in g'] = WtSamAluL

        WtSamSetup = WtEmptyPouSam + WtPUSam + WtSamAluL

        Cpt = ((WtEmptyPouSam*2.3)+(WtPUSam*1.5)+(WtSamAluL*0.9))/((WtRefSetup+WtSamSetup)/2)
        Mt = (WtRefSetup+WtSamSetup)/2

        with col2:

            SamNam = st.text_input(":blue[**Enter sample name**]",value='PCM XXXX')
            st.markdown('*Sample name is {}.*'.format(SamNam))
            input_values['Sample name'] = SamNam
        
        const1 = ((WtRefMatr*CpRefMatr)+(Mt*Cpt*CalFact))/WtSamMatr
        const2 = (Mt*Cpt*CalFact)/WtSamMatr
        try:
            sample_temp_list = new_df1['Sample'].tolist()
            ref_temp_list = new_df1['Reference'].tolist() 
            bath_temp_list = new_df1['Air Bath'].tolist()
        except:
            sys.exit()

        def area(lst):
            area_lst = []
            for num in range(len(lst)):
                try:
                    area = ((lst[num] + lst[num+1])*0.05)
                    area = (round(area, 2))
                    area_lst.append(area)
                except:
                    continue
            return area_lst
        
        sample_area = area(sample_temp_list)
        ref_area = area(ref_temp_list)
        bath_area = area(bath_temp_list)

        def area_diff(lst1,lst2):
            area_diff_lst = []
            for num in range(len(lst1)):
                try:
                    diff = lst2[num] - lst1[num]
                    diff = abs(round(diff,2))
                    area_diff_lst.append(diff)
                except:
                    continue
            return area_diff_lst
        
        sample_area_diff = area_diff(sample_area, bath_area)
        ref_area_diff = area_diff(ref_area, bath_area)

        final_temp_lst = [i for n, i in enumerate(sample_temp_list) if i not in sample_temp_list[:n]]

        def areaSum(lst1,lst2,lst3):
            area_sum = {}
            for i in range(len(lst1)):
                area_sum[lst1[i]] = 0
                try:
                    for j in range(len(lst2)):
                        if lst2[j] == lst1[i]:
                            area_sum[lst1[i]] = area_sum[lst1[i]] + lst3[j]
                            area_sum[lst1[i]] = round(area_sum[lst1[i]],2)
                except:
                    continue
            return area_sum
        
        area_sum_sample = areaSum(final_temp_lst,sample_temp_list,sample_area_diff)
        area_sum_ref = areaSum(final_temp_lst,ref_temp_list,ref_area_diff)

        def sumInt(dic):
            sum_int = {}
            for i in dic.keys():
                k = int(i)        
                if k in sum_int.keys():
                    sum_int[k] = sum_int[k] + dic[i] 
                    sum_int[k] = round(sum_int[k],2)
                else:
                    sum_int[k] = dic[i]
                    sum_int[k] = round(sum_int[k],2)                       
            return sum_int
        
        sample_sum_int = sumInt(area_sum_sample)
        ref_sum_int = sumInt(area_sum_ref)

        deltaH = {}
        deltaH_commu = {}
        sum_enthl = 0
        for i in sample_sum_int.keys():
            try:
                deltaH[i] = ((const1*sample_sum_int[i])/ref_sum_int[i])-const2
                sum_enthl = sum_enthl + deltaH[i]
                deltaH_commu[i] = sum_enthl
            except:
                continue
        deltaH_finl = pd.DataFrame(deltaH.items(), columns=['Temp', 'Enthalpy'])
        deltaH_commu_finl = pd.DataFrame(deltaH_commu.items(), columns=['Temp', 'Commu Enthalpy'])
        deltaH_finl = deltaH_finl[np.isfinite(deltaH_finl).all(1)]
        deltaH_commu_finl = deltaH_commu_finl[np.isfinite(deltaH_commu_finl).all(1)]
        result = pd.merge(deltaH_finl, deltaH_commu_finl, on = 'Temp')

        input_values_finl = pd.DataFrame(input_values.items(), columns=['Input Description', 'Value'])
            
        output_data = new_df1.join(input_values_finl)
        output_data_finl = output_data.join(result)
        

        if st.button('Show Enthalpy Data'):
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(x=result["Temp"], y=result["Enthalpy"], name="Enthalpy"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=result["Temp"], y=result['Commu Enthalpy'], name="Commu Enthalpy"),
                secondary_y=True,
            )
            fig.update_layout(
                title_text="Enthalpy Graph"
            )
            fig.update_xaxes(title_text="Temperature in degree C")
            fig.update_yaxes(title_text="Enthalpy in J/g", secondary_y=False)
            fig.update_yaxes(title_text="Commulative Enthalpy in J/g", secondary_y=True)

            st.plotly_chart(fig)
            
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
            
            df_xlsx = to_excel(output_data_finl)
            st.download_button(label='📥 Download Input and Output Data',
                                            data=df_xlsx ,
                                            file_name= 'output_data.xlsx')





