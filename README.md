# md5hint
Hint md5 hash with provided dictionary.

If you have this MD5 hash ```60737510d1c08b29c264695b2c9e9c9e```, but **dont know the original data**. You just write down the guess words into ```.txt``` file line-by-line and save them with the name as same as that hash, ie. ```60737510d1c08b29c264695b2c9e9c9e.txt```. Which includings suggest words like:
```
ten
words
atthe
first
section
arejust
example
ofdictionary
words
Bytheway
someword
and
other
posible
keywords
```
The output might be:

![Alt text](static/screenshot.png?raw=true "example output")


## Prerequisite
A. If you want to run this scrip in host system, these packages are required:
```bash
hashlib glob logging pathlib time itertools colorama threading mutiprocessing math argparse os
```
some of these packages are already installed by default, if not, install them via ```apt-get``` or ```pip``` as needed.

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
or just pull the image from Docker hub:
```bash
docker pull geeksloth/md5hint
```
By the way, the image from ```geeksloth/md5hint```'s Docker Hub is mainly built on M1 processor (linux/arm64/v8). Recommend to build from ```Dockerfile``` as step 2. instead.

3. Run a container:
```bash
docker run -it --rm -v $PWD:/app geeksloth/md5hint bash
```

## Run
After get into the container, run the following command:
```bash
cd /app
```
```bash
python3 main.py
```
The output will be stored in the ```out``` folder if the result is found.
