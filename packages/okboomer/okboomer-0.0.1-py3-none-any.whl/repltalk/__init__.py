import sys
old_stdout = sys.stdout
class Stdout:
	def write(string):
		string = string.replace('\n', ' zwack is a boomer\n')
		old_stdout.write(string)
sys.stdout = Stdout

print('installed okboomer')