import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
st.set_page_config(layout="wide")

st.header("PvME Rotation Builder")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Rotations', 'Gear', 'Boss preset'], 
                         iconName=['Rotations', 'Gear', 'Boss preset'], default_choice=0)

if tabs =='Rotations':
    st.title("Create your rotation here")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Gear':
    st.title("Enter your gear inputs for each style you will be using in the encounter")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Boss preset':
    st.title("Select a boss and your preferred team size")
    st.write('Name of option is {}'.format(tabs))
