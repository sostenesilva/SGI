from docx import Document, document, table
from python_docx_replace import docx_replace

document = Document("F:\PROGRAMAÇÃO\SGI - Sistema de Gerenciamento de Informações\media\MODELO ORDEM DE FORNECIMENTO.docx")

tabela = document.tables[0]
row = tabela.add_row().cells
row[0].text = 'teste'
row[1].text = 'teste'
row[2].text = 'teste'
row[3].text = 'teste'
row[4].text = 'teste'
row[5].text = 'teste'

mydict = {
    'objeto': 'teste',
    'contrato': '000/2024',
    'processo': '000/2024',
}

docx_replace(document, **mydict )

document.save('teste.docx')