# Daily Research

Daily Research is a real-time latest research papers reader, built in Python using [Streamlit](https://streamlit.io/). It uses present day RSS feeds from [arXiv](https://arxiv.org/) to fetch metadata about latest research papers published in various scientific fields (Computer Science, Mathematics, Statistics, etc.).

**Important Information**  
- Daily Research displays only those research papers that are mentioned in arXiv's present day RSS feeds. 
- RSS feeds from arXiv are unavailable on Saturdays and Sundays, and on occasional holidays. Therefore, Daily Research will not display any search results on those days.
- To understand the category taxonomy followed by arXiv, refer to this [link](https://arxiv.org/category_taxonomy).
- Some keywords to understand announce types:
    1. new - papers that are released for the first time on arXiv
    2. replace - updated versions of papers that are released
    3. cross - papers that are announced as new to categories that are not their primary category

# Features

1. **Interactive Category Selection:** Easily choose and manage preferred research paper subject categories.
2. **Filter for Search Results:** Refine search results by subject subcategory, announce type and keywords.
3. **Pagination:** Navigate easily through large sets of search results.
4. **Direct Links to Research Paper Website and PDF:** Access the main arXiv website and PDF of the research paper directly from the reader.

# Demo

Checkout the live version of Daily Research (hosted with Streamlit's Community Cloud):  
https://dailyresearch.streamlit.app

# Usage Instructions

1. Select a research paper subject category from the dropdown menu and wait for the search results to load.
2. [Optional Step] Filter the search results by subject subcategory and announce type from the dropdown menu.
3. [Optional Step] Filter the search results by keywords and press `ENTER`.

# Run Locally Instructions

Prerequisite: A latest version of [Python](https://www.python.org/)

To install and run Daily Research in a local Streamlit server on your machine, follow these steps:

1. Clone the repository:
```sh
git clone https://github.com/im-varun/daily-research.git
```

2. Navigate to the project directory:
```sh
cd daily-research
```

3. Install the required dependencies:
```sh
pip install -r requirements.txt
```

4. Run the Streamlit Application:
```sh
streamlit run streamlit_app.py
```

# Disclaimer and License

Any resemblance of the project name to real-world works is purely coincidental. The copyright of all research papers displayed in Daily Research belongs to their respective author(s) or publisher. This project is for educational purposes only.
  
Daily Research © 2024 by Varun Mulchandani is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).