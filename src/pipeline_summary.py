from langchain import vectorstores as vs
import json
from langchain import PromptTemplate
from nltk.tokenize import sent_tokenize
from extractive_summarizer import get_extractive_summary
import re
import warnings
from load_model_and_generate_response import generate_response
from output_parsing import parse_output_for_ui
warnings.filterwarnings('ignore')

chapter_to_title_mapper={
'1':'How to Build a Universe',
'2':'Welcome to the Solar System ',
'3':'The Reverend Evans\'s Universe',
'4':'The Measure of Things',
'5':'The Stone-Breakers',
'6':'Science Red in Tooth and Claw',
'7':'Elemental Matters',
'8':'Einstein\'s Universe',
'9':'The Mighty Atom',
'10':'Getting the Lead Out',
'11':'Muster Mark\'s Quarks',
'12':'The Earth Moves',
'13':'Bang!',
'14':'The Fire Below',
'15':'Dangerous Beauty',
'16':'Lonely Planet',
'17':'Into the Troposphere',
'18':'THE BOUNDING MAIN',
'19':'THE RISE OF LIFE',
'20':'SMALL WORLD',
'21':'LIFE GOES ON',
'22':'GOOD-BYE TO ALL THAT',
'23':'THE RICHNESS OF BEING',
'24':'CELLS',
'25':'DARWIN’S SINGULAR NOTION',
'26':'THE STUFF OF LIFE',
'27':'Ice Time',
'28':'The Mysterious Biped',
'29':'THE RESTLESS APE',
'30':'GOOD-BYE'   
}
def preprocess_text(text):
    text = text.lower()
    text = re.sub("[^a-z0-9]"," ",text)
    text = re.sub("(\s)+"," ",text)
    return text


def get_prompt(context, summary_words):
    query = f'Summarize the above text in {summary_words} words.'
    template = f'''You are an English literature expert who has solid ability of explaining complex things in a simple manner.

    Context: {context}
    
    Question: {query}

    Answer:'''
    prompt_template = PromptTemplate(
    input_variables=["query","context"],
    template=template)
    prompt = prompt_template.format(query=query,context=context)
    return prompt

def invoke_pipeline_summary(chapter_number, summary_words=50):
    chapter_wise_content = json.load(open('intermediate_files/chapter_wise_content.json','r'))
    context = chapter_wise_content[str(chapter_number)]
    num_sentences = len(sent_tokenize(context))
    num_sentences = min(100,num_sentences//4) ## used for extractive summary module
    json.dump(context, open('intermediate_files/summary_context.txt','w'))
    clean_context = preprocess_text(get_extractive_summary('intermediate_files/summary_context.txt',num_sentences))
    prompt = get_prompt(clean_context,summary_words)
    json.dump(prompt, open('intermediate_files/summary_prompt.txt','w'))
    output = generate_response(prompt, summary_words)
    json.dump(output, open('intermediate_files/summary_output.json','w'))
    output = parse_output_for_ui(output)
    return output

if __name__ == '__main__':
    chapter_number = "6"
    print(f'Chapter invoked : {chapter_to_title_mapper[str(chapter_number)]}')
    print(invoke_pipeline_summary(chapter_number,250))