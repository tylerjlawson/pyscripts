import os, shutil

def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

def create():
	os.makedirs('/home/tyler/Documents/test')
	n = 2000
	for i in range(4):
		os.makedirs('/home/tyler/Documents/test/'+str(i+n))
		for j in range(4):
			touch('/home/tyler/Documents/test/'+str(i+n)+'/test'+str(j)+'.jpg')

def delete():
	shutil.rmtree('/home/tyler/Documents/test')