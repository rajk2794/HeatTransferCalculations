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

(I) :rainbow[A phase-change material (PCM)] is a substance that undergoes a phase transition—typically between the fundamental states of matter, solid and liquid—while releasing or absorbing significant energy. The key feature of PCMs lies in their ability to store and release this energy during phase changes. When a PCM transitions from solid to liquid (or vice versa), it exhibits a latent heat storage property.

:orange[**A three-layer calorimeter**] is a specialized device used for precise heat measurements in scientific experiments. Let’s delve into its components and functioning:
1.	Metallic Vessel: The core of the calorimeter is a metallic vessel made of materials like copper or aluminum, which are good conductors of heat. This vessel holds the substances involved in the experiment.
2.	Insulating Jacket: The metallic vessel is placed inside an insulating jacket. This jacket prevents heat loss to the environment, ensuring that the calorimeter remains thermally isolated during the experiment.
3.	Thermometer Access: The calorimeter has a single opening through which a thermometer can be inserted. This thermometer monitors the change in thermal properties inside the vessel.
The working principle of a three-layer calorimeter involves measuring the heat exchange between substances. For instance, if a fixed amount of fuel is burned within the calorimeter, the heat lost by the fuel is equal to the heat gained by the water inside. By insulating the calorimeter, we improve the accuracy of the experiment. Through such measurements, we can determine both the heat capacity and the energy stored inside a phase change material. 

(II) A PCM Object is an encapsulation with a phase change material. A plastic bottle with a PCM inside is a PCM Object.

:green[**Mixing Calorimeter Calculation**] can determine enthalpy stored in a PCM object in a defined temperature range.  The enthalpy consists of both latent energy and specific capacity energy of the material. 

(III) Differential Scanning Calorimetry (DSC) is a powerful thermal analysis technique used to investigate the heat flow associated with phase transitions and chemical reactions in materials.

:blue[**DSC Cumulative Enthalpy Calculation**] converts the raw heat flow data from DSC into cumulative enthalpy data of the sample material in a defined temperature range.

(IV) :violet[**A heat flow meter (HFM)**] is a specialized laboratory instrument used to measure the thermal properties of various materials, including foams, solids, and textiles. Here’s how it works:
1.	Principle: In an HFM, a test specimen is placed between two heated plates. These plates are controlled to maintain a user-defined mean sample temperature and a specific temperature drop. The sample’s thickness corresponds to its actual dimension or matches the desired thickness for compressible samples.
2.	Heat Flow Measurement: The HFM measures the heat flowing through the specimen. It does so using two calibrated heat flux transducers that cover a large area on both sides of the sample. After reaching thermal equilibrium, the heat flux transducer output is calibrated with a standard.
3.	Thermal Conductivity Calculation: The average heat flux and the thermal resistance are used to calculate the thermal conductivity (λ) according to Fourier’s Law. The lower the U-value (reciprocal of total thermal resistance), the better the insulating ability of the material.
4.	Applications: HFMs are essential for determining thermal conductivity in materials like insulators, pipe insulations, and construction elements. They play a crucial role in optimizing energy efficiency, designing insulation systems, and ensuring material performance.

 :gray[**The Heat Flow Meter (HFM) sheet**] calculate thermal properties from raw temperature data.

'''
st.markdown(multi)