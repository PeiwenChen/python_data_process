
#Author: Peiwen Chen
#Date: Sep 18, 2014


import sys
import getopt
import plotly.plotly as plot 
from plotly.graph_objs import *


def read_blocks(input_file):
	empty_lines = 0
	blocks = []
	for line in open(input_file):
		# check if a new block 
		if not line or line.startswith('Action'):
			if empty_lines == 0:
				blocks.append([])
			empty_lines += 1
		else:
			empty_lines = 0
			blocks[-1].append(line)
	return blocks


def daemon_parser(input_file, outputfile):
	rpd_data = []
	dcd_data = []
	jdhcpd_data = []
	pppd_data = []
	
	for block in read_blocks(input_file):
		# print ' Action!'
		rpd_parsed = False
		dcd_parsed = False
		jdhcpd_parsed = False
		pppd_parsed = False

		for line in block:
			# parse for daemons, rpd, dcd, jdhcpd, pppd
			if not rpd_parsed and line.startswith('rpd'):
				consume = (line.split())[3]
				rpd_data.append(int(consume)) 
				rpd_parsed = True
			elif not dcd_parsed and line.startswith('dcd'):
				consume = (line.split())[3]
				dcd_data.append(int(consume))
				dcd_parsed = True
			elif not jdhcpd_parsed and line.startswith('jdhcpd'):
				consume = (line.split())[3]
				jdhcpd_data.append(int(consume))
				jdhcpd_parsed = True
			elif not pppd_parsed and line.startswith('pppd'):
				consume = (line.split())[3]
				pppd_data.append(int(consume))
				pppd_parsed = True
			elif rpd_parsed and dcd_parsed and jdhcpd_parsed and pppd_parsed:
				# this block read done, move on to next block
				break
			else:
				# skip this line
				continue

	# read all blocks into lists
	output = open(outputfile, 'w')
	output.write('RPD CONSUMED IFSTATES NUMBER\n')
	output.write(str(rpd_data))
	output.write('\nDCD CONSUMED IFSTATES NUMBER\n')
	output.write(str(dcd_data))
	output.write('\nJDHCPD CONSUMED IFSTATES NUMBER\n')
	output.write(str(jdhcpd_data))
	output.write('\nPPPD CONSUMED IFSTATES NUMBER\n')
	output.write(str(pppd_data))
	output.write('\n')
	output.close()

	plot.sign_in('Python-Demo-Account', 'gwt101uhh0')
	xlim = list(range(1,195))	
	trace0 = Scatter(x=xlim, y=rpd_data, mode='markers')
	trace1 = Scatter(x=xlim, y=dcd_data, mode='markerss')
	trace2 = Scatter(x=xlim, y=jdhcpd_data, mode='lines')
	trace3 = Scatter(x=xlim, y=pppd_data, mode='lines')
	data = Data([trace0, trace1, trace2, trace3])
	unique_url = plot.plot(data, filename = 'daemons consume ifstate ')


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
	daemon_parser(inputfile, outputfile)

if __name__ == "__main__":
	main(sys.argv[1:])	
