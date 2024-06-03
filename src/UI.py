import streamlit as st
from pdf_extraction import extract_content
from pipeline_summary import invoke_pipeline_summary,chapter_to_title_mapper
from rag_pipeline_qa import invoke_rag_pipeline_qa


def main():
    st.title("Book Companion")

    chapters_dict =extract_content() 
    selected_chapter = st.selectbox("Select Chapter:", list(chapters_dict.keys()))
    chapter_text = chapters_dict[selected_chapter]
    num_words = st.slider("Select the number of words in the summary", 50, 200, 50)
    #tab1, tab2 = st.tabs(["Summary", "Chapter Content & Q&A"])
    summary_button = st.checkbox('Generate Summary')

    if summary_button:
        
        with st.spinner('Generating Summary...'):
           summarized_text = invoke_pipeline_summary(selected_chapter, num_words)

        # with tab1:
        st.subheader("Chapter Name")
        chapter_name=chapter_to_title_mapper[str(selected_chapter)]
        st.write(chapter_name)
        st.subheader("Summary")
        with st.expander("View Summary"):
            st.write(summarized_text)

    qa_button = st.checkbox('Q/A')
    
    if qa_button:
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
        
        if user_question:
            if get_answer:
                with st.spinner('Processing your question...'):
                    answer = invoke_rag_pipeline_qa(user_question)

                with st.expander("View Answer"):
                    st.write(answer)            

            

if __name__ == '__main__':
    main()