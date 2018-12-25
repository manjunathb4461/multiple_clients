from tkinter import *

def  window(mylist):
	root = Tk()
	def func(name, root):
		#print(name)
		with open('qt', 'w') as f:
			f.write(str(name))
		root.destroy()

	for item in mylist:
		button = Button(root, text=item, command=lambda x=item: func(x, root))
		button.pack()

	root.mainloop()
