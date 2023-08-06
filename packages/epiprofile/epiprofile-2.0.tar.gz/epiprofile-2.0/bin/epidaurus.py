#!/usr/bin/env python

#import built-in modules
import os,sys
import collections
from numpy import nan_to_num,corrcoef,sqrt,array
from scipy.stats import kendalltau, spearmanr, trim_mean

#import third-party modules
import pyBigWig

from bwpmodule import BED
#changing history to this module

__author__ = "Liguo Wang"
__copyright__ = "Copyright 2013. All rights reserved."
__credits__ = []
__license__ = "MIT"
__version__="2.0"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Production"

usage='''
 Usage:
 
 python3 epidaurus.py config.txt  input.bed  out_prefix

 CONFIG_FILE specification:
 --------------------------

 1) Lines starting with "!" define the parameter-argument pairs. There are 4 parameters:
	!HALF_WINDOW_SIZE 1000         # window size extended to the middle of regions defined in BED file. Default = 1000 (bp)
	!HEAD_ROWS 2000                # Number of rows epidaurus.py will take into calculation. Default = 2000
	!HM_FORMAT pdf                 # Output format. Must be one of ("pdf", "png", "tiff"). Default = pdf
	!DIST_METRIC kendall           # Metric to measure distance between two rows. Must be one of ("pearson", "kendall", "spearman", "euclidean"). Default=kendall

    Parameter and Argument must be space or tab separated.
 
 2) Line starting with '&' define seed bigWig file. Example:
    
    &AR_DHT  /data/Huang_AR_ChIPSeq_MiPlus.normalized.bw
    
    Selection of different "seed" only affects the order of datsets on the heatmap.
 
 3) Lines starting with "%" define bigWig files. Example:
    %P300	/data/Fu_GSM686943_S25.LNCAP-p300-dht.bw
    %H3K4me1	/data/ENCODE_LNCaP_H3K3Me3.bw
    ...
    Name and Path_of_bigwig_file  must be space or tab separated 
    Name should be unique among all bigwig files
    Name should be as concise as possible

  4) lines starting with "#" will be considered as comments and ignored
  5) http://epidaurus.sourceforge.net/
  
 BED_FILE format:
 ----------------
 
  1) At least has 3 column: chrom(str), start(int), end(int)
  2) Genome coordinates must be hg19 (GRch37) based. 
  2) start is 0-based NOT inclusive, end is 1-based and inclusive.
  3) Other columns will be ignored
  4) https://genome.ucsc.edu/FAQ/FAQformat.html#format1
 
 OUTPUT files:
 -------------
 
 1) OUT_PREFIX.r: R script to generate heatmap
 2) OUT_PREFIX.data.xls: data matrix. Each row is a datset, each column is genomic position
 
 Online Manual: http://epidaurus.sourceforge.net/
	'''

def check_id(input_str):
	valid_symbols = 'abcdefghijklmnopqrstuvwxyz0123456789_.'
	tmp = ''
	for i in input_str.strip():
		if i.lower() not in valid_symbols:
			tmp = tmp + '_'
		else:
			tmp = tmp + i
	return tmp

	
