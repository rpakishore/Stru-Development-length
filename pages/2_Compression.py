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
    'spiral': False,
    '10M': False
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
def development_length(l_db, k_1):

    l_d = max(l_db*k_1, 200)
    return locals()
# <!-----Other functions------>
def update_inputs():
    for key in input.keys():
        st.session_state[key] = input[key]

# <!-----Heading------>
st.header("Compression development length | Cl. 12.3")
# <!-----Inputs------>
st.subheader("Inputs")

for key in input.keys():
    if key not in st.session_state:
        st.session_state[key] = input[key]

input['fc'] = st.slider(
    label="Concrete compressive Strength (f'c)", 
    min_value=5, 
    max_value=60, 
    step=5, 
    help="Clause 12.1.2 limits the max. concrete strength to 64MPa",
    key='fc')

input['fy'] = st.slider(
    label="Steel tensile Strength (fy)", 
    min_value=300, 
    max_value=500, 
    step=50, 
    key='fy')

options = tuple(bar_df['bars'])
input['bar'] = st.selectbox(label='Bar size',
                            options=options,
                            key='bar')
if type(input['bar']) == int:
    input['bar'] = options[input['bar']]

input['spiral'] = st.checkbox(
    label="Reinforcement enclosed within spiral rebar > Ø6mm and <100mm pitch",
    key='spiral')

input['10M'] = st.checkbox(
    label = "Reinforcement enclosed within 10M ties in compliance with Cl. 7.6.5 and spaced < 100mm",
    key=['10M'],
    help="Cl. 7.6.5 refers to `Ties for compression members`"
)
# <!-----Calculations------>
if input['spiral'] or input['10M']:
    modification_latex = "k_1 = 0.75\ |\ (Modification Factor\ |\ Cl. 12.3.3.b)"
    k_1 = 0.75
else:
    modification_latex = "k_1 = 1.0\ |\ (Modification Factor\ |\ Cl. 12.3.3.b)"
    k_1 = 1.0

# <!-----Results tab------>
st.subheader("Result")
basic_dev_latex, basic_dev_value = basic_dev_length(
    d_b=bar_df[bar_df['bars']==input['bar']]['size'].iloc[0],
    f_y = input['fy'],
    f_prime_c = input['fc'])
result_latex, result_value = development_length(
    l_db=basic_dev_value['l_db'],
    k_1 = k_1
)
st.latex("l_{d} = " + str(int(result_value['l_d'])) + '\ mm')

# <!-----Calculations tab------>
st.subheader("Calculation")
st.latex(basic_dev_latex)
st.latex(modification_latex)
st.latex(result_latex)