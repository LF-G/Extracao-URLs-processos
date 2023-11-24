# Extração de URLs de processos jurídicos

O código extraiURLs.py lê uma base de processos judiciais (documentos HTML) de Tribunais Regionais Eleitorais e imprime numa planilha xlsx todas as URLs contidas nesses processos, juntamente com os contextos (trechos de texto) e os documentos processuais específicos em que essas URLs aparecem. A base está organizada da seguinte maneira: os documentos de um mesmo processo estão reunidos em uma pasta cujo nome é o código desse processo; as pastas dos processos de um determinado TRE estão reunidas em uma pasta cujo nome especifica o TRE (jurisdição) em questão; as pastas de cada um dos TREs (jurisdições) estão reunidas em uma única grande pasta.

O formato de impressão é o seguinte:
Código do processo | Jurisdição | URL | Contexto | Documento

O programa também cria um arquivo com as URLs que foram descartadas durante a análise automatizada.

Além do código extraiURLs.py, este repositório contém:
(1) Uma pasta intitulada "Decisoes", que contém uma amostra de base de processos que o programa é capaz de ler;
(2) Um arquivo intitulado "URLs.xlsx", resultado da execução do programa sobre a base contida em "Decisoes";
(3) Um arquivo de descarte intitulado "descarte.xlsx", também resultado da execução do programa sobre a base contida em "Decisoes".


