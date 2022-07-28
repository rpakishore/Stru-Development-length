from this import d
import streamlit as st
from handcalcs.decorator import handcalc
from math import sqrt
import pandas as pd
from datetime import datetime
import json

input = {
    'fc': 25,
    'fy': 400,
    'bar': '15M',
    'side_cover':False,
    'tail_cover': True,
    '3_stirrups': True,
    'epoxy_bars': False,
    'Normal_density': True,
    'Hook': '90°',
    'ties':False,
    'stirrups':False,
    'case3':False,
    "bar_location_factor":False,
    "coating_factor":"Uncoated reinforcement",
    "density_factor":"Normal-density concrete"
}

bar_df = pd.DataFrame({
    'bars': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
    'size': [11.3, 16, 19.5, 25.2, 29.9, 35.7, 43.7, 56.4],
    'area': [100, 200, 300, 500, 700, 1000, 1500, 2500],
    'hook dia': [60, 90, 100, 150, 200, 250, 400, 550]
    })

# <!-----Functions------>

# <!-----Handcalc functions------>
@handcalc(precision=1,right="\ mm", scientific_notation=False)
def basic_dev_length(d_b, f_y, f_prime_c):
    l_db = max((0.24*d_b*f_y)/sqrt(f_prime_c),0.044*d_b*f_y) #Cl. 12.3.2
    return locals()
    
@handcalc(precision=2, right="\ mm")
def development_length_case1(k_1, k_2, k_3, k_4, f_y, f_prime_c, d_b):
    l_d = max(0.45*min(k_1*k_2, 1.7)*k_3*k_4*f_y/sqrt(f_prime_c)*d_b, 300)
    return locals()

@handcalc(precision=2, right="\ mm")
def development_length_case2(k_1, k_2, k_3, k_4, f_y, f_prime_c, d_b):
    l_d = max(0.6*min(k_1*k_2, 1.7)*k_3*k_4*f_y/sqrt(f_prime_c)*d_b, 300)
    return locals()
# <!-----Other functions------>
def update_inputs():
    for key in input.keys():
        st.session_state[key] = input[key]

# <!-----Heading------>
st.header("Tension development length | Cl. 12.2")
# <!-----Inputs------>
st.subheader("Inputs")

for key in input.keys():
    if not key in st.session_state:
        st.session_state[key] = input[key]

left_column, right_column = st.columns(2)
with left_column:
    input['fc'] = st.slider(
        label="Concrete compressive Strength (f'c)", 
        min_value=5, 
        max_value=60, 
        value=input['fc'],
        step=5, 
        help="Clause 12.1.2 limits the max. concrete strength to 64MPa",
        key='fc')

    input['fy'] = st.slider(
        label="Steel tensile Strength (fy)", 
        min_value=300, 
        max_value=500, 
        value=input['fy'], 
        step=50, 
        key='fy')

    options = tuple(bar_df['bars'])
    input['bar'] = st.selectbox(label='Bar size',
                                options=options,
                                index=options.index(input['bar']),
                                key='bar')
    if type(input['bar']) == int:
        input['bar'] = options[input['bar']]
    d_b = bar_df[bar_df['bars']==input['bar']]['size'].iloc[0]

    st.write("**Cases**")
    input['ties'] = st.checkbox(
        label="Member contains minimum ties per Cl. 7.6.5",
        value=input['ties'],
        help="Cl.7.6.5",
        key='ties')

    input['stirrups'] = st.checkbox(
        label="Member contains minimum stirrups within ld per Cl. 11.2.8.2",
        value=input['stirrups'],
        help="Cl.11.2.8.2",
        key='stirrups')

    input['case3'] = st.checkbox(
        label=f"Slabs, walls, shells or folded plates w/ clear spacing > {int(d_b*2)}mm between bars being developed",
        value=input['case3'],
        key='case3')


