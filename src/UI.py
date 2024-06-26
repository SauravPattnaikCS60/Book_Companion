import streamlit as st
from pdf_extraction import extract_content
from pipeline_summary import invoke_pipeline_summary,chapter_to_title_mapper
from rag_pipeline_qa import invoke_rag_pipeline_qa
import json


def main():
    st.title("Book Companion")

    chapters_dict = extract_content()  

  
    if 'selected_chapter_no' not in st.session_state:
        st.session_state.selected_chapter_no = 1
    if 'num_words' not in st.session_state:
        st.session_state.num_words = 50
    st.sidebar.title("Navigation")
    selected_tab = st.sidebar.radio("Go to", ["Home", "Summary", "Q&A"])

    if selected_tab == "Home":
        st.header("Home")
        chapter_options = [f"{num}: {name}" for num, name in chapter_to_title_mapper.items()]
        selected_chapter_option = st.selectbox("Select Chapter:", chapter_options)
        st.session_state.selected_chapter_no = int(selected_chapter_option.split(":")[0])

        st.session_state.num_words = st.slider("Select the number of words in the summary", 50, 200, 50)

    if selected_tab == "Summary":
        st.header("Summary")
        if st.session_state.selected_chapter_no is not None:
            chapter_text = chapters_dict[st.session_state.selected_chapter_no]
            with st.spinner('Generating Summary...'):
                summarized_text =invoke_pipeline_summary(st.session_state.selected_chapter_no, st.session_state.num_words) 
                # summarized_text = json.load(open('intermediate_files/summary_output.json','r'))
            
            st.subheader("Chapter Name")
            chapter_name = chapter_to_title_mapper.get(str(st.session_state.selected_chapter_no), "Unknown Chapter")
            st.write(chapter_name)
            st.subheader("Summary")
            with st.expander("View Summary"):
                st.write(summarized_text)
        else:
            st.write("Please select a chapter and the number of words from the Home tab.")

    if selected_tab=="Q&A":
        st.header("Q&A")
        if st.session_state.selected_chapter_no is not None:
            chapter_text = chapters_dict[st.session_state.selected_chapter_no]
            st.subheader("Chapter Content")
            with st.expander("View Chapter Content"):
                st.write(
                    f"""
                    <div style="height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
                    {chapter_text}</div>
                    """,
                    unsafe_allow_html=True
                )

            st.subheader("Ask a Question")
            user_question = st.text_input("Enter your question here:")
            get_answer = st.button('Get Answer')

            if user_question and get_answer:
                with st.spinner('Processing your question...'):
                    answer =invoke_rag_pipeline_qa(user_question)
                    # answer = json.load(open('intermediate_files/qa_output.json','r'))
                with st.expander("View Answer"):
                    st.write(answer)
        else:
            st.write("Please select a chapter and the number of words from the Home tab.")#
    
            

if __name__ == '__main__':
    main()