from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class CustomStemmer:
  def __init__(self, tweet_data):
      self.factory = StemmerFactory()
      self.stemmer = self.factory.create_stemmer()
      self.term_dict = {}
      for document in tweet_data:
        for term in document:
          if term not in self.term_dict:
            self.term_dict[term] = ''

      for term in self.term_dict:
        self.term_dict[term] = self.stemmed_wrapper(term)
        print(term,":" , self.term_dict[term])

  def stemmed_wrapper(self, term):
    return self.stemmer.stem(term)

  def get_stemmed_term(self, document):
    return [self.term_dict[term] for term in document]
  