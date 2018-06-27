import os, PIL, time
from PIL import Image
''' This is my python module for renaming and redating images
	This was originally created for expediting the organization 
	of digitized family pictures '''

def get_date_taken(path):
	''' helper function to get exif date of an image '''
	try:
		return Image.open(path)._getexif()[306]
	except KeyError:
		return Image.open(path)._getexif()[36867]
	

def rename_all (directory, word):
	''' renames all files in directory to whatever word is given
		i.e. word-0.jpg word-1.jpg ..... word-n.jpg '''
	i = 0
	for file in os.listdir(directory):
		ext = '.' + file.split('.')[-1]
		src = directory + file
		dst = directory + word + '-' + str(i) + ext
		os.rename(src,dst)
		i+=1

def rename_by_date(directory):
	''' Takes a directory and renames all files in directory with 
		date in format yyyy-mm-dd '''
	rename_all(directory, 'unchanged')
	start = time.time()
	repeats_dict = dict()
	Olength = len(os.listdir(directory))
	failed = 0 
	for file in os.listdir(directory):
		ext = '.' + file.split('.')[-1]
		try:
			date = get_date_taken(directory + file)
			date = date.split()[0]
			newName = date.replace(':','-') + ext
			if not directory[-1] == '/':
				directory += '/'
			src = directory + file
			dst = directory + newName
			key = newName.split('.')[0]
			try:
				n = repeats_dict[key]
				fileName = newName.split('.')[0] + '_' + str(n) + ext
				if n == 1:
					save = src
					src = dst
					dst  = directory + fileName
					os.rename(src,dst)
					repeats_dict[key] += 1
					n = repeats_dict[key]
					fileName = newName.split('.')[0] + '-' + str(n) + ext
					dst  = directory + fileName
					src = save
					os.rename(src,dst)
					repeats_dict[key] += 1
				else:
					dst  = directory + fileName
					os.rename(src,dst)
					repeats_dict[key] += 1
			except KeyError:
				os.rename(src,dst)
				repeats_dict[key] = 1
		except:
			failed += 1
	print("Images lost: " + str(Olength - len(os.listdir(directory))))
	print("Images successfully changed: " + str(len(os.listdir(directory)) - failed))
	print("Failed to name: " + str(failed))
	print ("Elapsed time for rename_by_date(): " + str(time.time() - start))

def is_Int(s):
	''' Helper to tell if data type is an int '''
	try: 
	  int(s)
	  return True
	except ValueError:
	  return False

def rename_by_parent(directory):
	''' Takes a folder that contains subfolder groupings, meant to be the year and renames
		all files in each subfolder grouping and renames and redates it to match its respective
		folder '''
	start = time.time()
	for i in [x for x in os.listdir(directory) if x != '.DS_Store']:
		n=1
		for j in [x for x in os.listdir(str(directory+i)) if x != '.DS_Store']:
			ext = '.' + j.split('.')[-1]
			src = directory + i + '/' + j
			dst = directory + i + '/' + i + '-' + str(n) + ext
			os.rename(src,dst)                                 # set name to date
			if is_Int(i.split('-')[0]):                        # change date
				os.system('touch -t ' + i.split('-')[0] + '01010000 ' + dst)  # date is set to folder year
																			  # and january 1st at 00:00
			n+=1

	for i in [x for x in os.listdir(directory) if x != '.DS_Store']:    
		os.system('mv ' + directory + i + '/*g ' + directory) # moves all image files (png jpg jpeg)
		try:
			l = os.listdir(directory+i)                        # only remove if is a folder
			os.system('rm -R ' + directory + i)
		except: 
			pass

	print("Total images changed: " + str(len(os.listdir(directory))))
	print ("Elapsed time for rename_by_date(): " + str(time.time() - start))

