import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from urllib.request import urlopen

query = {'api_key':'XWXTPc9xLBzXezMD08CHqWQAFV9fQdpllnNAmZLy', 'hd':'true'}
response = requests.get('https://api.nasa.gov/planetary/apod', params=query)

responseJSON = response.json()
explanation = responseJSON["explanation"]
hdImageLink = responseJSON["hdurl"]
print(hdImageLink)

class Interface:
	def __init__(self, window):
		self.window = window

		self.description = tk.Label(
			master = self.window,
			text = explanation,
			justify = "left",
			wraplength = 900,
			padx = 10,
			pady = 10,
		)
		self.description.pack()

		url_stream = urlopen(hdImageLink)
		raw_data = url_stream.read()
		url_stream.close()

		imageStream = Image.open(BytesIO(raw_data))
		self.NASAphoto = ImageTk.PhotoImage(imageStream)

		self.imageLabel = tk.Label(
			master = self.window,
			image = self.NASAphoto			#save image as attribute to stop garbage collection
		)
		self.imageLabel.pack(width=100, height=100)

if __name__ == '__main__':
	window = tk.Tk()
	window.title('NASA Picture of the Day!')
	app = Interface(window)
	window.mainloop()