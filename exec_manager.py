import os

class my_runner:
	def __init__(self, filename = ""):
		if filename == "":
			self.compiler = "gcc {} -fopenmp -o {}"
			self.runner = "./{} {} {}"
			return

		with open(filename, 'r') as infile:
			lines = infile.read().split('\n')
			lines = [line for line in lines if len(line) > 0]

		self.compiler = lines[0]
		self.runner = lines[1]

	def compile(self, filename):
		objectfile = filename[:filename.rindex('.')]
		print (self.compiler.format(filename,objectfile))
		os.system(self.compiler.format(filename,objectfile))
		return objectfile

	def run(self, filename, n_procs, kargs):
		os.system(self.runner.format(filename, kargs, n_procs))