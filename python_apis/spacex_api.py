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
		if (self.responseJSON['success'] == 'true'):
			self.success = True
		else:
			self.success = False
		self.timestamp = self.responseJSON['date_unix']
		self.time = datetime.fromtimestamp(self.timestamp)
		self.name = self.responseJSON['name']
		self.missionPatchUrl = self.responseJSON['links']['patch']['small']
		print(self.missionPatchUrl)
		self.missionPicturesUrls = self.responseJSON['links']['flickr']['original']
		print(self.missionPicturesUrls)

class Interface:

	def __init__(self, window):
		
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
			family = "Arial", 
			size = 20,
			weight = "bold"
		)
		self.detailsFont = tkFont.Font(
			family = "Arial",
			size = 12
		)

		self.apiCall = apiCall();

		

		self.titleFrame = tkinter.Frame(
			master = self.mainFrame,
			background = 'black'
		)
		self.title = tkinter.Label(
			master = self.titleFrame,
			text = "Latest SpaceX launch: {}".format(self.apiCall.name),
			font = self.titleFont
		)
		self.subtitle = tkinter.Label(
			master = self.titleFrame,
			text = self.apiCall.time,
			font = self.detailsFont
		)
		self.title.pack()
		self.subtitle.pack()
		self.titleFrame.grid(column = 0, row = 0, padx = 20, pady = 20)

		
		
		self.patchUrlStream = urlopen(self.apiCall.responseJSON['links']['patch']['small'])
		self.patchRawData = self.patchUrlStream.read()
		self.patchUrlStream.close()
		self.patchBytesImage = Image.open(BytesIO(self.patchRawData))

		self.patchImageWidth, self.patchImageHeight = self.patchBytesImage.size
		if(self.patchImageWidth > self.patchImageHeight):
			self.patchResizeHeight = int(((self.patchImageHeight / self.patchImageWidth) * 200) // 1)
			self.patchBytesImage = self.patchBytesImage.resize((200, self.patchResizeHeight))
		else:
			self.patchResizeWidth = int(((self.patchImageWidth / self.patchImageHeight) * 200) // 1)
			self.patchBytesImage = self.patchBytesImage.resize((self.patchResizeWidth, 200))
		self.patchPhoto = ImageTk.PhotoImage(self.patchBytesImage)

		self.patchLabel = tkinter.Label(
			master = self.mainFrame,
			image = self.patchPhoto,
			background = 'black'
		)
		self.patchLabel.grid(column = 1, row = 0)



		self.collageFrame = tkinter.Frame(
			master = self.mainFrame,
			background = 'black'
		)
		self.imageLabel1 = tkinter.Label(
			master = self.collageFrame,
			text = "Image Collage Here", 
			font = self.detailsFont
		)
		self.imageLabel1.pack()
		self.collageFrame.grid(column = 0, row = 1)



		self.mainFrame.grid(column = 0, row = 0)



if __name__ == '__main__':
	window = tkinter.Tk()
	window.configure(background='black')
	window.title('Latest SpaceX Launch')
	app = Interface(window)
	window.mainloop()