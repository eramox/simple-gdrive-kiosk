import logging
import subprocess

logger = logging.getLogger(__name__)

def execute_command(cmd: [str], env = None, log = logger):
	'''
	Execute a command in shell, retreving the error code and the output
	'''
	log.info(f"Executing {cmd}")

	result: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, env=env)

	if result.returncode != 0:
		debuglog = f"\n{result.stdout=}\n{result.stderr=}"
		agreg = " ".join(w for w in cmd)
		raise ValueError(f"Command [{agreg}], failed: {debuglog}")
	else:
		log.debug(f"{result.stdout=}")

	log.info(f"Command succeeded")

	return result.returncode, result.stdout, result.stderr

def background_command(cmd: [str], env = None, log = logger):
	'''
	Execute a command in shell, retreving the error code and the output
	'''
	log.info(f"Background {cmd}")

	process = subprocess.Popen(cmd, env=env)

	return process.pid


import time

def informed_delay(seconds: int, reason: str, logger: logging.Logger = logger) -> None:
	logger.info(f"Delay {seconds} seconds: {reason}")
	time.sleep(seconds)
	logger.info(f"Woke up from: {reason}")
