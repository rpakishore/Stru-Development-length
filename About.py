#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from handcalcs.decorator import handcalc
from math import sqrt
st.write("# Development length calculator")
st.write("""
### Purpose
- This is a web application that calculates the necessary tension and compression development lengths.
- All calculations are in accordance with CSA A23.3-19; Cl.12.

### Disclaimer
Although this calculator has been formally checked for technical correctness, it is not a substitute for engineering judgement, and does not relieve users of their duty to conduct required checking and quality control procedures.

### References
| S. No. | Reference | Year|
|--------|-----------|-----|
| 1. | CSA A23.3; Cl.12 | 2019|

### Color reference
| Color             | Legend                                                                |
| ----------------- | ------------------------------------------------------------------ |
| ![ee0e00](https://via.placeholder.com/25/ee0e00?text=+) #Red | Error|
| ![ebbd14](https://via.placeholder.com/25/ebbd14?text=+) #Yellow | Warning message |
| ![002080](https://via.placeholder.com/25/002080?text=+) #Blue | Author's notes  |


### Instructions for use
1. Review all information on the cover sheet
2. From the side bar, choose one of the 3 pages available [Hooked](Hooked), [Compression](Compression), [Tension](Tension)
3. Proceed to calculations by filing in all the values in the side bar.
4. Review entire workbook after completion
5. You may collapse the side bar and print the page using `Ctrl+P` to save the calculation as PDF.

### Version Notes and releases

|Version|v1.1|
|---|---|
|Version Notes| Draft web-release|
|Version Date| 2022 - July - 27|

***
""")
st.components.v1.html("""
<h3 style="font-family:courier;">Created by</h3>
<p style="font-family:courier;">
Arun Kishore<br>
Structural EIT,<br>
Associated Engineering,<br>
<a href="mailto:rpakishore@gmail.com">Mail</a> • <a href="https://www.linkedin.com/in/rpakishore/">LinkedIn</a><br>
version: 1.1
</p>
""")