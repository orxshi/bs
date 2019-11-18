from docx import Document
import re

document = Document()
#document.add_heading(i, 0)
myfile = open('output.txt').read()
p = document.add_paragraph(myfile)
document.save('word.docx')
