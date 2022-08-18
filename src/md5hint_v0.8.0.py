import hashlib
import glob
from sys import exit
import logging as log
from pathlib import Path
from time import time, sleep
from itertools import permutations
from config import *
from colorama import Fore
import threading
import multiprocessing as mp
from math import ceil
import argparse
import os



def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', placeholder='-', printEnd = "\r"):
	suffix += ' '*16
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + placeholder * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()

def progress(line_counter, total, prefix="", suffix=""):
	printProgressBar(line_counter, total, prefix = prefix, suffix = suffix, decimals = 0, length = 50)

def letterCasePerm(string):
	output=[""]
	for c in string:
		tmp = []
		if c.isalpha():
			for o in output:
				tmp.append(o+c.lower())
				tmp.append(o+c.upper())
		else:
			for o in output:
				tmp.append(o+c)
		output = tmp
	return output

def bruteForceNumber(string):
	output=[""]
	for c in string:
		tmp = []
		if c.isnumeric():
			for o in output:
				for i in range(0, 10):
					tmp.append(o+str(i))
		else:
			for o in output:
				tmp.append(o+c)
		output = tmp
	return output

def specialLetterPerm(string):
	output=[""]
	c_index = 0
	for c in string:
		tmp = []
		if (c in find_x):
			for o in output:
				tmp.append(o+c)
				tmp.append(o+replace_x[find_x.index(c)])
		else:
			for o in output:
				tmp.append(o+c)
		output = tmp
		c_index += 1
	return output	

def addSuffixPerm(string):
	output=[]
	#perms = [''.join(p) for p in set(permutations(specialChars))]
	#print(perms)
	perms = [''.join(p) for p in set(permutations(specialChars, conf_add_suffix))]
	for perm in perms:
		output.append(string+perm)
	'''
	output=[""]
	for c in string:
		tmp = []
		if c.isalpha():
			for o in output:
				tmp.append(o+c.lower())
				tmp.append(o+c.upper())
		else:
			for o in output:
				tmp.append(o+c)
		output = tmp
	'''
	#print(output)
	return output

def divide_chunks(l, n):
	for i in range(0, len(l), n): 
		yield l[i:i + n]

def hint(lines, threadName="threadx"):
	for line in lines:
		goDeeper = True
		line = line.strip()
		line_current = line
		line_prev = line
		find_index = 0
		while goDeeper:
			#progress(G.line_counter, G.line_total, prefix=threadName, suffix=line)
			log.debug("line_current: {}".format(line_current))
			if target == hashlib.md5(line_current.encode()).hexdigest():
				log.debug("found-> {}".format(line_current))
				G.result = line_current
				goDeeper = False
				break
			line_current_cases = []
			line_current_cases.append(line_current)
			if conf_letterCasePerm:
				for line_current_case in line_current_cases:
					cases = letterCasePerm(line_current_case)
					for case in cases:
						log.debug(case)
						if target == hashlib.md5(case.encode()).hexdigest():
							log.debug("found-> {}".format(case))
							G.result = case
							goDeeper = False
							break
				line_current_cases = cases

			if conf_permutation:
				result = []
				for line_current_case in line_current_cases:
					perms = [''.join(p) for p in permutations(line_current_case)]
					for perm in perms:						
						if target == hashlib.md5(perm.encode()).hexdigest():
							log.debug("found-> {}".format(perm))
							G.result = perm
							goDeeper = False
							break
						result.append(perm)
				line_current_cases = result

			if conf_bruteforce_number:
				result = []
				for line_current_case in line_current_cases:
					perms = bruteForceNumber(line_current_case)
					for perm in perms:						
						if target == hashlib.md5(perm.encode()).hexdigest():
							log.debug("found-> {}".format(perm))
							G.result = perm
							goDeeper = False
							break
						result.append(perm)
				line_current_cases = result

			if conf_replaceSpecial:
				result = []
				for line_current_case in line_current_cases:
					perms = specialLetterPerm(line_current_case)
					for perm in perms:						
						if target == hashlib.md5(perm.encode()).hexdigest():
							log.debug("found-> {}".format(perm))
							G.result = perm
							goDeeper = False
							break
						result.append(perm)
				line_current_cases = result
			
			#print(line_current_cases)
			if conf_add_suffix:
				result = []
				for line_current_case in line_current_cases:
					perms = addSuffixPerm(line_current_case)
					for perm in perms:
						if target == hashlib.md5(perm.encode()).hexdigest():
							log.debug("found-> {}".format(perm))
							G.result = perm
							goDeeper = False
							break
						result.append(perm)

			if line_current == line_prev:
				goDeeper = False
			else:
				line_prev = line_current
		if G.result is not None:
			progress(G.line_counter, G.line_total, prefix=threadName, suffix=line)
			break
		G.line_counter += 1
		progress(G.line_counter, G.line_total, prefix=threadName, suffix=line)

log.basicConfig(format='%(message)s', level=log.INFO)
mgr = mp.Manager()
G = mgr.Namespace()

print("worker count: {}".format(totalWorkers))
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', action='store', type=str, required=True)
parser.add_argument('-o', '--output', action='store', type=str, required=False, default=None)
args = parser.parse_args()
with open(args.input, 'r') as fc:
	lines = fc.readlines()
	if len(lines) < totalWorkers:
		conf_multiprocessing = False
if not os.path.exists(args.input):
	print("input error: {}".format(args.input))
else:
	if conf_multiprocessing:
		tic = time()
		target = Path(args.input).stem.lower()
		log.info("target-> {}".format(target))
		with open(args.input, 'r') as fc:
			lines = fc.readlines()
			lines_per_chunk = ceil(len(lines)/totalWorkers)
			chunks = list(divide_chunks(lines, lines_per_chunk))
			workers = []
			G.result = None
			G.line_total = len(lines)
			G.line_counter = 0
			progress(0, G.line_total)
			for i in range(totalWorkers):
				worker = mp.Process(target = hint, args =(chunks[i], "core"+str(i), ))
				workers.append(worker)
			for i in range(totalWorkers):
				workers[i].start()
			for i in range(totalWorkers):
				workers[i].join()
	else:
		tic = time()
		target = Path(args.input).stem.lower()
		log.info("target-> {}".format(target))
		with open(args.input, 'r') as fc:
			lines = fc.readlines()
			G.result = None
			G.line_total = len(lines)
			G.line_counter = 0
			hint(lines)
	if G.result is not None:
		log.info("match: {}".format(Fore.GREEN+G.result+Fore.RESET))
		if args.output is not None:
			outpath = os.path.dirname(os.path.abspath(args.output))
			if not os.path.exists(outpath):
				os.makedirs(outpath)
			with open(args.output, 'w+') as fo:
				fo.write(G.result)
			print("output exported: {}".format(args.output))
	else:
		progress(G.line_total, G.line_total, prefix="corex", suffix=" "*16)
		log.info("match: {}".format(Fore.RED+"not found"+Fore.RESET))
	log.info("elapsed {} seconds".format(time()-tic))
log.info("END")
