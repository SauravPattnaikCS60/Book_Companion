import pymupdf

filepath = 'data/book.pdf'

doc = pymupdf.open(filepath)
chapter_numbers = tuple([str(number) for number in range(0,30)])

def identify_new_chapter(content):
    if len(content) == 0:
        return False
    if content.startswith(chapter_numbers):
        return True

def extract_content():
    chapter_wise_content = {}
    chapter_count = 0
    prev_chapter = None
    chapter_content = ""
    for page in doc:
        content = page.get_text()
        content = content.strip()

        if identify_new_chapter(content) and prev_chapter is None:
            chapter_content += content
            prev_chapter = chapter_count
        
        if identify_new_chapter(content) and prev_chapter != None:
            chapter_wise_content[prev_chapter] = chapter_content
            prev_chapter += 1
            chapter_content = ""
        
        chapter_content += content
    
    return chapter_wise_content



