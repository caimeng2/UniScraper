"""A scraper that works with multiple types of webpages, including html, pdf, word documents, presentation slides, and spreedsheets"""

import pandas as pd
import numpy as np
import re
from ast import literal_eval
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import time
import nltk
import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def tag_visible(element):
    """A helper function to filter visible tags"""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def pdf_to_text(pdf_file):
    """Extract text from pdf file"""
    text_memory_file = io.StringIO()
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, text_memory_file, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(pdf_file):
        interpreter.process_page(page)
    text = text_memory_file.getvalue()
    text_memory_file.close()
    return text

def text_from_url(url):
    """Extract text from web pages"""
    try:
        req = requests.get(url)
        if 'text/html' in req.headers["Content-Type"]:
            driver.get(url)
            time.sleep(15)
            body = driver.page_source
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            text = u" ".join(t.strip() for t in visible_texts)
        elif 'application/pdf' in req.headers["Content-Type"]:
            pdf_memory_file = io.BytesIO()
            pdf_memory_file.write(req.content)
            text = pdf_to_text(pdf_memory_file)
        elif 
        else:
            csv.writer(open("error.csv", "a")).writerow([req.headers["Content-Type"],url])
            text = ""
    except Exception as e:
        csv.writer(open("error.csv", "a")).writerow([e,url])
        text = ""
    return text

def remove_non_eng(text):
    """A helper funtion to remove non-english text"""
    words = set(nltk.corpus.words.words())
    english = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())
    return english

def paragraph_from_text(text, search_string):
    """Get paragraphs containing a keyword with its context"""
    split_text = text.lower().split("\n\n")
    found = False
    previous = ""
    para = []
    for p in split_text:
        # to extract paragraphs containing a keyword and its immediate previous and after paragraphs
        if found:
            para.append(p)
            found = False
        if p.find(search_string.lower()) != -1:
            para.append(previous)
            para.append(p)
            found = True
        else:
            found = False
        previous = p
    para = list(set(para)) # remove duplicates
    para_str = " ".join(para)
    return para_str

def paragraph_from_url(url, search_string):
    """Extract paragraphs from a webpage"""
    web_text = text_from_url(url)
    eng_text = remove_non_eng(web_text)
    para = paragraph_from_text(eng_text, search_string)
    return para

class uniscraper(object):
    """A scraper that works with multiple types of webpages"""
    def __init__(self, url):
        self.url = url
        self.text = text_from_url(url)
        self.english = remove_non_eng(self.text)
    def search(self, string):
        self.para = paragraph_from_text(self.english, string)
        return self.para
