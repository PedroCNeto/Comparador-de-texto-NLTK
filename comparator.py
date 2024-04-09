import nltk
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

with open("texts/text1.txt", "r", encoding="UTF-8") as f:
    texto1Bruto = f.read()
with open("texts/text2.txt", "r", encoding="UTF-8") as f:
    texto2Bruto = f.read()

text1Tokens = tokenizer.tokenize(texto1Bruto)

listaStopWords = nltk.corpus.stopwords.words("portuguese")

text1Filtrado = [w.lower() for w in text1Tokens if  w not in listaStopWords]

frequenciaTexto1 = nltk.FreqDist(text1Filtrado)

print(frequenciaTexto1.most_common())


#tokens = nltk.word_tokenize(texto)
#print(tokens)