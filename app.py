import itertools
import streamlit as st
from category_mapping import arxiv_mapping
from research import arxiv_research

FEEDS_PER_PAGE = 10

@st.cache_data(show_spinner=False)
def load_data(category):
    return arxiv_research(category)

st.set_page_config('Daily Research', ':book:', layout='wide')
st.title('Daily Research: A Reader for Latest Research Papers :book:')

category = st.selectbox('Research Field', arxiv_mapping.keys(), index=None, placeholder='Select a Research Field', label_visibility='collapsed')

if category:
    entries = load_data(category)

    if entries:
        paginator_location = st.empty()

        num_pages = (len(entries) - 1) // (FEEDS_PER_PAGE + 1)
        page_format = lambda i: f'Page {i}'
        page_number = paginator_location.selectbox('Page Number', range(1, num_pages + 1), format_func=page_format, label_visibility='collapsed')

        min_index = page_number * FEEDS_PER_PAGE
        max_index = min_index + FEEDS_PER_PAGE

        paginator = itertools.islice(enumerate(entries), min_index, max_index)

        for i, entry in paginator:
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
    else:
        st.write('Announcements for latest research papers are unavailable today. Please check back tomorrow.')