import gensim

path = './model/idwiki_word2vec_200_new/idwiki_word2vec_200_new_lower.model'
id_w2v = gensim.models.word2vec.Word2Vec.load(path)
print(id_w2v.most_similar('kriminal'))
