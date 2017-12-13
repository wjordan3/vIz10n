from PIL import Image
import subprocess
#output = subprocess.check_output('', shell=True)

def find_problem_images(shell_prompt):
	output = output.splitlines()
	#you normally would not want to use shell=True
	output = subprocess.check_output(shell_prompt, shell=True)
	for file in output:
		try:
			im = Image.open(file)
		except:
			print(file)

find_problem_images('ls wgaScraping/*')
find_problem_images('ls artukscrapingartists/*')
find_problem_images('ls artukscraping/*')
