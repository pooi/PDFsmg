import os, sys
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

file_dir = input("File: ")

temp_list = os.path.split(file_dir)
file = str(temp_list[len(temp_list)-1])
file_name = file.replace(".pdf", "")

inputpdf = PdfFileReader(open(file_dir, "rb"), strict=False)

split_dir = os.path.join(os.path.curdir, file_name)
if not os.path.exists(split_dir):
    os.mkdir(split_dir)

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("%s_%04d.pdf" % (os.path.join(split_dir, file_name), i+1), "wb") as outputStream:
        output.write(outputStream)
