import itertools
import streamlit as st
from category_mapping import arxiv_mapping
from research import arxiv_research

FEEDS_PER_PAGE = 10

@st.cache_data(show_spinner=False)
def load_data(category_abbreviation, requested_announce_type):
    return arxiv_research(category_abbreviation, requested_announce_type)

st.set_page_config('Daily Research', ':book:', layout='wide')
st.title('Daily Research: A Reader for Latest Research Papers :book:')

with st.container(border=True):
    top_menu = st.columns([2, 2], vertical_alignment='center')
    bottom_menu = st.columns([2, 2], vertical_alignment='center')

    with top_menu[0]:
        category = st.selectbox('Category:', list(arxiv_mapping.keys()), index=None, placeholder='Select a Research Field')

    if category:
        subcategories = arxiv_mapping.get(category).get('sub_categories')

        with top_menu[1]:
            if (len(subcategories) > 0):
                subcategory = st.selectbox('Subcategory: ', list(subcategories.keys()), index=None, placeholder='Select a Research Field Subcategory')
            else:
                subcategory = st.selectbox('Subcategory: ', [''], index=None, placeholder='No Subcategories Available')
        
        with bottom_menu[0]:
            announce_type = st.selectbox('Announce Type: ', ['all', 'cross', 'new', 'replace', 'replace-cross'])
    else:
        with top_menu[1]:
            subcategory = st.selectbox('Subcategory: ', [''], index=None, placeholder='Select a Research Field Subcategory', disabled=True)
        
        with bottom_menu[0]:
            announce_type = st.selectbox('Announce Type: ', [''], disabled=True)

if category:
    category_data = arxiv_mapping.get(category)

    category_abbreviation = category_data.get('category_abbreviation')
    
    if subcategory:
        subcategory_abbreviation = category_data.get('sub_categories').get(subcategory)
        data_endpoint = '.'.join([category_abbreviation, subcategory_abbreviation])
    else:
        data_endpoint = category_abbreviation
    
    entries = load_data(data_endpoint, announce_type)

    if entries:
        col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment='center')
        
        page_selector = col3

        num_pages = ((len(entries) - 1) // FEEDS_PER_PAGE) + 1
        
        page_format = lambda i: f'{i + 1}'

        with page_selector:
            page = st.selectbox('Page Number: ', range(num_pages), format_func=page_format)

        min_index = page * FEEDS_PER_PAGE
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

                tags = [tag.get('term') for tag in entry.get('tags')]
                st.write('Tags: ', ', '.join(tags))

                arxiv_link = entry.get('link')
                pdf_link = arxiv_link.replace('abs', 'pdf')

                st.link_button('arXiv', arxiv_link)
                st.link_button('PDF', pdf_link)