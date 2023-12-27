import os
import shutil
import logging

logger = logging.getLogger(__name__)


class Data:
	def __init__(self, string):
		self.data = string

	def __str__(self):
		return self.data

	def __repr__(self):
		return self.data


class Converter:
	def __init__(self, tmpdir, log : logger = logger):
		self.log : logger = log
		self.tmpdir = tmpdir

	def get_opname(self) -> str:
		return ""

	def convert(self, inputs: [Data]) -> [str]:
		'''
		Handle the creation of path and other
		'''
		self.log.debug(f"Convert {inputs} to {self.get_opname()}")

		wd = os.path.join(self.tmpdir, self.get_opname())
		shutil.rmtree(wd, ignore_errors=True)
		os.mkdir(wd)

		self.log.debug(f"Created {wd}")
		self.wd = wd
		
		outputs = self.convert_list(inputs)

		self.log.debug(f"Converted to {str(outputs)}")

		return outputs

	def convert_one(self, input: Data) -> [str]:
		'''
		Only do the conversion
		'''
		pass

	def convert_list(self, in_datas: [Data]) -> [str]:
		'''
		Loop on files to convert
		'''
		self.log.debug(f"Converting {str(in_datas)}({len(in_datas)})")

		out_datas = []

		for data in in_datas:
			tmp = self.convert_one(data)

			out_datas.extend(tmp)

		return out_datas
