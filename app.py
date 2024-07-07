import streamlit as st
from category_mapping import arxiv_mapping

st.set_page_config('Daily Research', ':newspaper:')

category = st.selectbox('Research Field', arxiv_mapping.keys(), index=None, placeholder='Select a Research Field')