from converter.Converter import Converter, Data

from converter.office_command import call_soffice

class PPTtoPDF(Converter):

	def get_opname(self):
		return "ppt_to_pdf"

	def convert_one(self, presentation: str) -> [str]:
		return [Data(call_soffice(str(presentation), self.wd, "pdf", log=self.log))]
