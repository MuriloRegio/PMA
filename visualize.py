import plotly
import plotly.graph_objs as go
import sys

def readfile(filename):
	with open(filename, 'r') as infile:
		data = eval(infile.read())
	return data

def readFileList(files):
	data = {}
	
	for filename in args.file:
		for k,v in readfile(filename).items():
			if k not in data:
				data[k] = []
			data[k].append(v)
	return data

def proccessData(data):
	base = data["1"]

	from copy import copy
	tmp = copy(data)

	for k,vList in tmp.items():
		i = int(k)

		del data[k]

		if k == "1":
			key = k+" thread"
		else:
			key = k+" threads"

		data[key] = []

		for n,v in enumerate(vList):
			spup = base[n]/v
			expect = i
			eff = spup/i

			data[key].append((eff,spup,expect))


def draw(data):
	labels = sorted(list(data), key = lambda x : int(x.split(' ')[0]))

	execs = zip(*[data[k] for k in labels])
	plot_data = []

	for i, singular_data in enumerate(execs):
		i+=1

		y = zip(*singular_data)
		y,y1,y2 = map(list,y)

		plot_data.append(go.Scatter(x=labels, y=y1,name='Real Speed-up (execution {})'.format(i)))
		plot_data.append(go.Bar(x=labels, y=y,yaxis='y2',name='Efficiency (execution {})'.format(i)))

	plot_data.append(go.Scatter(x=labels, y=y2,name='Expected Speed-up'))

	layout = go.Layout(
	    title='Parallelization Efficiency Analysis',
	    xaxis=dict(
	        title='Number of Threads',
        	showgrid=False,
	        dtick=1
	    ),
	    yaxis=dict(
	        title='Speed-up',
	        overlaying='y2',
        	showgrid=False,
	        dtick=1
	    ),
	    yaxis2=dict(
	        title='Efficiency',
	        side='right',
	        range=[0, 1],
	        dtick=0.25
	    )
	)

	return go.Figure(data=plot_data, layout=layout)


if __name__ == "__main__":
	import argparse
	import plotly.io as pio

	parser = argparse.ArgumentParser(description="")

	parser.add_argument('file', metavar='FileName', type=str, nargs="+",
	            help='The path to the json files that contains the execution info.')

	args = parser.parse_args()

	data = readFileList(args.file)

	proccessData(data)
	fig = draw(data)
	plotly.offline.plot(fig, filename='efficiency_graph.html', auto_open=False)