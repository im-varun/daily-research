'''
This script is used to build Daily Research web application using Streamlit.
'''

import itertools
import streamlit as st
from category_mapping import arxiv_mapping
from research import arxiv_research

# number of feeds to display per page
FEEDS_PER_PAGE = 10

@st.cache_data(ttl='1h', show_spinner=False)
def load_data(data_endpoint, requested_announce_type, requested_keywords):
    '''
    This function is used for loading and caching RSS feeds data.

    The data is cached for 1 hour. After that, the application will discard any old, cached 
    values, and the function will be rerun.

    :param data_endpoint: The endpoint (category name with optional subcategory name) to 
    pass to the RSS feeds link provided by arXiv.
    :param requested_announce_type: Research paper announce type to use in filtering RSS feeds.
    :param requested_keywords: Keywords to use in filtering RSS feeds.

    :return: Filtered entries of RSS feed.
    '''
    return arxiv_research(data_endpoint, requested_announce_type, requested_keywords)

# set page configuration and title
st.set_page_config(page_title='Daily Research', page_icon=':book:', layout='wide')
st.title(body='Daily Research: A Reader for Latest Research Papers :book:')

# add a container for input search parameters
with st.container(border=True):
    # create a top menu and bottom menu (in the container) to store input fields
    top_menu = st.columns(spec=[2, 2], vertical_alignment='center')
    bottom_menu = st.columns(spec=[2, 6], vertical_alignment='center')

    # add category input field in first column of top menu bar
    with top_menu[0]:
        category = st.selectbox(label='Category:', options=list(arxiv_mapping.keys()), index=None, placeholder='Select a Category')

    # based on the value of category input field, get the values associated with other input fields
    if category:
        # get the data associated with category selected in category input field
        category_data = arxiv_mapping.get(category)

        # get the subcategories associated with category selected in category input field
        subcategories = category_data.get('sub_categories')

        # based on the number of subcategories, get the values associated with subcategory input field (enabled)
        if (len(subcategories) > 0):
            subcategories_list = list(subcategories.keys())
            subcategories_placeholder = 'Select a Subcategory'
        else:
            subcategories_list = ['']
            subcategories_placeholder = 'No Subcategories Available'
        
        # values associated with announce type input field (enabled)
        announce_type_list = ['all', 'cross', 'new', 'replace', 'replace-cross']

        # value associated with keywords input field (enabled)
        search_text_value = ''

        # set disabled boolean flags for subcategory, announce type and keywords input field to False (enabled)
        subcategories_flag = False
        announce_type_flag = False
        search_text_flag = False
    else:
        # values associated with subcategory input field (disabled)
        subcategories_list = ['']
        subcategories_placeholder = ''

        # value associated with announce type input field (disabled)
        announce_type_list = ['']

        # value associated with keywords input field (disabled)
        search_text_value = ' '

        # set disabled boolean flags for subcategory, announce type and keywords input field to True (disabled)
        subcategories_flag = True
        announce_type_flag = True
        search_text_flag = True

    # add subcategory input field in second column of top menu bar
    with top_menu[1]:
        subcategory = st.selectbox(label='Subcategory: ', options=subcategories_list, index=None, placeholder=subcategories_placeholder, disabled=subcategories_flag)

    # add announce type input field in first column of bottom menu bar
    with bottom_menu[0]:
        announce_type = st.selectbox(label='Announce Type: ', options=announce_type_list, disabled=announce_type_flag)

    # add keywords input field in second column of bottom menu bar
    with bottom_menu[1]:
        search_text = st.text_input(label='Keywords: ', value=search_text_value, placeholder='Search for Keywords', disabled=search_text_flag)

if category:
    # get the data associated with category selected in category input field
    category_data = arxiv_mapping.get(category)

    # get the category abbreviation associated with category selected in category input field
    category_abbreviation = category_data.get('category_abbreviation')
    
    # based on if a subcategory is selected, get the data endpoint to pass to the RSS feed url
    if subcategory:
        subcategory_abbreviation = category_data.get('sub_categories').get(subcategory)
        data_endpoint = '.'.join([category_abbreviation, subcategory_abbreviation])
    else:
        data_endpoint = category_abbreviation

    # based on if keywords entered in keywords input field, get the search keywords in the form of a list of keyword tokens
    if search_text:
        search_keywords = search_text.split()
    else:
        search_keywords = []
    
    # load the feed entries associated with requested data endpoint, announce type and search keywords
    entries = load_data(data_endpoint, announce_type, search_keywords)

    # if list of entries is non-null, then display the entries
    # else, print 'entries unavailable' message
    if entries:
        # create a bar to store information associated with the search results
        results_information = st.columns(spec=[6, 2], vertical_alignment='center')
        
        display_total_results = results_information[0] # display total search results in first column of results information bar
        page_selector = results_information[1] # create dropdown menu to select page number in second column of results information bar

        # calculate the total number of pages based on total number of feed entries
        num_pages = ((len(entries) - 1) // FEEDS_PER_PAGE) + 1
        
        # function to format page number
        page_format = lambda i: f'{i + 1}'

        # add field to display total number of search results
        with display_total_results:
            st.markdown(body=f'**Total Search Results:** {len(entries)}')

        # add a dropdown menu to select the page number
        with page_selector:
            page = st.selectbox(label='Page Number: ', options=range(num_pages), format_func=page_format)

        # calculate the first and last indices of feed entries to display on current page
        min_index = page * FEEDS_PER_PAGE
        max_index = min_index + FEEDS_PER_PAGE

        # get the feed entries to display on current page
        paginator = itertools.islice(enumerate(entries), min_index, max_index)

        # iterate through entries in paginator and display each in separate expander containers
        for i, entry in paginator:
            with st.expander(label=entry.get('title')):
                st.write('Authors: ', entry.get('author'))
                
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