import streamlit as st
from rag_pipeline_qa import invoke_rag_pipeline_qa
from pipeline_summary import invoke_pipeline_summary
from config import chapter_to_title_mappers
import os
import json
from utilities import set_png_as_page_bg



def main():
    st.set_page_config(page_title="Book Companion", page_icon=":memo:", layout="wide")
    st.markdown(
        """
        <style>
        .stSelectbox label, .stTextInput label, .stRadio label {
            color: white !important;
            font-size: 3.0em !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.write(
        f'<h1 style="color: white; text-align: center;">Book Companion</h1>',
        unsafe_allow_html=True
    )
    set_png_as_page_bg('images/background.jpg')
    # st.title("Book Companion")
    
    st.sidebar.title("Navigation")
    selected_tab = st.sidebar.radio("Go to", ["Home", "Q&A"])

    chapter_to_title_mapper = None
    book_name = None
    chapters_dict = None
    chapter_options = None
    selected_book = None
    if selected_tab == "Home":
        st.write('<h1 style="color:white;">Please select a book!</h1>', unsafe_allow_html=True)
        # st.header("Please select a book!")
        selected_book = st.selectbox(
        "Select Book:",
        [
            "Programming Python",
            "Vikings",
            "Introduction to ML",
        ],
    )
        st.session_state.selected_book = selected_book
        
    if selected_tab == "Q&A":
        st.write('<h1 style="color:white;">Fire away your queries below!</h1>', unsafe_allow_html=True)
        if st.session_state.selected_book is not None:
            chapter_to_title_mapper = chapter_to_title_mappers[st.session_state.selected_book]
            chapters_dict = json.load(open(f'intermediate_files/{st.session_state.selected_book}.json','r'))
            chapter_options = [
                f"{num}: {name}" for num, name in chapter_to_title_mapper.items()
                ]
            
            selected_chapter_option = st.selectbox("Select Chapter:", chapter_options)
            st.session_state.selected_chapter_no = str(
                selected_chapter_option.split(":")[0]
            )

            if st.session_state.selected_chapter_no is not None:
                chapter_text = chapters_dict[st.session_state.selected_chapter_no]
                st.write('<h1 style="color:white;">Chapter Content</h1>', unsafe_allow_html=True)
                with st.expander('View Chapter Content'):
                    st.markdown(
                            f"""
                            <div style="
                                height: 400px; 
                                overflow-y: scroll; 
                                border: 1px solid #ccc; 
                                padding: 10px; 
                                background-color: white;
                                color: black; /* Ensure text is visible */
                            ">
                            {chapter_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.write('<h1 style="color:white;">Ask a Question</h1>', unsafe_allow_html=True)
                
                user_question = st.text_input("Enter your question here:")
                get_answer = st.button("Get Answer")

                if user_question and get_answer:
                    with st.spinner("Processing your question..."):
                        answer = invoke_rag_pipeline_qa(user_question,st.session_state.selected_book,st.session_state.selected_chapter_no)
                        # answer = json.load(open('intermediate_files/qa_output.json','r'))
                    with st.expander("View Answer"):
                        st.write(answer)
            st.write('<h1 style="color:white;">Summary</h1>', unsafe_allow_html=True)
            st.markdown("""
                    <style>
                    /* Style the slider label text to be white */
                    .css-1wa3q6a.edgvbvh3 {
                        color: white;
                    }
                    /* Style the slider input text to be white */
                    .css-1y4p8pa.edgvbvh3 {
                        color: white;
                    }
                    </style>
                    """, unsafe_allow_html=True)
            st.session_state.num_words = st.slider("Select the number of words in the summary", 50, 200, 50)

            generate_summary = st.button('Generate Summary')
            if generate_summary:
                with st.spinner('Generating Summary...'):
                    context = chapters_dict[st.session_state.selected_chapter_no]
                    summarized_text =invoke_pipeline_summary(context, st.session_state.num_words)
                with st.expander("View Summary"):
                    st.markdown(
                            f"""
                            <div style="
                                height: 400px; 
                                overflow-y: scroll; 
                                border: 1px solid #ccc; 
                                padding: 10px; 
                                background-color: white;
                                color: black; /* Ensure text is visible */
                            ">
                            {summarized_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.write(
                "Please select a book from the home tab!"
            )  #


if __name__ == "__main__":
    main()

