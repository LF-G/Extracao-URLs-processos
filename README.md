# extracao_dados_processos

O código extraiURLs.py lê uma base de processos judiciais (documentos HTML) de Tribunais Regionais Eleitorais e imprime numa planilha .xlsx todas as URLs contidas nesses processos, juntamente com os contextos (trechos de texto) e os documentos processuais específicos em que essas URLs aparecem. A base está organizada da seguinte maneira: os documentos de um mesmo processo estão reunidos em uma pasta cujo nome é o código desse processo; as pastas dos processos de um determinado TRE estão reunidas em uma pasta cujo nome especifica o TRE (jurisdição) em questão; as pastas de cada um dos TREs (jurisdições) estão reunidas em uma única grande pasta.
O  formato de impressão é o seguinte:
Código do processo | Jurisdição | URL | Contexto | Documento
