

def parse_output_for_ui(text):
    answer_block = text.split("Answer:")[1]
    answer_block = answer_block.replace(r'<eos>','')
    return answer_block