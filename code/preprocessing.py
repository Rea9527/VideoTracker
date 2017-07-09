from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import os
import os.path
import re
import shutil


# store frame name to images.txt
def frameNameProcessing():
	imgIndex = 0
	videoIndex = 0

	while True:
		videoFolder = str(videoIndex)

		rootpath = './frames2/' + videoFolder
		try:
			writeFile = open(rootpath + '/images.txt', 'w')
		except IOError:
			print("convert to folder indices: ", videoIndex)
			break
		else:
			while True:
				num = str(int(videoIndex / 2)) + '_' + str(imgIndex)

				try:
					framename = rootpath + '/' + num + '.png'
					img = Image.open(framename)
				except IOError:
					print("convert to img indices: ", imgIndex)
					break
				else:
					# print(framename)
					writeFile.write(num + '.png\n')
					imgIndex += 1

			if videoIndex % 2 == 1:
				imgIndex = 0
			videoIndex += 1


#set rect region for the first frame for all videos, one by one automatically
# in folder /frames/, videos are stored in specified folder. Each store has two videos
# eg: video 0: folder 0, folder 1
#  		video 1: folder 2, folder 3
# 
# videoFolder/videoIndex: the actual folder name
# storeNum: index of the store, equal to (videoIndex / 2), since there are two videos for each store
def regionProcessing():
	videoIndex = 57

	while True:
		videoFolder = str(videoIndex)
		storeNum = str(int(videoIndex / 2))

		rootpath = './frames2/'+videoFolder
		try:
			img = Image.open(rootpath+'/28_74.png')

		except IOError:
			print('not found')
			break

		else:
			print("current video: ", videoIndex)
			imgArr = np.array(img)
			imshow(imgArr)

			x = ginput(4)
			print('click: ', x)
			close()

			result = ""
			for coord in x:
				result += str(int(coord[0])) + " " + str(int(coord[1])) + " "

			regionFile = open(rootpath + '/region.txt', 'w')
			regionFile.write(result)

			videoIndex += 1
			break


# To process one video for a store
# get region.txt and images.txt
def individualProcess():
	# set folder you want to process and initial image index
	folder = 37
	imgIndex = 86
	rootpath = './rotate/'+str(folder)+'/'

	path = rootpath+str(folder / 2)+'_'+str(imgIndex)+'.png'
	img = Image.open(path)

	imgArr = np.array(img)
	imshow(imgArr)

	x = ginput(4)
	print('click: ', x)
	close()

	result = ""
	for coord in x:
		result += str(int(coord[0])) + " " + str(int(coord[1])) + " "

	regionFile = open(rootpath+'region.txt', 'w')
	regionFile.write(result)


	imgIndex = 86

	try:
		writeFile = open(rootpath+'images.txt', 'w')
	except IOError:
		print("convert to folder indices: ", videoIndex)
	else:
		while True:
			num = '18_' + str(imgIndex)

			try:
				framename = rootpath + num + '.png'
				img = Image.open(framename)
			except IOError:
				print("convert to img indices: ", imgIndex)
				break
			else:
				# print(framename)
				writeFile.write(num + '.png\n')
				imgIndex += 1


# down sample all the images to 228 * 118
# source image folder: /allframes/
# des imaga folder: /allsamples_down/
def downsample():

	curDir = os.getcwd() + '/frames2/'
	newDir = os.getcwd() + '/downsample/'
  
  # traverse all the folders and images
	for parent1, dirnames1, filenames1 in os.walk(curDir):
		# /frames
		for dirname in dirnames1:
			# /0 /1 /2...
			for parent2, dirnames2, filenames2 in os.walk(curDir + dirname):
				for filename in filenames2:
					if filename.find('.png') != -1:
						img = Image.open(curDir + dirname + '/' + filename)
						outImg = img.resize((228, 128))
						try:
							outImg.save(newDir + dirname + '/' + filename, 'png')
						except IOError:
							os.mkdir(newDir + dirname)
							outImg.save(newDir + dirname + '/' + filename, 'png')


# for each store, get the total image frames
# and store in a list: counts
def getTotalCountForEachStore():
	curDir = './downsample/'
	counts = [0 for x in range(0, 65)]
	# get number of imgs of each store
	for parent1, dirnames1, filenames1 in os.walk(curDir):
		# /frames
		for dirname in dirnames1:
			# /0 /1 /2...
			for parent2, dirnames2, filenames2 in os.walk(curDir + dirname):
				storeNum = int(int(dirname) / 2)
				# print(dirname, len(filenames2))
				counts[storeNum] += len(filenames2)
	print(counts)
	return counts


# 
def classify():

	MAX_STORE = 65

	counts = getTotalCountForEachStore()

	curDir = './allsamples_down/'
	trainDir = './train_data/'
	testDir = './test_data/'

	curStore = 0
	curImg = 0
	index = 0

	# read text file and open train txt and test txt
	textFile = open('./output.txt', 'r')
	trainFile = open('./train_data.txt', 'w')
	testFile = open('./test_data.txt', 'w')
	textLines = textFile.readlines()
	trainFile.write(textLines[0])
	testFile.write(textLines[0])
	del textLines[0]
	print(len(textLines))

	# get train data
	while True:
		dis = counts[curStore] / 30.0
		# file anchor point
		storePointer = 0
		storePointer += sum(counts[0:curStore])
		# print(storePointer)
		while True:
			# print(curStore)
			try:
				filename = str(curStore) + '_' + str(int(curImg)) + '.png'
				img = Image.open(curDir + filename)
			except IOError:
				break
			else:
				newName = str(curStore) + '_' + str(index) + '.png'
				shutil.copyfile(os.path.join(curDir, filename), os.path.join(trainDir, newName))

				splitLine = textLines[int(storePointer)+int(curImg)].split(',', 1)
				splitLine[0] = newName
				# get the line and rename
				line = splitLine[0] + ',' + splitLine[1]
				trainFile.write(line)

				index += 1
				curImg += dis

		curStore += 1
		print(curStore)
		index = 0
		curImg = 0
		if curStore >= MAX_STORE:
			break


	curStore = 0
	curImg = 0
	index = 0
	# get test data
	while True:
		dis = counts[curStore] / 24.0
		# file anchor point
		storePointer = 0
		storePointer += sum(counts[0:curStore])
		while True:
			try:
				filename = str(curStore) + '_' + str(int(curImg)) + '.png'
				img = Image.open(curDir + filename)
			except IOError:
				break
			else:
				newName = str(curStore) + '_' + str(index) + '.png'
				shutil.copyfile(os.path.join(curDir, filename), os.path.join(testDir, newName))

				# get the line and rename
				splitLine = textLines[int(storePointer)+int(curImg)].split(',', 1)
				splitLine[0] = newName
				line = splitLine[0] + ',' + splitLine[1]
				# write
				testFile.write(line)
				index += 1
				curImg += dis

		curStore += 1
		index = 0
		curImg = 0
		if curStore >= MAX_STORE:
			break
	


if __name__ == "__main__":
	# print("Frame name processing...")
	# frameNameProcessing()

	# print("Region processing...")
	# regionProcessing()

	# print("Down sampling...")
	# downsample()

	print("Classifying...")
	classify()

	# individualProcess()

