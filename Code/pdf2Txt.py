import os
import subprocess

pdf_folder = 'novel'

# Section for normal human-written texts
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(pdf_folder, txt_filename)

        subprocess.run(['pdftotext', pdf_path, txt_path])

        print(f'{filename} to {txt_filename}')

# Section for NeurIPS papers
# k = 0
# papers = {}
#
# for filename in os.listdir(pdf_folder):
#     if filename.endswith('.pdf'):
#         k += 1
#         pdf_path = os.path.join(pdf_folder, filename)
#         papers[k] = os.path.splitext(filename)[0]
#         txt_filename = '2022-' + str(k) + '.txt'
#         txt_path = os.path.join(pdf_folder, txt_filename)
#
#         subprocess.run(['pdftotext', pdf_path, txt_path])
#
#         print(f'{filename} to {txt_filename}')
#
# print(papers)
