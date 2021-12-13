import pandas as pd
import numpy as np
import ast

def convert_text_list(texts):
  texts = ast.literal_eval(texts)
  return [text for text in texts]

if __name__ == "__main__":
  news_data = pd.read_csv('text_preprocessing.csv')
  news_data['news_list'] = news_data['title_tokens_stemmed'].apply(convert_text_list)
  print(news_data['news_list'])