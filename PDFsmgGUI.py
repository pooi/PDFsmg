import os, sys
import datetime
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def checkGenerate(file1, file2):
    file1_str = file1.get()
    file2_str = file2.get()

    if file1_str == "" or (not file1_str.endswith(".pdf")):
        messagebox.showerror("Error", "File 1 is not selected")
        return

    if file2_str == "" or (not file2_str.endswith(".pdf")):
        messagebox.showerror("Error", "File 2 is not selected")
        return

    generatePDF(file1_str, file2_str)

def generatePDF(file1, file2):
    try:
        if not file1.endswith(".pdf"):
            fileName1 = file1 + ".pdf"
        else:
            fileName1 = file1
            file1.replace(".pdf", "")

        if not file2.endswith(".pdf"):
            fileName2 = file2 + ".pdf"
        else:
            fileName2 = file2
            file2.replace(".pdf", "")

        inputpdf1 = PdfFileReader(open(fileName1, "rb"), strict=False)
        inputpdf2 = PdfFileReader(open(fileName2, "rb"), strict=False)

        tmp_dir = os.path.join(os.path.curdir, "tmp")
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)

        for i in range(inputpdf1.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf1.getPage(i))
            with open("%s_%04d.pdf" % (os.path.join(tmp_dir, "tmp"), i * 2 + 1), "wb") as outputStream:
                output.write(outputStream)

        pdf2_size = inputpdf2.numPages
        for i in range(pdf2_size):
            output = PdfFileWriter()
            output.addPage(inputpdf2.getPage(pdf2_size - i - 1))
            with open("%s_%04d.pdf" % (os.path.join(tmp_dir, "tmp"), (i + 1) * 2), "wb") as outputStream:
                output.write(outputStream)

        pdfs = []

        for file in os.listdir(tmp_dir):
            if os.path.isdir(file) or file.startswith("."):
                continue
            if file.endswith(".pdf"):
                pdfs.append(os.path.join(tmp_dir, file))

        pdfs.sort()

        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append(pdf)

        now = datetime.datetime.now()
        time_str = "%d%02d%02d%02d%02d%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

        merger.write(os.path.join(os.path.curdir, "result_%s.pdf" % time_str))

        shutil.rmtree(tmp_dir, ignore_errors=True)

        messagebox.showinfo("Information", "Successfully generate PDF")
    except:
        messagebox.showerror("Error", "Error!!")


def checkMerge(dir, sort):
    dir_str = dir.get()
    if dir_str == "":
        messagebox.showerror("Error", "Directory is not selected")
        return

    mergePDF(dir_str, sort.get())

def mergePDF(main_dir, sort):
    try:
        temp_list = os.path.split(main_dir)
        fileName = temp_list[len(temp_list) - 1]

        pdfs = []

        for file in os.listdir(main_dir):
            if os.path.isdir(file) or file.startswith("."):
                continue
            if file.endswith(".pdf"):
                pdfs.append(os.path.join(main_dir, file))


        bsort = False
        if sort == 1:
            bsort = True

        pdfs.sort(reverse=bsort)

        merger = PdfFileMerger(strict=False)

        for pdf in pdfs:
            print(pdf)
            merger.append(pdf)

        merger.write(os.path.join(os.path.curdir, "%s (merged).pdf" % fileName))

        messagebox.showinfo("Information", "Successfully merge PDF")
    except:
        messagebox.showerror("Error", "Error!!")

def checkSplit(file_dir, mode):
    file_dir_str = file_dir.get()
    if file_dir_str == "" or (not file_dir_str.endswith(".pdf")):
        messagebox.showerror("Error", "File is not selected")
        return

    splitPDF(file_dir_str, mode)

def splitPDF(file_dir, mode):
    try:
        temp_list = os.path.split(file_dir)
        file = str(temp_list[len(temp_list) - 1])
        file_name = file.replace(".pdf", "")

        inputpdf = PdfFileReader(open(file_dir, "rb"), strict=False)

        split_dir = os.path.join(os.path.curdir, file_name)
        if not os.path.exists(split_dir):
            os.mkdir(split_dir)

        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("%s_%04d.pdf" % (os.path.join(split_dir, file_name), i + 1), "wb") as outputStream:
                output.write(outputStream)

        messagebox.showinfo("Information", "Successfully split PDF")
    except:
        messagebox.showerror("Error", "Error!!")


