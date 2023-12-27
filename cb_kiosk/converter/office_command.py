import os

from util import execute_command

def call_soffice(input_file, output_dir, output_type, log=None) -> str:
	basename = os.path.basename(input_file)
	file_wo_ext = basename[:-4]

	cmd = [
		"soffice",
		"--headless",
		"--convert-to",
		output_type,
		"--outdir",
		output_dir,
		input_file,
	]

	execute_command(cmd, log=log)

	outfile = f"{output_dir}/{file_wo_ext}.{output_type}"

	if not os.path.isfile(outfile):
		raise FileNotFoundError(f"Conversion of {input_file} to {output_type} {outfile} failed")
	else:
		if log is not None:
			log.debug(f"Generated {outfile}")

	return outfile
