import gensim
# import pandas as pd
import csv

path = './idwiki_word2vec_200_new_lower.model'
id_w2v = gensim.models.word2vec.Word2Vec.load(path)


def nextproses(kata):
    tes = id_w2v.wv.most_similar(kata)
    arr = []

    for x in range(len(tes)):
        arr.append(tes[x][0])

    return(arr)


def similar(kata, proseske):
    tes = id_w2v.wv.most_similar(kata)
    arr = []

    # proses masukin ke csv

    f = open('tes2.csv', 'a', encoding='UTF8', newline='')

    for x in range(len(tes)):
        arr.append(tes[x][0])

    writer = csv.writer(f)
    writer.writerow([str(proseske), kata, tes])

    f.close()

    return(arr)


def tree(arr, proseske):
    hasil = []
    for x in range(len(arr)):
        for y in range(10):
            tes = similar(arr[x][y], proseske)
            hasil.append(tes)
    return(hasil)


if __name__ == "__main__":

    path = './idwiki_word2vec_200_new_lower.model'
    id_w2v = gensim.models.word2vec.Word2Vec.load(path)

    # setelah proses pertama ini di comen sampe
    # f = open('tes2.csv', 'w', encoding='UTF8',)

    # writer = csv.writer(f)
    # writer.writerow(['tingkat setelah parent', 'parent', 'similarity'])

    # f.close()
    # sini

    x = 1

    # ini buat tes pertaman
    tes = similar('korban', x)

    # ini tes kedua dan seterusnya
    # print("kecelakan")
    # tes = nextproses('korban')  # selanjutnya 2 di bawah kesialan ini

    data = []
    data.append(tes)

    # ini ingin mulai proses dari angka brp

    while(True):

        # ini mau sampe proses ke berapa di looping
        if(x < 4):

            # ini setelah proses satu pindah ke atas x=x+1
            coba = tree(data, x)

            # setelah proses pertama ini pindah ke bawah coba = tree .....
            x = x+1

            data = coba
            print(x)
            continue
        else:
            break
