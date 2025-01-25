from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import Image
#from cryptography.fernet import Fernet

def genData(data):

		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]

		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1

		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

def encode(img, text, new_image_name, key):
	image = Image.open(img, 'r')

	if (len(text) == 0) or (len(img) == 0) or (len(new_image_name) == 0):
		mb.showerror("Error", 'Please fill-up all the fields')
	key = int(key)
	def encrypt(text):
		cipher = ''
		for c in text:
			if c.isalpha() == False:
				cipher += c
			elif c.isupper():
				cipher += chr((ord(c) + key - 65) % 26 + 65)
			elif c.islower():
				cipher += chr((ord(c) + key - 97) % 26 + 97)
		return cipher    
	encrypted_text = encrypt(text)
	new_image = image.copy()
	encode_enc(new_image, encrypted_text)

	new_image_name += '.png'

	new_image.save(new_image_name, 'png')
	mb.showinfo("Encode", "Image encoded successfully")


def decode(img, strvar,key):

	image = Image.open(img, 'r')
 
	data = ''
	imgdata = iter(image.getdata())
	key = int(key)
	def decrypt(text):
		cipher = ''
		for c in text:
			if c.isalpha()==False:
				cipher += c
			elif c.isupper():
				cipher += chr((ord(c) - key - 65) % 26 + 65)
			elif c.islower():
				cipher += chr((ord(c) - key - 97) % 26 + 97)
		return cipher  
 
	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
 
		#string of binary data
		binstr = ''
 
		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'
 
		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			data = decrypt(data)
			strvar.set(data)
			return data

def encode_image():
	"""root.destroy()
	enc = Tk()"""
	enc = Toplevel(root)
	enc.title("Encode Image")
	enc.geometry('600x260')
	enc.resizable(0, 0)
	enc.config(bg='#856ff8')
	Label(enc, text='Encode an image', font=("Consolas", 15), bg='#856ff8',fg='white').place(x=220, rely=0)

	Label(enc, text='Choose image file:', font=("Times New Roman", 13),bg='#856ff8').place(x=10, y=50)

	def OpenFile():
		global Filepath
		Filepath=StringVar()
		Filepath = fd.askopenfilename(initialdir = "/Desktop" , title = "SelectFile",filetypes=(("jpeg files","*jpg"),("all files","*.*")))
 
		label2 = Label(enc,text=Filepath, width=21)
		label2.place(x=350,y=50)

	Label(enc, text='Enter secret data: ', font=("Times New Roman", 13), bg='#856ff8').place(x=10, y=90)
	Label(enc, text='Enter a key to encrypt your data: ', font=("Times New Roman", 13),bg='#856ff8').place(x=10, y=130)
	Label(enc, text='Enter the new file name: ', font=("Times New Roman", 13),bg='#856ff8').place(x=10, y=170)

	secretdata = Entry(enc, width=35)
	secretdata.place(x=350, y=90)

	key = Entry(enc, width=35)
	key.place(x=350, y=130)

	newfilename = Entry(enc, width=35)
	newfilename.place(x=350, y=170)


	SelectButton = Button(enc,text="Choose image",font=('Helvetica',7), relief="solid", command=OpenFile).place(x=505,y=50)
	img_path = Entry(enc, width=24, text="FileOpen").place(x=350, y=50)
	Button(enc, text='Encode', font=('Helvetica', 12), bg='black',fg='#00ff33', command=lambda:
	encode(Filepath, secretdata.get(), newfilename.get(), key.get())).place(x=270, y=210)    



def decode_image():
	dec = Toplevel(root)
	dec.title("Decode Image")
	dec.geometry('600x340')
	dec.resizable(0, 0)
	dec.config(bg='#856ff8')

	Label(dec, text='Decode an image', font=("Consolas", 15), bg='#856ff8',fg='white').place(x=220, rely=0)
	Label(dec, text='Choose stego image:', font=("Times New Roman", 12),bg='#856ff8').place(x=10, y=50)
	Label(dec, text='Enter the key: ', font=("Times New Roman", 13),bg='#856ff8').place(x=10, y=90)
	def OpenFile():
		global Filepath
		Filepath=StringVar()
		Filepath = fd.askopenfilename(initialdir = "/Desktop" , title = "SelectFile",filetypes=(("png files","*png"),("all files","*.*")))
 
		label2 = Label(dec,text=Filepath, width=26)
		label2.place(x=320,y=50)

	file = Entry(dec, width=30)
	file.place(x=320, y=50)

	key = Entry(dec, width=30)
	key.place(x=320, y=90)


	text_strvar = StringVar()

	SelectButton = Button(dec,text="Choose image",font=('Helvetica',7), relief="solid", command=OpenFile).place(x=513,y=50)
	Button(dec, text='Decode', font=('Helvetica', 12), bg='black',fg='#00ff33', command=lambda:
	decode(Filepath, text_strvar, key.get())).place(x=270, y=130)

	Label(dec, text='Decoded data: ', font=("Times New Roman", 12), bg='#856ff8').place(x=15, y=170)

	data = Entry(dec, width=94, text=text_strvar, state='disabled')
	data.place(x=15, y=200, height=100)
	

# Initializing the window
root = Tk()
#sb = Scrollbar(root)
#sb.pack(side = RIGHT, fill = Y)
root.title('Image Steganography v1')
root.geometry('400x320')
root.resizable(0, 0)
root.config(bg='grey')

Label(root, text='Image Steganography', font=('Times', 15), bg='Royalblue', wraplength=300).place(x=130, y=10)
Label(root, text='Encrypt your secret message\nHide it in the image ;)\n', font=('Comic Sans MS', 10), bg='grey', wraplength=300).place(x=130, y=40)
Label(root, text='Click here to encode', font=('Times', 10), bg='grey', wraplength=300).place(x=160, y=85)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='Green', command=encode_image).place(x=85, y=110)

Label(root, text='Want to see the secret message\nin the stego image?', bg='grey',font=('Comic Sans MS', 10), wraplength=300).place(x=125, y=170)
Label(root, text='Click here to decode', font=('Times', 10), bg='grey',wraplength=300).place(x=160, y=215)

Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='green', command=decode_image).place(x=85, y=242)

root.update()
root.mainloop()
