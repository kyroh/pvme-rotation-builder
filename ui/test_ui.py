from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import json
import os

with open(os.path.join('utils', 'GEAR.json'), 'r') as g:
            gear = json.load(g)


helms = [item['name'] for item in gear if item['slot'] == 'helm']

with st.form("main_inputs"):
    st.write("Inside the form")
    helm = st.selectbox('Select and option', helms)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("helm", helm)

st.write("Outside the form")
    
    