def read_cfg(cfg_file):
	'''process config file, extract parameters (arguments) and bigwig files'''
	paras = {'HALF_WINDOW_SIZE':1000,'HEAD_ROWS':2000, 'HM_FORMAT':'pdf', 'DIST_METRIC':'kendall'}
	bw_files = {}
	bw_files_names = collections.defaultdict(int)
	seed_file = {}
	seed_count = 0
	for line in open (cfg_file):
		if not line.strip(): continue
		if line.startswith('#'): continue
		line = line.strip(' \n')
		if line.startswith('!'):
			line = line.lstrip('! ')
			fields = line.split()
			if len(fields) !=2:
				print("Two columns expected: key_word <tab>  value. Format error in " + line, file=sys.stderr)
				continue
			paras[fields[0]] = fields[1]
			
		elif line.startswith('%'):
			line = line.lstrip('% ')
			fields = line.split()
			if len(fields) !=2:
				print("Two columns expected: key_word <tab>  file. Format error in " + line, file=sys.stderr)
				continue
			id = check_id(fields[0])
			bw_files[id] = fields[1]
			bw_files_names[id] += 1
		elif line.startswith('&'):
			seed_count +=1
			line = line.lstrip('& ')
			fields = line.split()
			if len(fields) !=2:
				"Two columns expected: key_word <tab>  file. Format error in " + line
				continue
			id = check_id(fields[0])
			seed_file[id] = fields[1]
		else:
			continue
	if seed_count == 0:
		print("Error in " + cfg_file + ": no seed data found!", file=sys.stderr)
		sys.exit(0)
	elif seed_count >1:
		print("Error in " + cfg_file + ": more than one seed data found!", file=sys.stderr)
		sys.exit(0)
	if len( bw_files) == 0:
		print("Error in " + cfg_file + ": no bigwig files found!", file=sys.stderr)
		sys.exit(0)
	for k,v in list(bw_files.items()):
		#print k + '\t' + v
		if bw_files_names[k] > 1:
			print('Warning: bigWig file name: ' + k + ' was used more than once', file=sys.stderr)
			sys.exit(0)
		if not os.path.exists(v):
			print("Warning: File " + v + " does NOT exist.", file=sys.stderr)
			sys.exit(0)
	return (paras, bw_files, seed_file)
			
			
def profile_bwfile(inbed,bwfile,cut=0.1):
	'''retrieve signal from bigwig file for each entry in input bed file
	return trimmed mean signal
	cut = proportiontocut of trimmed mean
	'''
	bw = pyBigWig.open(bwfile)
	if bw.isBigWig():
		pass
	else:
		print ("%s is NOT a bigwig file!" % bwfile, file=sys.stderr)
		sys.exit(0)
	bw_signals =[]	#list of list
	for chrom, start, end, strand in inbed:	
		try:		
			bw_signal = nan_to_num(bw.values(chrom,int(start),int(end)))
		except:
			continue
		if strand == '-':
			bw_signal = bw_signal[::-1]
			
		if len(bw_signal)==0:
			continue
		else:
			bw_signals.append(bw_signal)
			
	trimMean_sig = trim_mean(array(bw_signals), proportiontocut = cut, axis=0)
	return trimMean_sig


