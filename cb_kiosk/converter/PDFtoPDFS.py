import os
import glob

from converter.Converter import Converter, Data

from util import execute_command

class PDFtoPDFS(Converter):

	def get_opname(self) -> str:
		return "split_pdf"

	def convert_one(self, pdf) -> [str]:
		pdf = str(pdf)
		basename = os.path.basename(pdf)
		file_wo_ext = basename[:-4]

		cmd = [
			"./pdfsplit.sh",
			f"{str(pdf)}",
			"1",
			f"{self.wd}/",
		]

		execute_command(cmd)

		outfiles = list(glob.glob(f"{self.wd}/{file_wo_ext}_*.pdf"))
		nb_outfiles = len(list(glob.glob(f"{self.wd}/{file_wo_ext}_*.pdf")))

		if nb_outfiles == 0:
			raise FileNotFoundError(f"Split of {pdf} into pages failed")
		else:
			outfiles = [ Data(f"{self.wd}/{file_wo_ext}_{i}.pdf") for i, _ in enumerate(outfiles) ]
			self.log.debug(f"Generated {outfiles}")

		return outfiles
