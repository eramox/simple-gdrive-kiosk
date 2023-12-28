import os
import glob
from PyPDF2 import PdfWriter, PdfReader

from converter.Converter import Converter, Data

from util import execute_command

class PDFtoPDFS(Converter):

	def get_opname(self) -> str:
		return "split_pdf"

	def convert_one(self, pdf) -> [str]:
		outputs = []
		inputpdf = PdfReader(open(str(pdf), "rb"))

		for i in range(len(inputpdf.pages)):
		    output = PdfWriter()
		    output.add_page(inputpdf.pages[i])
		    
		    name = "document-page%s.pdf" % i
		    with open(name, "wb") as outputStream:
		        output.write(outputStream)

		    outputs.append(Data(name))

		return outputs