def Rcode_write(dataset,Rfile,colNum,file_prefix, format, half_window):
	'''generate R script for visualization'''
	(tick_pos, tick_lab) = tick_and_marker(half_window)
	ROUT = open(file_prefix + '.r','w')
	names=[]
	datas=[]
	for name, data in dataset:
		names.append(name)
		datas.append(data)
		print(name + ' <- c(' + ','.join([str(i) for i in data]) + ')', file=ROUT)
	print('data_matrix' + ' <- matrix(c(' + ','.join(names) + '), byrow=T, ' +  'ncol=' + str(colNum) + ')', file=ROUT)
	print('rowLabel <- c(' + ','.join(['"' + i + '"' for i in names]) + ')', file=ROUT)
	print('\n', file=ROUT)
	#print >>ROUT, '%s(\"%s.%s\", width=%f, height=%f)' % (format.lower(),file_prefix + ".heatMap",format.lower(), 7, 7.0*len(names)/20)
	print('%s(\"%s.%s\")' % (format.lower(),file_prefix + ".heatMap",format.lower()), file=ROUT)
		
	#print >>ROUT, 'Lab.palette <-colorRampPalette(c("white","red"), space = "rgb")'
	#print >>ROUT, 'colls=Lab.palette(256)'
	print('rc <- cm.colors(ncol(data_matrix))', file=ROUT)
	print('heatmap(data_matrix' + ', scale=c(\"none\"),keep.dendro=F, labRow = rowLabel ' + ',Colv = NA,Rowv = NA,labCol=NA,col=cm.colors(256),margins = c(6, 8),ColSideColors = rc,cexRow=1,cexCol=1,xlab="Distance to peak center (bp)",add.expr=x_axis_expr <- axis(side=1,at=c(%s),labels=c(%s)))' % (','.join([str(i) for i in tick_pos]), ','.join(['"' + str(i) + '"' for i in tick_lab])), file=ROUT)
	print('dev.off()', file=ROUT)
	
	print('\n', file=ROUT)
	#print >>ROUT, '%s(\"%s.%s\", width=%f, height=%f)' % (format.lower(),file_prefix + ".lineGraph",format.lower(), 7, 7.0*len(names)/12)
	print('%s(\"%s.%s\")' % (format.lower(),file_prefix + ".curve",format.lower()), file=ROUT)
	print('par(mfrow=c(%d,1),mar=c(0,3,0,2))' % len(names), file=ROUT)
	print("x=%d:%d" % (-half_window,half_window), file=ROUT)
	#print >>ROUT, "plot(x,%s,type='l',xaxt='n',yaxt='n',lwd=0.8)" % (names[0])
	#print >>ROUT, "text(%d,%d,labels=c(\"%s\"))" % (-half_window, 0.8,names[0])
	#print >>ROUT, "abline(v=0,lty=\"dashed\",lwd=0.5,col=\"red\")"
	
	for i in range(0,len(names)):
		print("plot(x,%s,type='l',xaxt='n',yaxt='n',lwd=0.8,col=\"red\")" % (names[i]), file=ROUT)
		print("text(%d,%f,labels=c(\"%s\"))" % (-half_window, 0.8,names[i]), file=ROUT)
		print("abline(v=0,lty=\"dashed\",lwd=0.5)", file=ROUT)
		#print >>ROUT, "abline(h=0.25,lty=\"dashed\",lwd=0.2)"
		#print >>ROUT, "abline(h=0.5,lty=\"dashed\",lwd=0.2)"
		#print >>ROUT, "abline(h=0.75,lty=\"dashed\",lwd=0.2)"
	print('dev.off()', file=ROUT)
	
def pearson_cor(seed, data):
	corr={}
	sorted_data=[]				
	for seed_name, seed_dat in list(data.items()):
		sorted_data.append((seed_name,seed_dat))
		for fish_name, fish_dat in list(data.items()):
			corr[fish_name] = corrcoef(seed_dat, fish_dat)[0,1]
	
	for k,v in sorted(iter(corr.items()),key= lambda k_v: (k_v[1],k_v[0]),reverse = True):
		#print k + '\t' + str(v)
		sorted_data.append((k, data[k]))	
	
	return sorted_data

def spearman_rho(seed, data):
	corr={}
	sorted_data=[]
	for seed_name, seed_dat in list(seed.items()):
		sorted_data.append((seed_name,seed_dat))
		for fish_name, fish_dat in list(data.items()):
			corr[fish_name] = spearmanr(seed_dat, fish_dat)[0]
	
	for k,v in sorted(iter(corr.items()),key= lambda k_v1: (k_v1[1],k_v1[0]),reverse = True):
		#print k + '\t' + str(v)
		sorted_data.append((k, data[k]))	
	
	return sorted_data
	    
def euclidean_dist(seed, data):
	corr={}
	sorted_data=[]
	for seed_name, seed_dat in list(seed.items()):
		sorted_data.append((seed_name,seed_dat))
		for fish_name, fish_dat in list(data.items()):
			#corr[fish_name] = eudist(seed_dat, fish_dat)
			corr[fish_name] =sqrt(sum((array(seed_dat)-array(fish_dat))**2))
	
	for k,v in sorted(iter(corr.items()),key= lambda k_v2: (k_v2[1],k_v2[0]),reverse = True):
		#print k + '\t' + str(v)
		sorted_data.append((k, data[k]))	
	
	return sorted_data
    
