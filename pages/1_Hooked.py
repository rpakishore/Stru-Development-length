import streamlit as st
from handcalcs.decorator import handcalc
from math import sqrt
import pandas as pd

input = {
    'fc': 25,
    'fy': 400,
    'bar': 1,
    'side_cover':False,
    'tail_cover': True,
    '3_stirrups': True,
    'epoxy_bars': False,
    'Normal_density': True,
    'Hook': 1
}
bar_df = pd.DataFrame({
    'bars': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
    'size': [11.3, 16, 19.5, 25.2, 29.9, 35.7, 43.7, 56.4],
    'area': [100, 200, 300, 500, 700, 1000, 1500, 2500],
    'hook dia': [60, 90, 100, 150, 200, 250, 400, 550]
    })

# <!-----Heading------>
st.header("Development of standard hooks in tension | Cl. 12.5")
# <!-----Inputs------>
st.subheader("Inputs")
left_column, right_column = st.columns(2)
with left_column:
    input['fc'] = st.slider("Concrete compressive Strength (f'c)", 5, 60, input['fc'],5, help="Clause 12.1.2 limits the max. concrete strength to 64MPa")

    input['fy'] = st.slider("Steel tensile Strength (fy)", 300, 500, input['fy'], 50)

    options = list(bar_df['bars'])
    input['bar'] = st.selectbox('Bar size',options,index=input['bar'],)
    input['bar'] = options.index(input['bar'])

    options = ('180°', '90°')
    input['Hook'] = st.selectbox('Hook type',options, index=input['Hook'])
    input['Hook'] = options.index(input['Hook'])

with right_column:
    st.write("**Options**")
    input['side_cover'] = st.checkbox("Side cover < 60mm", input['side_cover'], help="side cover (normal to plane of hook) is less than 60mm")
    input['tail_cover'] = st.checkbox("Tail cover > 50mm", input['tail_cover'], help="For 90° hooks, cover on bar extension beyond the hook is not less than 50mm")
    input['3_stirrups'] = st.checkbox("Atleast 3 stirrups or ties", input['3_stirrups'], help=f"Hook is enclosed vertically/horizontally within 3 ties/stirrups spaced along a length of > {int(bar_df['hook dia'][input['bar']])} mm and a spacing <= {round(bar_df['size'][input['bar']]*3,1)} mm")
    input['epoxy_bars'] = st.checkbox("Epoxy coated bars", input['epoxy_bars'])
    input['Normal_density'] = st.checkbox("Normal-density concrete", input['Normal_density'])


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
    if input['bar'] < 6:
        if not input['side_cover']:
            if input['Hook'] == 1:
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
    if input['bar'] < 6:
        if input['3_stirrups']:
            k_2 = 0.8
            comment = "Ties/Stirrup\ requirement\ met"
        else:
            comment = "Ties/Stirrup\ requirement\ not\ met"
    else:
        comment = "Bar size > 35M"
    comment += "\ |\ Cl. 12.5.3.c"
    return k_2, comment

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
    d_b=bar_df['size'][input['bar']],
    f_prime_c=input['fc'],
    f_y = input['fy']
    )
result_latex, result_value = development_length(calculation_value['l_hb'], bar_df['size'][input['bar']])
st.latex(result_latex + '\ mm\ |\ (Cl. 12.5.1)')
st.latex("l_{dh} = " + str(int(result_value['l_dh'])) + '\ mm')

# <!-----Calculations tab------>
st.subheader("Calculation")
st.latex("k_{1} =" + str(k_1) +"\ (" + k_1_comment + ")")
st.latex("k_{2} =" + str(k_2) +"\ (" + k_2_comment + ")")
st.latex("k_{3} =" + str(k_3) +"\ (" + k_3_comment + ")")
st.latex("k_{4} =" + str(k_4) +"\ (" + k_4_comment + ")")
st.latex(calculation_latex)