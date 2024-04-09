import nltk
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

with open("texts/text1.txt", "r", encoding="UTF-8") as f:
    texto1Bruto = f.read()
with open("texts/text2.txt", "r", encoding="UTF-8") as f:
    texto2Bruto = f.read()

listaStopWords = nltk.corpus.stopwords.words("portuguese")

def keywordsGetter(bruteText):
    textTokens = tokenizer.tokenize(bruteText)
    textFiltrado = [w.lower() for w in textTokens if  w not in listaStopWords]
    frequenciaTexto = nltk.FreqDist(textFiltrado)
    returnArray = []
    for i in frequenciaTexto:
        if frequenciaTexto[i] >= 2:
            returnArray.append(i)  # Acessando a segunda posição de cada tupla
    return returnArray

arrayKeyWords1 = keywordsGetter(texto1Bruto)
arrayKeyWords2 = keywordsGetter(texto2Bruto)

print(arrayKeyWords1)
print(arrayKeyWords2)

#tokens = nltk.word_tokenize(texto)
#print(tokens)