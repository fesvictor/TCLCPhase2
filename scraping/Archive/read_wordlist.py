# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 17:23:29 2017

@author: Gary
"""

def read_wordlist():
    word_list = []
    with open ("scraper/political parties and figures.txt", 'r') as f:
        for word in f:
            if (word != "\n"):
                word_list.append(word.strip())
    with open ("scraper/political topics.txt", 'r') as f:
        for word in f:
            if (word != "\n"):
                word_list.append(word.strip())          
    return word_list