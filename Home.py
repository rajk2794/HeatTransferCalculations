import streamlit as st

st.set_page_config(
    page_title="Home"
)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Calculations in Heat Transfer")
st.sidebar.success("Select a :rainbow[calculation] above")

st.markdown("Welcome &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = ''':red[**Heat transfer**] is a fundamental process that occurs when there is a temperature difference between two systems. It involves the movement of thermal energy from a region of higher temperature to a region of lower temperature. There are three primary modes of heat transfer:
1.	Conduction: In this mode, energy is transmitted directly from one particle to another within a material. When particles with higher kinetic energy collide with slower-moving particles, the latter gain energy. 
2.	Convection: Convection occurs in fluids (liquids or gases) and involves the bulk movement of heated material. As a fluid is heated, it becomes less dense and rises, creating currents. Conversely, cooler fluid descends. 
3.	Radiation: Unlike conduction and convection, radiation does not require a medium. It is the transfer of energy through electromagnetic waves, such as infrared radiation. The Sun’s energy reaching Earth is an example of radiation. Objects emit and absorb radiation based on their temperatures.

:rainbow[A phase-change material (PCM)] is a substance that undergoes a phase transition—typically between the fundamental states of matter, solid and liquid—while releasing or absorbing significant energy. The key feature of PCMs lies in their ability to store and release this energy during phase changes. When a PCM transitions from solid to liquid (or vice versa), it exhibits a latent heat storage property.

:orange[**A three-layer calorimeter**] is a specialized device used for precise heat measurements in scientific experiments. Let’s delve into its components and functioning:
1.	Metallic Vessel: The core of the calorimeter is a metallic vessel made of materials like copper or aluminum, which are good conductors of heat. This vessel holds the substances involved in the experiment.
2.	Insulating Jacket: The metallic vessel is placed inside an insulating jacket. This jacket prevents heat loss to the environment, ensuring that the calorimeter remains thermally isolated during the experiment.
3.	Thermometer Access: The calorimeter has a single opening through which a thermometer can be inserted. This thermometer monitors the change in thermal properties inside the vessel.
The working principle of a three-layer calorimeter involves measuring the heat exchange between substances. For instance, if a fixed amount of fuel is burned within the calorimeter, the heat lost by the fuel is equal to the heat gained by the water inside. By insulating the calorimeter, we improve the accuracy of the experiment. Through such measurements, we can determine both the heat capacity and the energy stored inside a phase change material. 

'''
st.markdown(multi)