import streamlit as st
from category_mapping import arxiv_mapping
from research import arxiv_research

st.set_page_config('Daily Research', ':book:', layout='wide')

st.title('Daily Research: A Reader for Latest Research Papers :book:')

category = st.selectbox('Research Field', arxiv_mapping.keys(), index=None, placeholder='Select a Research Field', label_visibility='collapsed')

@st.cache_data(show_spinner=False)
def load_data(category):
    return arxiv_research(category)

with st.spinner(f'Loading {category} RSS Feeds ....'):
    entries = load_data(category)

    for entry in entries:
        with st.expander(entry.get('title')):
            st.write('Authors: ', entry.get('author'))
            
            arxiv_id = entry.get('id').split(':')[2]
            st.write('arXiv ID: ', arxiv_id)
            
            st.write('Announce Type: ', entry.get('arxiv_announce_type'))

            summary = entry.get('summary')

            abstract_index = summary.index('Abstract')
            abstract = summary[abstract_index:]

            st.write(abstract)

            arxiv_link = entry.get('link')
            pdf_link = arxiv_link.replace('abs', 'pdf')

            st.link_button('arXiv', arxiv_link)
            st.link_button('PDF', pdf_link)