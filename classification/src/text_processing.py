import pandas as pd
import re
import string
from custom_stemmer import CustomStemmer
import swifter

# import word_tokenize & FreqDist from NLTK
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# ----- Tokenizing -----
def remove_news_special(text):
  # remove tab, new line, and back slice
  text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
  # remove non ASCII (emoticon, kanji, .etc)
  text = text.encode('ascii', 'replace').decode('ascii')
  # remove mention, link, hashtag
  text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
  # remove incomplete url
  return text.replace("http://", " ").replace("https://", " ")

#remove number
def remove_number(text):
  return re.sub(r"\d+", "", text)

#remove punctuation
def remove_punctuation(text):
  return text.translate(str.maketrans("", "", string.punctuation))

#remove whitespace leading & trailing
def remove_whitespace_LT(text):
  return text.strip()

#remove multiple whitespace into single whitespace
def remove_whitespace_multiple(text):
    return re.sub('\s+',' ',text)

#remove single char
def remove_single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)

#NLTK word rokenize 
def word_tokenize_wrapper(text):
    return word_tokenize(text)

#NLTK calc frequency distribution
def freqDist_wrapper(text):
    return FreqDist(text)

#stopword removal
def stopwords_removal(words):
  list_stopwords = stopwords.words('indonesian')
  list_stopwords.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                       '&amp', 'yah'])
  list_stopwords = set(list_stopwords)

  return [word for word in words if word not in list_stopwords]

if __name__ == "__main__":
  # nltk.download_shell()
  news_data = pd.read_csv("scrapped_news.csv", encoding = "ISO-8859-1")
  # print(news_data['description'].isnull())
  # print(news_data['description'].isnull())
  news_data['description'] = news_data['description'].apply(remove_news_special)
  # news_data['description'] = news_data['description'].apply(remove_number)
  news_data['description'] = news_data['description'].apply(remove_punctuation)
  news_data['description'] = news_data['description'].apply(remove_whitespace_LT)
  news_data['description'] = news_data['description'].apply(remove_whitespace_multiple)
  news_data['description'] = news_data['description'].apply(remove_single_char)
  news_data['description_tokens'] = news_data['description'].apply(word_tokenize_wrapper)
  news_data['description_tokens_fdist'] = news_data['description_tokens'].apply(freqDist_wrapper)
  news_data['description_tokens_wsw'] = news_data['description_tokens'].apply(freqDist_wrapper)

  stemmer = CustomStemmer(news_data['description_tokens_wsw'])
  news_data['description_tokens_stemmed'] = news_data['description_tokens_wsw'].swifter.apply(stemmer.get_stemmed_term)
  # We will skip normalization word 
  
  news_data.to_csv('text_preprocessing.csv')