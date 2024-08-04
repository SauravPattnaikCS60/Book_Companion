import pymupdf
from config import *
import json

def identify_new_chapter(content, chapter_numbers):
    if len(content) == 0:
        return False
    if content.startswith(chapter_numbers):
        return True


def extract_content(filepath, chapter_numbers):
    doc = pymupdf.open(filepath)
    chapter_wise_content = {}
    chapter_count = 0
    prev_chapter = None
    chapter_content = ""
    for page in doc:
        content = page.get_text()
        content = content.strip()
        if identify_new_chapter(content, chapter_numbers) and prev_chapter is None:
            chapter_content += content
            prev_chapter = chapter_count

        if identify_new_chapter(content, chapter_numbers) and prev_chapter != None:
            chapter_wise_content[prev_chapter] = chapter_content
            prev_chapter += 1
            chapter_content = ""

        chapter_content += content

    return chapter_wise_content


if __name__ == '__main__':
    books_filenames = ["Programming Python", "Vikings", "Introduction to ML", "A Short History of Nearly Everything"]

    for book in books_filenames:
        filepath = 'data/' + book_file_mapping[book]
        chapter_numbers = chapter_numbers_mapper[book]
        result = extract_content(filepath, chapter_numbers)
        json.dump(result, open(f'intermediate_files/{book}.json','w'))