with right_column:    
    st.markdown("##### Modification Factors")
    st.markdown("**Bar location factor (k1)**")
    input['bar_location_factor'] = st.checkbox(
        label=f"Hoirz. reinf. placed w/ more than 300mm of fresh concrete is cast in the member below",
        value=input['bar_location_factor'],
        key='bar_location_factor')

    st.markdown("**Coating Factor (k2)**")
    coating_options = (
        f"Epoxy coated rebat with clear cover < {int(d_b*3)}mm or with clearspcing between bars < {int(d_b*6)}mm",
        "For all other epoxy-coated reinforcement",
        "Uncoated reinforcement")
    input['coating_factor'] = st.radio(
        label = "Choose one of the following:",
        options = coating_options,
        index=coating_options.index(input['coating_factor']),
        key="coating_factor")

    st.markdown("**Concrete Density Factor (k3)**")
    density_options = (
        "Structural low-density concrete",
        "Structural semi-low-density concrete",
        "Normal-density concrete")
    input['density_factor'] = st.radio(
        label = "Choose one of the following:",
        options = density_options,
        index=density_options.index(input['density_factor']),
        key="density_factor")

# <!-----Calculations------>
if input['ties'] or input['stirrups'] or input['case3']:
    case = 1
else:
    case = 2
if input['bar_location_factor']:
    k_1 = 1.3
    k_1_latex = "k_{1} = 1.3\ (Cl. 12.2.4.a)"
else:
    k_1 = 1.0
    k_1_latex = "k_{1} = 1.0\ (Cl. 12.2.4.a)"

if input['coating_factor'] == coating_options[0]:
    k_2 = 1.5
    k_2_latex = "k_{2} = 1.3\ (Cl. 12.2.4.b)"
elif input['coating_factor'] == coating_options[1]:
    k_2 = 1.2
    k_2_latex = "k_{2} = 1.2\ (Cl. 12.2.4.b)"
elif input['coating_factor'] == coating_options[2]:
    k_2 = 1.0
    k_2_latex = "k_{2} = 1.0\ (Cl. 12.2.4.b)"

if input['density_factor'] == density_options[0]:
    k_3 = 1.3
    k_3_latex = "k_{3} = 1.3\ (Cl. 12.2.4.c)"
elif input['density_factor'] == density_options[1]:
    k_3 = 1.2
    k_3_latex = "k_{3} = 1.2\ (Cl. 12.2.4.c)"
elif input['density_factor'] == density_options[2]:
    k_3 = 1.0
    k_3_latex = "k_{3} = 1.0\ (Cl. 12.2.4.c)"

if input['bar'] in ['10M', '15M', '20M']:
    k_4 = 0.8
    k_4_latex = "k_{4} = 0.8\ (Bar\ size \leq 20M\ |\ Cl. 12.2.4.d)"
else:
    k_4 = 1.0
    k_4_latex = "k_{4} = 1.0\ (Bar\ size > 20M\ |\ Cl. 12.2.4.d)"

if case == 1:
    calc_latex, calc_value = development_length_case1(
        k_1=k_1,
        k_2=k_2,
        k_3=k_3,
        k_4=k_4,
        f_y=input['fy'],
        f_prime_c=input['fc'],
        d_b=d_b
    )
else:
    calc_latex, calc_value = development_length_case2(
        k_1=k_1,
        k_2=k_2,
        k_3=k_3,
        k_4=k_4,
        f_y=input['fy'],
        f_prime_c=input['fc'],
        d_b=d_b
    )
# <!-----Results tab------>
st.subheader("Result")
st.latex("l_{d}="+ str(int(calc_value['l_d'])) + '\ mm⁺')
st.write(f"⁺For the bar being developed: min. clear cover = {round(d_b,1)} mm and min. clear spacing = {round(1.4*d_b,1)} mm; per Cl. 12.2.3")

# <!-----Calculations tab------>
st.subheader("Calculation")
st.latex(k_1_latex)
st.latex(k_2_latex)
st.latex(k_3_latex)
st.latex(k_4_latex)
st.latex(calc_latex)
st.latex("l_{d}="+ str(int(calc_value['l_d'])) + '\ mm')