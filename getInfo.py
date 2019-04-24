import os
import time


def getAvgTime(objFile, n_its, n_threads, kargs):
	total = 0
	for _ in range(n_its):
		then = time.time()
		os.system("./{} {} {}".format(objFile, kargs, n_threads))
		now = time.time()
		total += now-then

	return total/n_its

def runMultiple(infile,n_its,max_t,hthreads,kargs):
	threads = list(range(1,max_t+1)) + hthreads
	results = {}

	for i in threads:
		results[str(i)] = getAvgTime(infile,n_its,i,kargs)

	return results
	

if __name__ == "__main__":
	import argparse
	import json

	parser = argparse.ArgumentParser(
		description="""
			Gets the average execution time of a program when ran with different 
			amounts of threads (requires number of threads to be
			the last paramater of the program).
		""",
		epilog="""
		Running examples:
			(1) python getInfo.py mysourcefile; 
			(2) python getInfo.py -o myobjectfile;
			(3) python getInfo.py mysourcefile --kargs "my program parameters";
			(4) python getInfo.py mysourcefile -t 8 --hyper 10 12 14 16
		""")

	parser.add_argument('-o', dest='is_compiled', action='store_true',
	                    help='Flag for informing that the file is object code.')

	parser.add_argument('file', metavar='FileName', type=str,
	                    help='The relative path to the file that contains either source or object code.')

	parser.add_argument("-i", dest='n_its', metavar='max_iterations', type=int, default=5,
	                    help='Number of iterations to take an average of execution time. (default = 5)')

	parser.add_argument("-t", dest='max_t', metavar='max_threads', type=int, default=4,
	                    help='Max number of threads to run the comparation. (default = 4)')

	parser.add_argument('--hyper', dest='hthreads', type=int, nargs='+', default=[],
	                    help='Inform a sequence of hyperthreads to run the test.')

	parser.add_argument('--kargs', dest='kargs', type=str, default = "",
	                    help='Other parameters for the program.')

	args = parser.parse_args()

	infile 	 = args.file
	max_t 	 = args.max_t
	n_its 	 = args.n_its
	hthreads = args.hthreads
	kargs	 = args.kargs

	if n_its < 1:
		print ("Invalid number of iterations!")
		exit(1)

	if max_t < 1:
		print ("Invalid number of threads!")
		exit(1)


	if not args.is_compiled:
		filename = infile[:infile.rindex('.')]

		os.system("gcc {} -fopenmp -o {}".format(infile,filename))

		infile = filename

	with open(infile+"_results.json","w") as outfile:
		json.dump(
			runMultiple(infile,n_its,max_t,hthreads,kargs),
			outfile
		)
	print ("Successfully wrote file '{}'!".format(infile+"_results.json"))