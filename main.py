from collections import defaultdict
from bs4 import BeautifulSoup
import nltk, urllib.request
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

import re
import json

from nltk.tokenize import word_tokenize, sent_tokenize

stopwords =  set(stopwords.words('english'))

default_url  = 'https://en.wikipedia.org/wiki/History_of_Python'


def extract_from_url(url = default_url):
    sentences = []
    content = []

    # extract html
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except:
        return sentences, content

    html_parsed = BeautifulSoup(html,'html.parser') 
    html_data = html_parsed.find_all(['title', 'h1', 'h2', 'h3', 'p'])

    for h in html_data:
        if h.name == 'p':
            text = h.text
            # remove whitespace
            text = re.sub(r'\s+'," ", text)
            
            # split paragraph
            text = sent_tokenize(text)

            # print(text)

            sentences = sentences + text

            content.append({h.name: text})
            
        else:
            content.append({h.name: h.text})

    return sentences, content


def word_tokenizer(sentences):
    all_words = []

    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        
        # also remove stopwords
        words = [word for word in words if word.isalnum() and word not in stopwords]

        all_words += words

    return all_words


def compute_word_frequency(words):
    # compute word frequency
    word_freq = defaultdict(int)
    for word in words:
        word_freq[word] +=1

    return word_freq


def compute_sentence_score(sentences, word_freq):
    # compute sentence scores based on word frequency
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] += word_freq[word]
    
    return sentence_scores


def summarize(sentences):
    sentences = sentences

    words = word_tokenizer(sentences)

    word_freq = compute_word_frequency(words)

    sentence_scores = compute_sentence_score(sentences, word_freq)

    # consider 30% of total sentences
    num_sentences = (len(sentences)) * 0.3
    print("extracted {0} out of {1}".format(int(num_sentences), len(sentences)))

    # select top-rating sentences
    return sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:int(num_sentences)]


def mark_content(top_sentences, content):
    marked_content = content

    for mc in marked_content:
        for key, val in mc.items():
        
            if key == 'p':

                for i in enumerate(top_sentences):
                    for j in enumerate(val):
                        if i[1] == j[1]:
                            
                            # modify sentence string
                            val[j[0]] = ":red["+j[1]+"]"

                            # remove marked sentence 
                            top_sentences.remove(i[1])

    return marked_content


def main(url = default_url):
    sentences, content = extract_from_url(url)

    top_sentences = summarize(sentences)

    marked_content = mark_content(top_sentences, content)

    # print(json.dumps(marked_content))
    return marked_content
