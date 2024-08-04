import streamlit as st
from rag_pipeline_qa import invoke_rag_pipeline_qa
from config import chapter_to_title_mappers
import os
import json
from utilities import set_png_as_page_bg



def main():
    st.set_page_config(page_title="Book Companion", page_icon=":memo:", layout="wide")

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
        st.header("Please select a book!")
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
        st.header("Fire away your queries below!")
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
                st.subheader("Chapter Content")
                with st.expander("View Chapter Content"):
                    st.write(
                        f"""
                        <div style="height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
                        {chapter_text}</div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.subheader("Ask a Question")
                user_question = st.text_input("Enter your question here:")
                get_answer = st.button("Get Answer")

                if user_question and get_answer:
                    with st.spinner("Processing your question..."):
                        answer = invoke_rag_pipeline_qa(user_question,st.session_state.selected_book,st.session_state.selected_chapter_no)
                        # answer = json.load(open('intermediate_files/qa_output.json','r'))
                    with st.expander("View Answer"):
                        st.write(answer)
        else:
            st.write(
                "Please select a book from the home tab!"
            )  #


if __name__ == "__main__":
    main()