def kendall_tau(seed, data):
	corr={}
	sorted_data=[]
	for seed_name, seed_dat in list(seed.items()):
		sorted_data.append((seed_name,seed_dat))
		for fish_name, fish_dat in list(data.items()):
			corr[fish_name] = kendalltau(seed_dat, fish_dat)[0]
	
	for k,v in sorted(iter(corr.items()),key= lambda k_v3: (k_v3[1],k_v3[0]),reverse = True):
		#print k + '\t' + str(v)
		sorted_data.append((k, data[k]))	
	
	return sorted_data
					 
def tick_and_marker(size):
	'''calculate tick position'''
	step = int(size/100.0 + 0.5) * 100
	tick_labels = list(range(-size,size+1,step))
	tick_pos = list(range(0,size*2+1,step))
	return (tick_pos, tick_labels)		

def main():
	if len(sys.argv) ==2 :
		if sys.argv[1] in ('-v','-V', '--v', '--V','--version'):
			print("Epidaurus %s" % __version__, file=sys.stderr)
			sys.exit(0)
	elif len(sys.argv) ==4:
		cfg_file = sys.argv[1]
		bed_file = sys.argv[2]
		output_prefix = sys.argv[3]
		OUT_DATA = open(output_prefix + '.data.xls','w')
		#OUT_COE = open(output_prefix + '.coefficient.xls','w')
		input_bed = []
		
		other_bw_profile = {}		# raw value
		seed_bw_profile = {}
		other_bw_profile_norm = {}	# normalized value
		seed_bw_profile_norm = {}		
		column_number = set()
		if os.path.exists(cfg_file) and os.path.exists(bed_file):
		
			#reading config file
			print("reading config file: " + cfg_file + '...', file=sys.stderr)
			(parameters,bigwigFiles, seedFile) = read_cfg(cfg_file)
			
			# check parameters
			try:
				if int(parameters['HALF_WINDOW_SIZE']) < 0:
					print("'HALF_WINDOW_SIZE' can't be negative\n", file=sys.stderr)
					sys.exit(0)
			except:
				print("'HALF_WINDOW_SIZE' takes positive integer value.\n", file=sys.stderr)
				sys.exit(0)

			try:
				if int(parameters['HEAD_ROWS']) < 0:
					print("'HEAD_ROWS' can't be negative\n", file=sys.stderr)
					sys.exit(0)
			except:
				print("'HEAD_ROWS' takes positive integer value.\n", file=sys.stderr)
				sys.exit(0)

			try:
				if parameters['HM_FORMAT'] not in ('pdf', 'png','tiff'):
					print("'HM_FORMAT' can only take 'pdf', 'png' or 'tiff'\n", file=sys.stderr)
					sys.exit(0)
			except:
				print("'HM_FORMAT' can only take 'pdf', 'png' or 'tiff'\n", file=sys.stderr)
				sys.exit(0)
			try:
				if parameters['DIST_METRIC'] not in ('pearson', 'kendall', 'spearman', 'euclidean'):
					print("'DIST_METRIC' can only take 'pearson', 'kendall', 'spearman' or 'euclidean'\n", file=sys.stderr)
					sys.exit(0)
			except:
				print("'DIST_METRIC' can only take 'pearson', 'kendall', 'spearman' or 'euclidean'\n", file=sys.stderr)
				sys.exit(0)
			
			# output parameters
			print("\nParameters:", file=sys.stderr)
			for k,v in list(parameters.items()):
				print("%-20s%-10s" % (k,v), file=sys.stderr)
			print(file=sys.stderr)
			
			#reading input bed file
			if int(parameters['HALF_WINDOW_SIZE']) > 0:
				print("Extend %d bp to the middle of %s file" % (int(parameters['HALF_WINDOW_SIZE']), bed_file), file=sys.stderr)
				tmp = BED.ParseBED(bed_file)
				input_bed = tmp.midBED(half_window_size = parameters['HALF_WINDOW_SIZE'],head_num = parameters['HEAD_ROWS'])
			elif int(parameters['HALF_WINDOW_SIZE']) == 0:
				print("Using regions defined in %s file" % bed_file, file=sys.stderr)
				for l in open(bed_file):
					l = l.strip()
					if l.startswith('#'):continue
					if l.startswith('track'):continue
					f = l.split()
					if len(f) < 3:
						continue
					elif (len(f) >= 6) and (f[5] in ('+','-')):
						input_bed.append(  (f[0], int(f[1]), int(f[2]), f[5])   )
					else:
						input_bed.append(  (f[0], int(f[1]), int(f[2]), 'NA')   )
						
			else:
				print("'HALF_WINDOW_SIZE' takes positive integer value.\n", file=sys.stderr)
				sys.exit(0)
			
			if len(input_bed) <= 0:
				print('no input genomic intervals. Exit!', file=sys.stder)
				sys.exit(2)
			
			if int(parameters['HALF_WINDOW_SIZE']) == 0:
				#print input_bed[0] 
				parameters['HALF_WINDOW_SIZE'] = (int(input_bed[0][2])-int(input_bed[0][1]))/2
				#print parameters['HALF_WINDOW_SIZE']
			print("total " + str(len(input_bed)) + " lines loaded!\n", file=sys.stderr)
			
			#loading seed file
			for k,bwf in list(seedFile.items()):
				print('extracting signals from SEED: %s -> %s' % (k,bwf), file=sys.stderr)
				seed_bw_profile[k] = profile_bwfile(input_bed,bwf)
				print(k + ' <- c(' + ','.join([str(i) for i in seed_bw_profile[k]]) + ')', file=OUT_DATA)
			
			#loading other bw files
			count=0
			for k,bwf in list(bigwigFiles.items()):
				count +=1
				print("[%s/%s] extracting signals from file: %s -> %s ..." % (str(count), str(len(list(bigwigFiles.keys()))), k, bwf), file=sys.stderr)
				tmp = profile_bwfile(input_bed,bwf)
				other_bw_profile[k] = tmp
				column_number.add(len(tmp))
				print(k + ' <- c(' + ','.join([str(i) for i in tmp]) + ')', file=OUT_DATA)
			
			# normalize seed
			for k,v in list(seed_bw_profile.items()):
				if (max(v) - min(v)) > 0:
					seed_bw_profile_norm[k] = [(i - min(v))/(max(v) - min(v)) for i in v]
				else:
					seed_bw_profile_norm[k] = [0]* len(v)
			
			# normalize other
			for k,v in list(other_bw_profile.items()):
				if (max(v) - min(v)) > 0:
					other_bw_profile_norm[k] = [(i - min(v))/(max(v) - min(v)) for i in v]
				else:
					other_bw_profile_norm[k] = [0]* len(v)
			
			#sorted by correlation coefficient
			if parameters['DIST_METRIC'].lower() == "pearson":
				sorted_profile = pearson_cor(seed_bw_profile, other_bw_profile)
			elif parameters['DIST_METRIC'].lower() == "kendall":
				sorted_profile = kendall_tau(seed_bw_profile_norm, other_bw_profile_norm)
			elif parameters['DIST_METRIC'].lower() == "spearman":
				sorted_profile = spearman_rho(seed_bw_profile_norm, other_bw_profile_norm)
			elif parameters['DIST_METRIC'].lower() == "euclidean":
				sorted_profile = euclidean_dist(seed_bw_profile_norm, other_bw_profile_norm)
			else:
				print("'DIST_METRIC' can only take 'pearson', 'kendall', 'spearman' or 'euclidean'\n", file=sys.stderr)
				sys.exit(0)
			
			#generate R code and heatmap
			if len(column_number) == 1:
				Rcode_write(sorted_profile,output_prefix + '.r', column_number.pop(),output_prefix,parameters['HM_FORMAT'],int(parameters['HALF_WINDOW_SIZE']))
			else:
				print('column numbers (window width) are different between dataset', file=sys.stderr)
				sys.exit(3)
			
	else:
		print(usage, file=sys.stderr)
		sys.exit(0)			
		
if __name__ == '__main__':
	main()
