
from converter.Converter import Converter, Data

from converter.office_command import call_soffice

class PDFtoJPEG(Converter):

	def get_opname(self):
		return "pdf_to_jpeg"

	def convert_one(self, pdf) -> [str]:
		return [Data(call_soffice(str(pdf), self.wd, "jpeg", log=self.log))]
