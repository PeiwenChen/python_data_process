
#Author: Peiwen Chen
#Date: Sep 22, 2014


import sys
import getopt

import plotly.plotly as plot 
from plotly.graph_objs import *


def read_blocks(input_file):
	"""
	read the *.top file into blocks
	"""
	empty_lines = 0
	blocks = []
	for line in open(input_file):
		# check if a new block 
		if not line or line.startswith('last'):
			if empty_lines == 0:
				blocks.append([])
			empty_lines += 1
		else:
			empty_lines = 0
			blocks[-1].append(line)
	return blocks


def parse_daemons(input_file, outputfile):
	"""
	parsing the *.top file to read the WCPU value for daemons and plot
	"""
	daemon_name = ['chassisd', 'l2ald', 'top', 'dcd', 'mib2d', 'rpd', 'dfwd', 
		    'eventd', 'shm-rtsdbd', 'jdhcpd', 'cosd', 'snmpd', 'rmopd',
		    'cfmd', 'l2cpd', 'pppd', 'dfcd', 'pfed']
	daemons_dict = {} 

	for block in read_blocks(input_file):
		for line in block:
			li =line.split()
			if 'root' in li:
			    # parse for daemons
			    name = str(li[-1])
			    # debugging: print "name is %s " %name
			    for n in daemon_name:
				if n == name:
				    if not name in daemons_dict:
					daemons_dict[name] = []
				    # debugging: print "add wcpu %s to daemon %s " %( li[-2], n)
				    daemons_dict[name].append(float(li[-2].strip('%')))
				    break
	# debugging: printing the dict
	"""
	for k, v in daemons_dict.items():
	    print "key is %s, the length of value is %d" %(k, len(v))
	    print k, v
	"""   
	daemons_no = len(daemons_dict.keys())
	print " There are %d processes tracking " %daemons_no
	
	return daemons_dict

def plot_daemons(daemons_dict):
	"""
	plor for daemons_dict with plotly
	"""
	
	# specify the color for daemons
	color_dict = {'chassisd':'#ff1493', 'l2ald':'#daa520', 'top':'#8b0000', 'dcd':'#ff00ff', 
		'mib2d':'#8b008b', 'rpd':'#00ff7f', 'dfwd':'#006400', 'eventd':'##008b8b', 
		'shm-rtsdbd':'#00ffff', 'jdhcpd':'#1e90ff', 'cosd':'0000ff', 'snmpd':'0000FF',
		'rmopd':'#708090', 'cfmd':'#d8bfd8', 'l2cpd':'#faa460', 'pppd':'#ffd700',
		'dfcd':'#db7093', 'pfed':'#7b68ee'}
	
	max_length = max([len(v) for v in daemons_dict.values()])
	plot.sign_in('Python-Demo-Account', 'gwt101uhh0')
	xlim = list(range(1,max_length+1))	
	traces = []

	for k in daemons_dict.keys():
	    trace = Scatter(x=xlim, y=daemons_dict[k], mode='lines', name=k, marker=Marker(color=color_dict[k]))
	    traces.append(trace)
	
	#data = Data([trace0, trace1, trace2, trace3])
	data = Data(traces)
	unique_url = plot.plot(data, filename = 'daemons WCPU ')


def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.pyt -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print 'input file is " ', inputfile
	print 'output file is " ', outputfile 
	d_dict = parse_daemons(inputfile, outputfile)
	plot_daemons(d_dict)

if __name__ == "__main__":
	main(sys.argv[1:])	
