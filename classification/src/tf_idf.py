import pandas as pd
import numpy as np
import ast

def convert_text_list(texts):
  texts = ast.literal_eval(texts)
  return [text for text in texts]

def calc_TF(document):
  # counts the number of times the word appears in review
  TF_dict = {}
  for term in document:
      if term in TF_dict:
        TF_dict[term] += 1
      else:
        TF_dict[term] = 1

  # Computes tf for each word
  for term in TF_dict:
      TF_dict[term] = TF_dict[term] / len(document)
  return TF_dict


def calc_DF(tfDict):
    count_DF = {}
    # Run through each document's tf dictionary and increment countDict's (term, doc) pair
    for document in tfDict:
        for term in document:
            if term in count_DF:
                count_DF[term] += 1
            else:
                count_DF[term] = 1
    return count_DF

def calc_IDF(__n_document, __DF):
    IDF_Dict = {}
    for term in __DF:
        IDF_Dict[term] = np.log(__n_document / (__DF[term] + 1))
    return IDF_Dict

def calc_TF_IDF(TF):
    TF_IDF_Dict = {}
    #For each word in the review, we multiply its tf and its idf.
    for key in TF:
        TF_IDF_Dict[key] = TF[key] * IDF[key]
    return TF_IDF_Dict

if __name__ == "__main__":
  news_data = pd.read_csv('text_preprocessing.csv')
  news_data['news_list'] = news_data['title_tokens_stemmed'].apply(convert_text_list)
  news_data["TF_dict"] = news_data['news_list'].apply(calc_TF)
  # print(news_data['TF_dict'].head())
  index = 10

  # print('%20s' % "term", "\t", "TF\n")
  # for key in news_data["TF_dict"][index]:
  #     print('%20s' % key, "\t", news_data["TF_dict"][index][key])

  DF = calc_DF(news_data["TF_dict"])
  n_document = len(news_data)
  IDF = calc_IDF(n_document, DF)

  news_data["TF-IDF_dict"] = news_data["TF_dict"].apply(calc_TF_IDF)

  # Check TF-IDF result
  index = 1

  print('%20s' % "term", "\t", '%10s' % "TF", "\t", '%20s' % "TF-IDF\n")
  for key in news_data["TF-IDF_dict"][index]:
      print('%20s' % key, "\t", news_data["TF_dict"][index][key] ,"\t" , news_data["TF-IDF_dict"][index][key])