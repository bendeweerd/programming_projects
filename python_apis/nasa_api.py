import tkinter
import tkinter.font as tkFont

from PIL import Image, ImageTk
from io import BytesIO

import requests
from urllib.request import urlopen

from datetime import date

query = {'api_key':'XWXTPc9xLBzXezMD08CHqWQAFV9fQdpllnNAmZLy', 'hd':'true'}
response = requests.get('https://api.nasa.gov/planetary/apod', params=query)

responseJSON = response.json()
explanation = responseJSON["explanation"]
hdImageLink = responseJSON["hdurl"]

class Interface:
	def __init__(self, window):

		self.window = window
		self.mainFrame = tkinter.Frame(
			master = self.window,
			background='black'
		)

		# create fonts to use throughout the application
		self.titleFont = tkFont.Font(
			family = "Arial",
			size = 24,
			weight = "bold"
		)
		self.detailsFont = tkFont.Font(
			family = "Arial",
			size = 12
		)

		self.mainFrame.columnconfigure(0, weight = 1)

		for i in range(3):
			self.mainFrame.rowconfigure(i, weight = 1)

		# set title text with current date and display
		today = date.today()
		self.dateText = today.strftime("%B %d, %Y")

		self.title = tkinter.Label(
			master = self.mainFrame,
			text = "NASA POD: " + self.dateText,
			font = self.titleFont,
			fg = 'white',
			background='black'
		)
		self.title.grid(column = 0, row = 0, sticky = tkinter.W, padx = (20, 20), pady = (20, 0))

		# pull description from API and display
		self.description = tkinter.Label(
			master = self.mainFrame,
			text = explanation,
			justify = "left",
			wraplength = 600,
			fg = 'white',
			background='black',
			font = self.detailsFont
		)
		self.description.grid(column = 0, row = 1, padx = 20, pady = 20, sticky = tkinter.W)

		# get the actual image
		url_stream = urlopen(hdImageLink)
		raw_data = url_stream.read()
		url_stream.close()

		self.bytesImage = Image.open(BytesIO(raw_data))
		self.imageWidth, self.imageHeight = self.bytesImage.size

		# resize image to fit nicely in window
		if(self.imageWidth > self.imageHeight):
			self.heightMultiplied = int(((self.imageHeight / self.imageWidth) * 600) // 1)
			print("Height adjusted to " + str(self.heightMultiplied))
			self.bytesImage = self.bytesImage.resize((600, self.heightMultiplied))
		else:
			self.widthMultiplied = int(((self.imageWidth / self.imageHeight) * 600) // 1)
			self.bytesImage = self.bytesImage.resize((self.widthMultiplied, 600))

		self.NASAphoto = ImageTk.PhotoImage(self.bytesImage)

		self.imageLabel = tkinter.Label(
			master = self.mainFrame,
			image = self.NASAphoto,			#save image as attribute to stop garbage collection
			padx = 20,
			pady = 20,
			background='black'
		)
		self.imageLabel.grid(column = 0, row = 2)
		self.mainFrame.grid(column = 0, row = 0, pady = (0, 20))

if __name__ == '__main__':
	window = tkinter.Tk()
	window.configure(background='black')
	window.title('NASA Picture of the Day!')
	app = Interface(window)
	window.mainloop()