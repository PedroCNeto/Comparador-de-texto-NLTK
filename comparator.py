import nltk
from nltk.tokenize import RegexpTokenizer
import spacy
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import re

nlp = spacy.load("pt_core_news_md")
tokenizer = RegexpTokenizer(r'\w+')

with open("texts/text1.txt", "r", encoding="UTF-8") as f:
    texto1Bruto = f.read()
with open("texts/text2.txt", "r", encoding="UTF-8") as f:
    texto2Bruto = f.read()

listaStopWords = nltk.corpus.stopwords.words("portuguese")

def keywordsGetter(bruteText):
    #Tira os \n do texto
    bruteTextNoNewLine = re.sub('\n', '', bruteText)
    
    #Tokeniza com o SpaCy
    textTokens = nlp(bruteTextNoNewLine)
    
    #Tira as pontuacoes
    textTokensNoPunct = [w for w in textTokens if not w.is_punct]

    #Tira as stopwords
    textTokensNoStopWords = [w for w in textTokensNoPunct if  w.orth_.lower() not in listaStopWords]

    #Faz o lemmer em todas as palavras que sobraram
    textFiltrado = [w.lemma_ for w in textTokensNoStopWords]

    #Para participar do array final a palavra tem que ter 0.75% (testes feitos em textos pequenos para textos maiores a % pode ser maior) de aparição no texto
    size = len(textFiltrado)
    porcentagem = size * 0.0075

    #Verifica a frequencia das palavras
    frequenciaTexto = nltk.FreqDist(textFiltrado)
    returnArray = []
    for i in frequenciaTexto:
        if frequenciaTexto[i] >= porcentagem:
            returnArray.append(i) 
    return returnArray

def porcentCalc(size1, size2, keys):
    #Calculo de % baseado na quantidade de keywords encontradas nos 2 textos
    porcent1 = keys*100 / size1
    porcent2 = keys*100 / size2
    porcentTotal = (porcent1 + porcent2) / 2
    if(porcentTotal > 100):
        porcentTotal = 100
    return porcentTotal

def textComparison(keywords1, keywords2):
    qtdKeys = 0
    for i in keywords1:
        print("----------------------------------")
        print(i)
        #Tira o acento para não bugar no lexico
        palavraSemAcento = normalize('NFKD', i).encode('ASCII','ignore').decode('ASCII')
        print(palavraSemAcento)
        listaSinonimos = getSinonimos(palavraSemAcento)
        print(listaSinonimos)
        #Verifica se achou palavras ou sinonimos no texto todo(pode achar mais de 1 sinonimo por vez)
        for j in keywords2:
            if i == j:
               qtdKeys+=1
               print("Palavra encontrada")
            else:
                for k in listaSinonimos:
                    if k == j:
                        qtdKeys+=1
                        print("Sinonimo encontrado")

    porcentTotal = porcentCalc(len(keywords1), len(keywords2), qtdKeys)
    print("A porcentagem é de " + str("{:.2f}".format(porcentTotal)))

def getSinonimos(palavra):
    #Essa função vai buscar os sinonimos do site Lexico
    url = "https://www.lexico.pt/" + palavra + "/"
    data = requests.get(url)
    soup = BeautifulSoup(data.content,'html.parser')
    #Pega as palavras, que vem em uma string unica
    palavras = soup.find('p', class_=["words-buttons"])
    if palavras != None:
        #Caso a string não seja nula, ele pega o span que contem todos os sinonimos, pois em alguns casos o texto trazia textos extras
        sinonimosString = palavras.find('span')
        #Separa em um array pelas virgulas
        arrayPalavras = sinonimosString.text.split(", ")   
        return arrayPalavras
    else:
        return []

arrayKeyWords1 = keywordsGetter(texto1Bruto)
arrayKeyWords2 = keywordsGetter(texto2Bruto)
print(arrayKeyWords1)

textComparison(arrayKeyWords1, arrayKeyWords2)


