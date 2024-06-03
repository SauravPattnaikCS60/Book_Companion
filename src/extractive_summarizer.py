from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def get_extractive_summary(filename,num_sentences=100):
    LANGUAGE = "english"
    parser = PlaintextParser.from_file(filename, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])


# print(get_extractive_summary('context.txt'))