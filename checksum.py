import hashlib
import time
import tkFileDialog
import ttk
import zlib
from Tkinter import *
from tkFileDialog import askopenfilename


class GUIChecksumCalculator:
    def __init__(self, master):
        frame = Frame(master, width=550, height=500)
        frame.pack_propagate(0)
        frame.pack()
        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.open = Button(frame, text="OPEN FILE", fg="black", command=self.open_file).pack(side=BOTTOM, fill=X)
        self.save = Button(frame, text="SAVE LOG", fg="black", command=self.save_file).pack(side=BOTTOM, fill=X)
        self.infoText = StringVar()
        self.loading = Label(master, textvariable=self.infoText).pack()
        self.text = Text(frame, height=50, width=200)
        self.text.pack()
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

    def open_file(self):
        self.infoText.set("Loading file...")
        filename = askopenfilename()

        with open(filename) as file_to_check:
            start = time.clock()
            data = file_to_check.read()
            formattedfilename = filename[filename.rfind('/'):len(filename)].replace('/', '')
            alist = ["MD5:    " + hashlib.md5(data).hexdigest() + "\n", "CRC:    " + crc(filename) + "\n",
                     "SHA1:   " + hashlib.sha1(data).hexdigest() + "\n",
                     "SHA224: " + hashlib.sha224(data).hexdigest() + "\n",
                     "SHA256: " + hashlib.sha256(data).hexdigest() + "\n",
                     "SHA384: " + hashlib.sha384(data).hexdigest() + "\n",
                     "SHA512: " + hashlib.sha512(data).hexdigest() + "\n"]
            self.text.insert(END, "\n------------------------------------------------------------------\n")
            self.text.insert(END, formattedfilename + " Calculated. Took: " + "{0:.4f}".format(time.clock() - start) + " sec")
            self.text.insert(END, "\n------------------------------------------------------------------")
            for thingy in alist:
                self.text.insert(END, "\n" + thingy)
            self.text.insert(END, "\n------------------------------------------------------------------")
            self.infoText.set("Loading done (" + formattedfilename + ")")


    def save_file(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            self.infoText.set("File not saved")
            return
        f.write(str(self.text.get(1.0, END)))
        self.infoText.set("File saved in: " + f.name)
        f.close()


def crc(filename):  # thanks http://stackoverflow.com/users/224656/bastian
    prev = 0
    for eachLine in open(filename, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X" % (prev & 0xFFFFFFFF)

root = Tk()
root.title("Checksum Calculator")
app = GUIChecksumCalculator(root)
root.mainloop()
