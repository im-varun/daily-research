import itertools
import streamlit as st
from category_mapping import arxiv_mapping
from research import arxiv_research

FEEDS_PER_PAGE = 10

@st.cache_data(ttl='1h', show_spinner=False)
def load_data(category_abbreviation, requested_announce_type, requested_keywords):
    return arxiv_research(category_abbreviation, requested_announce_type, requested_keywords)

st.set_page_config(page_title='Daily Research', page_icon=':book:', layout='wide')
st.title(body='Daily Research: A Reader for Latest Research Papers :book:')

with st.container(border=True):
    top_menu = st.columns(spec=[2, 2], vertical_alignment='center')
    bottom_menu = st.columns(spec=[2, 6], vertical_alignment='center')

    with top_menu[0]:
        category = st.selectbox(label='Category:', options=list(arxiv_mapping.keys()), index=None, placeholder='Select a Category')

    if category:
        category_data = arxiv_mapping.get(category)

        subcategories = category_data.get('sub_categories')

        if (len(subcategories) > 0):
            subcategories_list = list(subcategories.keys())
            subcategories_placeholder = 'Select a Subcategory'
        else:
            subcategories_list = ['']
            subcategories_placeholder = 'No Subcategories Available'
        
        announce_type_list = ['all', 'cross', 'new', 'replace', 'replace-cross']

        search_text_value = ''

        subcategories_flag = False
        announce_type_flag = False
        search_text_flag = False
    else:
        subcategories_list = ['']
        subcategories_placeholder = ''

        announce_type_list = ['']

        search_text_value = ' '

        subcategories_flag = True
        announce_type_flag = True
        search_text_flag = True

    with top_menu[1]:
        subcategory = st.selectbox(label='Subcategory: ', options=subcategories_list, index=None, placeholder=subcategories_placeholder, disabled=subcategories_flag)

    with bottom_menu[0]:
        announce_type = st.selectbox(label='Announce Type: ', options=announce_type_list, disabled=announce_type_flag)

    with bottom_menu[1]:
        search_text = st.text_input(label='Keywords: ', value=search_text_value, placeholder='Search for Keywords', disabled=search_text_flag)

if category:
    category_data = arxiv_mapping.get(category)

    category_abbreviation = category_data.get('category_abbreviation')
    
    if subcategory:
        subcategory_abbreviation = category_data.get('sub_categories').get(subcategory)
        data_endpoint = '.'.join([category_abbreviation, subcategory_abbreviation])
    else:
        data_endpoint = category_abbreviation

    if search_text:
        search_keywords = search_text.split()
    else:
        search_keywords = []
    
    entries = load_data(data_endpoint, announce_type, search_keywords)

    if entries:
        results_menu = st.columns(spec=[6, 2], vertical_alignment='center')
        
        results_information = results_menu[0]
        page_selector = results_menu[1]

        num_pages = ((len(entries) - 1) // FEEDS_PER_PAGE) + 1
        
        page_format = lambda i: f'{i + 1}'

        with results_information:
            st.markdown(body=f'**Total Results:** {len(entries)}')

        with page_selector:
            page = st.selectbox(label='Page Number: ', options=range(num_pages), format_func=page_format)

        min_index = page * FEEDS_PER_PAGE
        max_index = min_index + FEEDS_PER_PAGE

        paginator = itertools.islice(enumerate(entries), min_index, max_index)

        for i, entry in paginator:
            with st.expander(label=entry.get('title')):
                st.write('Authors: ', entry.get('author'))
                
                arxiv_id = entry.get('id').split(':')[2]
                st.write('arXiv ID: ', arxiv_id)
                
                st.write('Announce Type: ', entry.get('arxiv_announce_type'))

                summary = entry.get('summary')
                abstract = summary[summary.index('Abstract'):]
                st.write(abstract)

                tags = [tag.get('term') for tag in entry.get('tags')]
                st.write('Tags: ', ', '.join(tags))

                arxiv_link = entry.get('link')
                pdf_link = arxiv_link.replace('abs', 'pdf')

                st.link_button(label='arXiv', url=arxiv_link)
                st.link_button(label='PDF', url=pdf_link)
    else:
        st.markdown(body='**Latest Research Papers for selected parameters are unavailable today.**')
        st.markdown(body='**Please check back tomorrow.**')