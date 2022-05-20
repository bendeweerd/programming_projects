import tkinter
import tkinter.font as tkFont

from PIL import Image, ImageTk
from io import BytesIO

import requests
from urllib.request import urlopen

from datetime import date
from datetime import datetime

class apiCall:

	def __init__(self):

		self.response = requests.get('https://api.spacexdata.com/v4/launches/latest')
		self.responseJSON = self.response.json()

		self.responseDetails = self.responseJSON["details"]
		self.timestamp = self.responseJSON['date_unix']
		self.time = datetime.fromtimestamp(self.timestamp)
		self.missionName = self.responseJSON['name']
		self.missionPatchUrl = self.responseJSON['links']['patch']['small']
		self.missionPicturesUrls = self.responseJSON['links']['flickr']['original']

class Interface:

	def __init__(self, window):
		
		self.apiCall = apiCall()

		#create main window and frame to hold widgets
		self.window = window
		self.mainFrame = tkinter.Frame(
			master = self.window,
			background = 'black'
		)
		for i in range (2):
			self.mainFrame.columnconfigure(i, weight = 1)
			self.mainFrame.rowconfigure(i, weight = 1)

		#create fonts
		self.titleFont = tkFont.Font(
			# family = "Arial",
			family = "Magneto", 
			size = 20,
			weight = "bold"
		)
		self.detailsFont = tkFont.Font(
			# family = "Arial",
			family = "Magneto",
			size = 12
		)

		self.titleFrame = tkinter.Frame(
			master = self.mainFrame,
			background = 'black'
		)
		self.title = tkinter.Label(
			master = self.titleFrame,
			text = "Latest SpaceX launch: {}".format(self.apiCall.missionName),
			font = self.titleFont,
			foreground = 'white',
			background = 'black'
		)
		self.subtitle = tkinter.Label(
			master = self.titleFrame,
			text = self.apiCall.time,
			font = self.detailsFont,
			foreground = 'white',
			background = 'black'
		)
		self.title.pack()
		self.subtitle.pack()
		self.titleFrame.grid(column = 0, row = 0, padx = 20, pady = 20)

		
		self.patchUrlStream = urlopen(self.apiCall.missionPatchUrl)
		self.patchRawData = self.patchUrlStream.read()
		self.patchUrlStream.close()
		self.patchBytesImage = Image.open(BytesIO(self.patchRawData))

		# patch image is square
		self.patchImageWidth, self.patchImageHeight = self.patchBytesImage.size
		self.patchImageCropPoints = self.get_crop_points(self.patchImageWidth, self.patchImageHeight)
		self.patchBytesImage = self.patchBytesImage.crop(
			(self.patchImageCropPoints[0],
			self.patchImageCropPoints[1],
			self.patchImageCropPoints[2],
			self.patchImageCropPoints[3])
		)

		self.patchBytesImage = self.patchBytesImage.resize((200, 200))
		self.patchPhoto = ImageTk.PhotoImage(self.patchBytesImage)

		self.patchLabel = tkinter.Label(
			master = self.mainFrame,
			image = self.patchPhoto,
			background = 'black'
		)
		self.patchLabel.grid(column = 1, row = 0, padx = 15, pady = 15)

		# self.collage1UrlStream = urlopen(self.apiCall.responseJSON['links']['flickr']['original'][0])
		# self.collage1RawData = self.collage1UrlStream.read()
		# self.collage1UrlStream.close()
		# self.collage1BytesImage = Image.open(BytesIO(self.collage1RawData))

		# self.collage1ImageWidth, self.collage1ImageHeight = self.collage1BytesImage.size
		# self.collage1ImageCropPoints = self.get_crop_points(self.collage1ImageWidth, self.collage1ImageHeight)
		# self.collage1BytesImage = self.collage1BytesImage.crop(
		# 	(self.collage1ImageCropPoints[0],
		# 	self.collage1ImageCropPoints[1],
		# 	self.collage1ImageCropPoints[2],
		# 	self.collage1ImageCropPoints[3])
		# )
		# self.collage1BytesImage = self.collage1BytesImage.resize((400, 400))
		# self.collage1Photo = ImageTk.PhotoImage(self.collage1BytesImage)

		# self.collageFrame = tkinter.Frame(
		# 	master = self.mainFrame,
		# 	background = 'black'
		# )
		# self.imageLabel1 = tkinter.Label(
		# 	master = self.collageFrame,
		# 	image = self.collage1Photo,
		# 	background = 'black'
		# )
		# self.imageLabel1.pack()
		# self.collageFrame.grid(column = 0, row = 1, padx = 15, pady = 15)

		self.mainFrame.grid(column = 0, row = 0)

	def get_crop_points(self, width, height):
		cropLeft = 0
		cropTop = 0
		cropRight = width
		cropBottom = height

		if(width > height):
			cropLeft = (width - height) // 2
			cropRight = width - cropLeft
		else:
			cropTop = (height - width) // 2
			cropBottom = height - cropTop

		cropPoints = [cropLeft, cropTop, cropRight, cropBottom]
		return cropPoints

if __name__ == '__main__':
	window = tkinter.Tk()
	window.configure(background='black')
	window.title('Latest SpaceX Launch')
	app = Interface(window)
	window.mainloop()