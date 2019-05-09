import exec_manager
import time


def getAvgTime(objFile, n_its, n_threads, kargs, execution_manager):
	exec_times = []

	for _ in range(n_its):
		then = time.time()
		# os.system("./{} {} {}".format(objFile, kargs, n_threads))
		execution_manager.run(objFile, n_threads, kargs)
		now = time.time()
		exec_times.append(now-then)

	avg = sum(exec_times)/n_its
	var = sum([(t - avg)**2 for t in exec_times])/max(1,n_its-1) # takes the max to avoid division by zero
	std_dev = var ** (1/2)

	return avg, var, std_dev

def runMultiple(infile, n_its, max_t, hthreads, kargs, execution_manager):
	threads = list(range(1,max_t+1)) + hthreads
	results = {}
	statistics = {}

	for i in threads:
		avg, var, std_dev = getAvgTime(infile,n_its,i,kargs,execution_manager)
		results[str(i)] = avg
		statistics[str(i)] = {"average":avg, "variance":var, "standart deviation":std_dev}

	return results, statistics
	

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

	parser.add_argument('-c', dest='InfoFile', type=str, default="",
	                    help='File for informing a different compilation and execution method.')

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

	manager = exec_manager.my_runner(args.InfoFile)

	if not args.is_compiled:
		# filename = infile[:infile.rindex('.')]
		# os.system("gcc {} -fopenmp -o {}".format(infile,filename))
		# infile = filename

		infile = manager.compile(infile)


	results = runMultiple(infile,n_its,max_t,hthreads,kargs, manager)
	avg_time = results[0]
	statistics = results[1]

	with open(infile+"_results.json","w") as outfile:
		json.dump(
			avg_time,
			outfile
		)

	with open(infile+"_statistics.json","w") as outfile:
		json.dump(
			statistics,
			outfile
		)
	print ("Successfully wrote files '{0}_results.json' and '{0}_statistics.json'!".format(infile))