def load_file(label):
    file = filedialog.askopenfilename(filetypes=(
                                           ("PDF files", "*.pdf"),
                                           ("All files", "*.*")))
    label.set(file)

def load_dir(dir):
    path = filedialog.askdirectory()
    dir.set(path)

def toggleGenerate():
    print("toggleGenerate")
    splitFrame.pack_forget()
    mergeFrame.pack_forget()

    generateFrame.pack(side=TOP, pady=10)

def toggleSplit():
    print("toggleSplit")
    generateFrame.pack_forget()
    mergeFrame.pack_forget()

    splitFrame.pack(side=TOP, pady=10)

def toggleMerge():
    print("toggleMerge")
    generateFrame.pack_forget()
    splitFrame.pack_forget()

    mergeFrame.pack(side=TOP, pady=10)


root = Tk()

Title = root.title("PDFsmg")
root.geometry('600x400+100+100')

frame = Frame(root)
frame.pack()

topframe = Frame(root)
topframe.pack(side=TOP)

generateFrame = Frame(root)
# generateFrame.pack(side=BOTTOM)

splitFrame = Frame(root)
# bottomframe2.pack(side=BOTTOM)

mergeFrame = Frame(root)
# bottomframe3.pack(side=BOTTOM)

generate = Button(topframe, text="Generate", fg="black", command=toggleGenerate)
generate.pack(side=LEFT)
split = Button(topframe, text="Split", fg="black", command=toggleSplit)
split.pack(side=LEFT)
merge = Button(topframe, text="Merge", fg="black", command=toggleMerge)
merge.pack(side=LEFT)

def setGenerateFrame():

    label_file1_str = StringVar()
    label_file1 = Label(generateFrame, textvariable=label_file1_str)
    label_file1_str.set("Select File 1")
    label_file1.grid(row=0, column=0)

    file1_dir = StringVar()
    label_file1_dir = Label(generateFrame, textvariable=file1_dir)

    b1 = Button(generateFrame, text="Browse", command=lambda : load_file(file1_dir))
    b1.grid(row=0, column=1)
    label_file1_dir.grid(row=0, column=2)


    label_file2_str = StringVar()
    label_file2 = Label(generateFrame, textvariable=label_file2_str)
    label_file2_str.set("Select File 2")
    label_file2.grid(row=1, column=0)

    file2_dir = StringVar()
    label_file2_dir = Label(generateFrame, textvariable=file2_dir)

    b2 = Button(generateFrame, text="Browse", command=lambda: load_file(file2_dir))
    b2.grid(row=1, column=1)
    label_file2_dir.grid(row=1, column=2)

    g_btn = Button(generateFrame, text="Generate", bg="green", fg="black", command=lambda: checkGenerate(file1_dir, file2_dir))
    g_btn.grid(row=2, columnspan=3)

def setMergeFrame():

    label_dir_str = StringVar()
    label_dir = Label(mergeFrame, textvariable=label_dir_str)
    label_dir_str.set("Select Directory")
    label_dir.grid(row=0, column=0)

    dir = StringVar()
    dir_label = Label(mergeFrame, textvariable=dir)

    b1 = Button(mergeFrame, text="Browse", command=lambda: load_dir(dir))
    b1.grid(row=0, column=1)
    dir_label.grid(row=0, column=2)

    sort_var = IntVar()
    Checkbutton(mergeFrame, text="내림차순", variable=sort_var).grid(row=1, columnspan=3)


    m_btn = Button(mergeFrame, text="Merge", bg="green", fg="black", command=lambda: checkMerge(dir, sort_var))
    m_btn.grid(row=2, columnspan=3)

def setSplitFrame():
    label_file1_str = StringVar()
    label_file1 = Label(splitFrame, textvariable=label_file1_str)
    label_file1_str.set("Select File 1")
    label_file1.grid(row=0, column=0)

    file1_dir = StringVar()
    label_file1_dir = Label(splitFrame, textvariable=file1_dir)

    b1 = Button(splitFrame, text="Browse", command=lambda: load_file(file1_dir))
    b1.grid(row=0, column=1)
    label_file1_dir.grid(row=0, column=2)


    m_btn = Button(splitFrame, text="Split", bg="green", fg="black", command=lambda: checkSplit(file1_dir, 0))
    m_btn.grid(row=1, columnspan=3)




setGenerateFrame()
setSplitFrame()
setMergeFrame()

toggleGenerate()

root.mainloop()
