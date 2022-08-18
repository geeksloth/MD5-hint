import glob
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', action='store', type=str, required=False, default="in")
parser.add_argument('-o', '--output', action='store', type=str, required=False, default="out")
args = parser.parse_args()

if not os.path.exists(args.input):
	print("input error: {}".format(args.input))
else:
	files = glob.glob(os.path.join(args.input, "*"), recursive=True)
	for f in files:
		o = os.path.join(args.output, os.path.basename(f))
		cmd = """python3 src/md5hint_v0.8.0.py -i {} -o {}""".format(f, o)
		os.system(cmd)
		