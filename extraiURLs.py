'''
Autor: Luiz Fernando Antonelli Galati
'''

'''
Este código lê uma base de processos judiciais (documentos HTML) de Tribunais Regionais Eleitorais e imprime, numa
planilha .xlsx, todas as URLs contidas nesses processos, juntamente com os contextos (trechos de texto) e os documentos
específicos em que essas URLs aparecem. A base está organizada da seguinte maneira: os documentos de um mesmo processo
estão reunidos em uma pasta cujo nome é o código desse processo; as pastas dos processos de um determinado TRE estão
reunidas em uma pasta cujo nome especifica o TRE (jurisdição) em questão; as pastas de cada um dos TREs (jurisdições) 
estão reunidas em uma única grande pasta.

O  formato de impressão é o seguinte:
Código do processo | Jurisdição | URL | Contexto | Documento
'''


# -*- coding: utf-8 -*-

import os
import time
import re
import xlsxwriter
from urllib.request import urlopen
from bs4 import BeautifulSoup


linhaBlacklist = 1

''' Escreve um cabeçalho na planilha "planilha" '''

def escreveCabecalho (planilha):
    planilha.write (0, 0, "CNJ")
    planilha.write (0, 1, "Jurisdição")
    planilha.write (0, 2, "URL")
    planilha.write (0, 3, "contexto_1")
    planilha.write (0, 4, "documento_1")
    planilha.write (0, 5, "contexto_2")
    planilha.write (0, 6, "documento_2")
    planilha.write (0, 7, "contexto_3")
    planilha.write (0, 8, "documento_3")
    planilha.write (0, 9, "contexto_4")
    planilha.write (0, 10, "documento_4")
    planilha.write (0, 11, "contexto_5")
    planilha.write (0, 12, "documento_5")  


''' Recebe uma URL, contexto "texto" e verifica se a estrutura URL + texto está na lista "lista_estruturas_processo".
Retorna 1 se ele estiver e 0 caso contrário. '''

def estruturaNaLista (URL, texto, lista_estruturas_impressas):
    i = 0
    while (i < len (lista_estruturas_impressas)):
        if (URL == lista_estruturas_impressas[i][0] and texto == lista_estruturas_impressas[i][1]):
            return 1
        i = i + 1
    return 0
    
    
''' Recebe o caminho da pasta de um processo e retorna a lista de links desse processo.                                                                            '''

def montaListaLinksProcesso (caminhoProcesso):
    listaArquivos = os.listdir (caminhoProcesso)
    listaArquivos.sort ()    
    lista_links_processo = []
    
    for k in range (len (listaArquivos)):
        caminhoArquivoAtual = caminhoProcesso + "/" + listaArquivos[k]        
            
        html = urlopen ("file:///" + caminhoArquivoAtual)
        res = BeautifulSoup (html.read (), "html5lib")        
        
        for paragrafo in res.findAll ("p"):
            texto = paragrafo.text
            lista_links_paragrafo = re.findall (r"http[^ ,\n^()\"]*|www[^ ,\n()\"]*|[\w@]*\.com[^ ,\n()\"]*", texto)
            lista_links_processo = lista_links_processo + lista_links_paragrafo
        
    return lista_links_processo


''' Recebe uma lista de links "lista_links_processo" e retorna uma nova lista
"novaLista" que não contém nem links PJE, nem links TRE . '''

def eliminaPJEeTRE (lista_links_processo, novaPlanilha2):
    global linhaBlacklist
    i = 0
    novaLista = []
    global linhaBlacklist
    while (i < len (lista_links_processo)):
        if (lista_links_processo[i].__contains__("pje.") == 1 or lista_links_processo[i].__contains__("tre.") == 1):
            novaPlanilha2.write (linhaBlacklist, 0, lista_links_processo[i])
            linhaBlacklist = linhaBlacklist + 1
        else:
            novaLista.append (lista_links_processo[i])         
        i = i + 1
        
    return novaLista


''' Recebe uma lista de links "lista_links_processo" e retorna uma nova lista
"novaLista" que não contém links que possuam @ . '''

def eliminaArroba (lista_links_processo, novaPlanilha2):
    global linhaBlacklist
    i = 0    
    novaLista = []    
    while (i < len (lista_links_processo)):
        if (lista_links_processo[i].__contains__("@") == 1):
            novaPlanilha2.write (linhaBlacklist, 0, lista_links_processo[i])
            linhaBlacklist = linhaBlacklist + 1
        else:
            novaLista.append (lista_links_processo[i])       
        i = i + 1
        
    return novaLista


''' Recebe uma lista de links "lista_links_processo" e retorna uma nova lista
"novaLista" que contém os links da lista de entrada sem os seguintes sinais
gráficos no final: ponto (.), ponto-e-vírgula (;), aspas simples ('),
aspas duplas ("), sinal de maior (>), espaço ( ) e sinal de fecha colchetes (]).
                                                                             '''

def eliminaSinais (lista_links_processo):
    i = 0
    novaLista = []
    while (i < len (lista_links_processo)):
        string = lista_links_processo[i]
        
        while (string[len (string) - 1] == "." or string[len (string) - 1] == ";" or string[len (string) - 1] == "'" or string[len (string) - 1] == "\"" or string[len (string) - 1] == "/" or string[len (string) - 1] == ">" or string[len (string) - 1] == ' ' or string[len (string) - 1] == "]"):
            novoTam = len (string) - 1
            string = string[0:novoTam]
           
        novaLista.append (string)
        i = i + 1    
    
    return novaLista 


