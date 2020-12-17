import os
import re
from PyPDF4.pdf import PdfFileReader as pr, PdfFileWriter as pw
import img2pdf
from pathlib import Path


def MergePDF(dir_path):
    pdf_files = list()
    merged_file = pw()
    for filename in os.listdir(dir_path):
        ext = filename.split('.')[-1]
        if ext.lower() in ['pdf', 'jpg', 'png', 'jpeg', 'tiff']:
            pdf_files.append(filename)

    print(pdf_files)
    # 按文件名中的数字排序
    pdf_files = sorted(pdf_files, key=lambda i: int(re.findall(r'^(\d+).*?', i)
                                     [0]) if re.findall(r'^(\d+).*?', i) else -1)

    for pdf_file in pdf_files:
        print(pdf_file)
        ext = pdf_file.split('.')[-1]
        if ext.lower() in ['jpg', 'png', 'jpeg', 'tiff']:
            imgPage = img2pdf.convert(pdf_file)
            merged_file.addPage(imgPage)
        else:
            # 读取PDF文件
            try:
                pdf = pr(open(pdf_file, "rb"))
            except:
                print(f'{pdf_file}无法解析')
                continue
            # 获得源PDF文件中页面总数
            if pdf.isEncrypted:
                print(f'{pdf_file} 是加密文件')
                res = input('输入密码(回车键跳过)')
                if res:
                    while res:
                        try:
                            pdf.decrypt(res)
                        except:
                            print('密码错误')
                        res = input('输入密码(回车键跳过)')
                continue
            pageCount = pdf.getNumPages()
            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                merged_file.addPage(pdf.getPage(iPage))
    with open('merged.pdf', "wb") as outputfile:
        # 注意这里的写法和正常的上下文文件写入是相反的
        merged_file.write(outputfile)
    print('Done')
    input()


if __name__ == '__main__':
    # 设置存放多个pdf文件的文件夹
    dir_path = r'.'
    MergePDF(dir_path)
