import streamlit as st
from category_mapping import arxiv_mapping

category = st.selectbox('Research Field', arxiv_mapping.keys(), index=None, placeholder='Select a Research Field')