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

# <!-----Other functions------>

# <!-----Heading------>
st.header("Tension development length")
# <!-----Inputs------>
st.subheader("Inputs")

# <!-----Calculations------>

# <!-----Results tab------>
st.subheader("Result")


# <!-----Calculations tab------>
st.subheader("Calculation")