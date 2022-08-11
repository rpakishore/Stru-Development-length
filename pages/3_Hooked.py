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
    'Hook': '90°'
}


bar_df = pd.DataFrame({
    'bars': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
    'size': [11.3, 16, 19.5, 25.2, 29.9, 35.7, 43.7, 56.4],
    'area': [100, 200, 300, 500, 700, 1000, 1500, 2500],
    'hook dia': [60, 90, 100, 150, 200, 250, 400, 550]
    })


# <!-----Functions------>

# <!-----Handcalc functions------>
@handcalc(precision=1)
def calculation_steps(k_1,k_2,k_3,k_4,d_b,f_prime_c,f_y):
    """Generate latex and calculate basic development length

    Args:
        k_1 (float): Side cover parameter
        k_2 (float): Stirrup parameter
        k_3 (float): Concrete density parameter
        k_4 (float): Reinforcing bar parameter
        d_b (float): Bar diameter in mm
        f_prime_c (float): Concrete compressive strength in MPa
        f_y (float): Rebar tensile strength in MPa

    Returns:
        latex, local_variables: Returns the latex for the substitution and the local variables for the same
    """
    l_hb = k_1*k_2*k_3*k_4*(100*d_b)/sqrt(f_prime_c)*f_y/400
    return locals()

@handcalc(precision=1)
def development_length(l_hb, d_b):
    """Generate latex and calculate hooked development length

    Args:
        l_hb (float): basic development length in mm
        d_b (float): Bar diameter in mm

    Returns:
        latex, local_variables: Returns the latex for the substitution and the local variables for the same
    """
    l_dh = max(l_hb, 150, 8*d_b)
    return locals()

# <!-----Other functions------>
def k1(input):
    """Calculates side cover parameter based on inputs

    Args:
        input (dict): Dict. with all inputs defined

    Returns:
        float,str: returns the k1 parameter and comment justification
    """
    k_1 = 1.0
    if input['bar'] != "45M" and input['bar'] != "55M":
        if not input['side_cover']:
            if input['Hook'] == '90°':
                if input['tail_cover']:
                    k_1 = 0.7
                    comment = "Side cover > 60mm\ |\ 90°\ hook\ |\ Tail\ cover > 50mm"
                else:
                    comment = "Tail cover <= 50mm"
            else:
                k_1 = 0.7
                comment = "Side cover > 60mm"
        else:
            comment = "Side cover < 60mm"
    else:
        comment = "Bar size > 35M"
    comment += "\ |\ Cl. 12.5.3.b"
    return k_1, comment

def k2(input):
    """Calculates stirrup parameter based on inputs

    Args:
        input (dict): Dict. with all inputs defined

    Returns:
        float,str: returns the k2 parameter and comment justification
    """
    k_2 = 1.0
    if input['bar'] != "45M" and input['bar'] != "55M":
        if input['3_stirrups']:
            k_2 = 0.8
            comment = "Ties/Stirrup\ requirement\ met"
        else:
            comment = "Ties/Stirrup\ requirement\ not\ met"
    else:
        comment = "Bar size > 35M"
    comment += "\ |\ Cl. 12.5.3.c"
    return k_2, comment

def update_inputs():
    for key in input.keys():
        st.session_state[key] = input[key]
    return

# <!-----Heading------>
st.header("Development of standard hooks in tension | Cl. 12.5")
# <!-----Inputs------>
st.subheader("Inputs")

left_column, right_column = st.columns(2)

for key in input.keys():
    if key not in st.session_state:
        st.session_state[key] = input[key]

with left_column:
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

    options = ('180°', '90°')
    input['Hook'] = st.selectbox(label='Hook type',
                                 options=options, 
                                 key='Hook')
    if type(input['Hook']) == int:
        input['Hook'] = options[input['Hook']]

with right_column:
    st.write("**Options**")
    input['side_cover'] = st.checkbox(label="Side cover < 60mm",
                                      help="side cover (normal to plane of hook) is less than 60mm", 
                                      key='side_cover')
    input['tail_cover'] = st.checkbox(label="Tail cover > 50mm", 
                                      help="For 90° hooks, cover on bar extension beyond the hook is not less than 50mm", 
                                      key='tail_cover')
    input['3_stirrups'] = st.checkbox(label="Atleast 3 stirrups or ties", 
                                      help=f"Hook is enclosed vertically/horizontally within 3 ties/stirrups spaced along a length of > {int(bar_df[bar_df['bars']==input['bar']]['hook dia'].iloc[0])} mm and a spacing <= {round(bar_df[bar_df['bars']==input['bar']]['size'].iloc[0]*3,1)} mm", 
                                      key='3_stirrups')
    input['epoxy_bars'] = st.checkbox(label="Epoxy coated bars", 
                                      key='epoxy_bars')
    input['Normal_density'] = st.checkbox(label="Normal-density concrete", 
                                          key='Normal_density')
    
    uploaded_file = st.file_uploader(
        label="Upload variables",
        type = "json",
        help="Import previously used variables",
        accept_multiple_files=False
    )
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        input = json.load(uploaded_file)

        st.button(
            label="Update",
            on_click=update_inputs,
            key="update_button"
            )
        
# <!-----Calculations------>
k_1, k_1_comment = k1(input)
k_2, k_2_comment = k2(input)
if input['Normal_density']:
    k_3 = 1.0
    k_3_comment = "Normal-density\ concrete\ |\ Cl.12.5.3.e"
else:
    k_3 = 1.3
    k_3_comment = "Low-density\ concrete\ |\ Cl.12.5.3.e"

if input['epoxy_bars']:
    k_4 = 1.2
    k_4_comment = "Epoxy-coated\ reinforcement\ |\ Cl.12.5.3.f"
else:
    k_4 = 1.0
    k_4_comment = "Normal\ reinforcement\ |\ Cl.12.5.3.f"

# <!-----Results tab------>
st.subheader("Result")
calculation_latex, calculation_value = calculation_steps(
    k_1=k_1,
    k_2=k_2,
    k_3=k_3,
    k_4=k_4,
    d_b=bar_df[bar_df['bars']==input['bar']]['size'].iloc[0],
    f_prime_c=input['fc'],
    f_y = input['fy']
    )
result_latex, result_value = development_length(calculation_value['l_hb'], bar_df[bar_df['bars']==input['bar']]['size'].iloc[0])
st.latex(result_latex + '\ mm\ |\ (Cl. 12.5.1)')
st.latex("l_{dh} = " + str(int(result_value['l_dh'])) + '\ mm')

# <!-----Calculations tab------>
st.subheader("Calculation")
st.latex("k_{1} =" + str(k_1) +"\ (" + k_1_comment + ")")
st.latex("k_{2} =" + str(k_2) +"\ (" + k_2_comment + ")")
st.latex("k_{3} =" + str(k_3) +"\ (" + k_3_comment + ")")
st.latex("k_{4} =" + str(k_4) +"\ (" + k_4_comment + ")")
st.latex(calculation_latex)

#st.write(st.session_state)
_, middle_column,_ = st.columns(3)


with middle_column:
    st.download_button(
        label="Export Variables",
        help="Export the variables for above",
        file_name=f"Hooked_dev_length_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
        mime="application/json",
        data=json.dumps(input, indent=4))

# ---- HIDE STREAMLIT STYLE ----

hide_st_style = """
                <style>
                #MainMenu{visibility: hidden;}
                footer{visibility: hidden;}
                header{visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html = True)  