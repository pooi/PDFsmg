import os, sys
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

main_dir = input("Dir: ")

temp_list = os.path.split(main_dir)
fileName = temp_list[len(temp_list)-1]

pdfs = []

for file in os.listdir(main_dir):
    if os.path.isdir(file) or file.startswith("."):
        continue
    if file.endswith(".pdf"):
        pdfs.append(os.path.join(main_dir, file))

pdfs.sort()

merger = PdfFileMerger(strict=False)

for pdf in pdfs:
    print(pdf)
    merger.append(pdf)

merger.write(os.path.join(os.path.curdir, "%s (merged).pdf" % fileName))
print(os.path.curdir)