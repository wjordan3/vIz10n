from PIL import Image
import subprocess
#output = subprocess.check_output('', shell=True)

def find_problem_images(shell_prompt):
	output = output.splitlines()
	output = subprocess.check_output(shell_prompt, shell=True)
	for file in output:
		try:
			im = Image.open(file)
		except:
			print(file)

find_problem_images('ls wgaScraping/*')