''' Recebe uma lista de links "lista_links_processo" e retorna uma nova lista "novaLista"
que não contém links que possuam "br.com.infox.cliente.home.ProcessoTrfHome" .        '''

def eliminaInfox (lista_links_processo, novaPlanilha2):
    global linhaBlacklist
    i = 0
    novaLista = []
    while (i < len (lista_links_processo)):
        if (lista_links_processo[i].__contains__("br.com.infox.cliente.home.ProcessoTrfHome") == 1):
            novaPlanilha2.write (linhaBlacklist, 0, lista_links_processo[i])
            linhaBlacklist = linhaBlacklist + 1
        else:
            novaLista.append (lista_links_processo[i])       
        i = i + 1
        
    return novaLista  
  

''' Recebe uma lista de links de um processo e elimina dela todos os links repetidos.
                                                                                  '''
def eliminaRepeticoes (lista_links_processo):
    tam = len (lista_links_processo)
    i = 0
    while (i < tam - 1):
        j = i + 1
        while (j < tam):
            if (lista_links_processo[i] == lista_links_processo[j]):
                # desloca todo mundo
                k = j + 1
                while (k < tam):
                    lista_links_processo[k-1] = lista_links_processo[k]
                    k = k + 1
                tam = tam - 1
            else:
                j = j + 1
        i = i + 1
    return tam       


def main ():   
    camDirAtual = os.getcwd ()
    camDirJurisdicoes = camDirAtual + "/Decisoes"

    novoArquivo = xlsxwriter.Workbook ("URLs.xlsx", {'strings_to_urls': False})
    novaPlanilha = novoArquivo.add_worksheet ("URLs")
    escreveCabecalho (novaPlanilha)
    
    novoArquivo2 = xlsxwriter.Workbook ("descarte.xlsx", {'strings_to_urls': False})
    novaPlanilha2 = novoArquivo2.add_worksheet ("descarte")
    
    ultimaLinhaImpressa = 0    
    
    ''' Jurisdições '''
    listaJurisdicoes = os.listdir (camDirJurisdicoes)
    listaJurisdicoes.sort ()
    for i in range (len (listaJurisdicoes)):
        caminhoJurisdicaoAtual = camDirJurisdicoes + "/" + listaJurisdicoes[i]    
        
        ''' Números de processos '''
        listaProcessos = os.listdir (caminhoJurisdicaoAtual)
        listaProcessos.sort ()
        for j in range (len (listaProcessos)):               
            caminhoProcessoAtual = caminhoJurisdicaoAtual + "/" + listaProcessos[j]
            lista_links_processo = montaListaLinksProcesso (caminhoProcessoAtual)
            lista_links_processo = eliminaPJEeTRE (lista_links_processo, novaPlanilha2)
            lista_links_processo = eliminaArroba (lista_links_processo, novaPlanilha2)
            lista_links_processo = eliminaSinais (lista_links_processo)
            lista_links_processo = eliminaInfox (lista_links_processo, novaPlanilha2)
            tamListaLinksProcesso = eliminaRepeticoes (lista_links_processo)     

            if (tamListaLinksProcesso == 0):
                novaPlanilha.write (ultimaLinhaImpressa + 1, 0, listaProcessos[j])
                novaPlanilha.write (ultimaLinhaImpressa + 1, 1, listaJurisdicoes[i])
                novaPlanilha.write (ultimaLinhaImpressa + 1, 2, "URLs não encontradas")
                ultimaLinhaImpressa = ultimaLinhaImpressa + 1
            else:
                lista_estruturas_impressas = []
                lugaresDeImpressao = []
                cont = 0
                while (cont < tamListaLinksProcesso):
                    lugaresDeImpressao.append (3)
                    cont = cont + 1         
                            
                cont = 0
                while (cont < tamListaLinksProcesso):
                    novaPlanilha.write (ultimaLinhaImpressa + cont + 1, 0, listaProcessos[j])
                    novaPlanilha.write (ultimaLinhaImpressa + cont + 1, 1, listaJurisdicoes[i])
                    novaPlanilha.write (ultimaLinhaImpressa + cont + 1, 2, lista_links_processo[cont])                   

                    cont = cont + 1
            
                ''' Arquivos do processo '''
                listaArquivos = os.listdir (caminhoProcessoAtual)
                listaArquivos.sort ()
                for k in range (len (listaArquivos)):                
                    caminhoArquivoAtual = caminhoProcessoAtual + "/" + listaArquivos[k]

                    html = urlopen ("file:///" + caminhoArquivoAtual)
                    res = BeautifulSoup (html.read (), "html5lib")


                    textoAnt = ""
                    for paragrafo in res.findAll ("p"):
                        texto = paragrafo.text
                        cont = 0
                        while (cont < tamListaLinksProcesso):
                            if (texto.__contains__(lista_links_processo[cont]) and estruturaNaLista (lista_links_processo[cont], texto, lista_estruturas_impressas) == 0):
                                # escrita no arquivo
                                novaPlanilha.write (ultimaLinhaImpressa + cont + 1, lugaresDeImpressao[cont], textoAnt + texto)
                                novaPlanilha.write (ultimaLinhaImpressa + cont + 1, lugaresDeImpressao[cont] + 1, listaArquivos[k])
                                lugaresDeImpressao[cont] = lugaresDeImpressao[cont] + 2
                                lista_estruturas_impressas.append ([lista_links_processo[cont], texto])
                            cont = cont + 1
                        textoAnt = texto
            
                ultimaLinhaImpressa = ultimaLinhaImpressa + tamListaLinksProcesso                
       
 
    novoArquivo.close ()
    novoArquivo2.close ()   
    

main ()
