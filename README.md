# md5hint
Hint md5 hash with provided dictionary

## Prerequisite
A. If you want to run this scrip in host system, these packages are required:
```bash
hashlib glob logging pathlib time itertools colorama threading mutiprocessing math argparse os
```
some of these packages are already installed by default, if not, install them via ```apt-get``` or ```pip``` as needed
B. Run this script with ```Docker``` container is recommend way, please follow the next step.

## Getting started
1. Clone this repo and change directory into it:
```bash
git clone https://github.com/geeksloth/md5hint.git && cd md5hint
```
2. Build a Docker image from the ```Dockerfile```:
```bash
docker build -t md5hint .
```
3. Run a container:
```bash
docker run -it --rm -v $PWD:/app md5hint bash
```

## Run
After get into the container, run the following command:
```bash
cd /app
```
```bash
python3 main.py
```
