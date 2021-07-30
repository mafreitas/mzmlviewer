import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
from pyopenms import *

uploaded_file = st.file_uploader("Choose a file")

@st.cache(show_spinner=False,hash_funcs={pyopenms_4.MSExperiment: lambda _: None})
def load_data(uploaded_file):
  
  filename=os.path.join("tmp",uploaded_file.name)
  with open(filename,"wb") as f: 
    f.write(uploaded_file.getbuffer())

  exp = MSExperiment()
  MzMLFile().load(filename, exp)
  return exp

if uploaded_file is not None:
    exp = load_data(uploaded_file)

@st.cache (show_spinner=False,hash_funcs={pyopenms_4.MSExperiment: lambda _: None})
def get_tic(exp,level):
  
  retention_times = []
  intensities = []
  for spec in exp:
      if int(spec.getMSLevel()) in level:
          retention_times.append(spec.getRT())
          intensities.append(sum(spec.get_peaks()[1]))
  
  return [retention_times, intensities]

level = st.multiselect(
      'Select MS Level',
      [1, 2],
      [1]
     )

rt,i = get_tic(exp,level)
fig2, ax2 = plt.subplots(facecolor='black')
ax2.plot(rt,i)
# ax.spines['bottom'].set_color('white')
ax2.spines['top'].set_color('black') 
ax2.spines['right'].set_color('black')

st.pyplot(fig2)

scan = st.slider(
    'Select a range of values',
    0, len(rt)-1,0,1)


data = exp.getSpectrum(scan).get_peaks()
plt.style.use('dark_background')
fig1, ax1 = plt.subplots(facecolor='black')
ax1.plot(data[0],data[1])
# ax.spines['bottom'].set_color('white')
ax1.spines['top'].set_color('black') 
ax1.spines['right'].set_color('black')
st.pyplot(fig1)

