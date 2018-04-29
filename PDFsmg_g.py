import os, sys
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

main_dir = "/Users/tw/Desktop/pdf_test"

file1 = input("File name 1: ")
fileName1 = ""
if not file1.endswith(".pdf"):
    fileName1 = file1 + ".pdf"
else:
    fileName1 = file1
    file1.replace(".pdf", "")

file2 = input("File name 2:")
fileName2 = ""
if not file2.endswith(".pdf"):
    fileName2 = file2 + ".pdf"
else:
    fileName2 = file2
    file2.replace(".pdf", "")

inputpdf1 = PdfFileReader(open(os.path.join(main_dir, fileName1), "rb"), strict=False)
inputpdf2 = PdfFileReader(open(os.path.join(main_dir, fileName2), "rb"), strict=False)

tmp_dir = os.path.join(main_dir, "tmp")
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

for i in range(inputpdf1.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf1.getPage(i))
    with open("%s_%04d.pdf" % (os.path.join(tmp_dir, "tmp"), i*2+1), "wb") as outputStream:
        output.write(outputStream)


pdf2_size = inputpdf2.numPages
for i in range(pdf2_size):
    output = PdfFileWriter()
    output.addPage(inputpdf2.getPage(pdf2_size - i - 1))
    with open("%s_%04d.pdf" % (os.path.join(tmp_dir, "tmp"), (i+1)*2), "wb") as outputStream:
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

merger.write(os.path.join(main_dir, "%s_%s_result.pdf" % (file1, file2)))

shutil.rmtree(tmp_dir, ignore_errors=True)