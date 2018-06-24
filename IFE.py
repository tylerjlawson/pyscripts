import os, ntpath, PIL, re
from PIL import Image

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_date_taken(path):
	Image.open(path)._setexif()[306]
	return Image.open(path)._getexif()[306]

def rename_all (directory, word):
	i = 0
	for file in os.listdir(directory):
		s = path_leaf(file)
		ext = '.' + s.split('.')[-1]
		src = directory + s
		dst = directory + word + '-' + str(i) + ext
		os.rename(src,dst)
		i+=1

def rename_by_parent(directory):
	for i in os.listdir(directory):
		n=0
		for j in os.listdir(str(directory+i)):
			s = path_leaf(j)
			ext = '.' + s.split('.')[-1]
			src = directory + i + '/' + j
			dst = directory + i + '/' + i + '-' + str(n) + ext
			os.rename(src,dst)
			if re.split('- _',s)[0].is_integer():
				try:
					os.system('jhead -ds' + re.split('- _',s)[0] + dst)
				except:
					print('Date note changed: '+ re.split('- _',s)[0] + dst)
			n+=1