import os
import re
from PyPDF4.pdf import PdfFileReader as pr, PdfFileWriter as pw
import img2pdf
import pikepdf._cpphelpers


def main(dir_path):
    file_list = get_file_list(dir_path)
    merged_file = merge_pdf(file_list)
    save_pdf(merged_file)
    print('Done')
    input()


def conv_img2pdf(filename, ext):
    with open(f'{filename}.pdf', 'wb') as pdf:
        img = img2pdf.convert(filename+ext)
        pdf.write(img)
        filename += '.pdf'
    return filename


def get_file_list(dir_path):
    file_list = list()
    for filename in os.listdir(dir_path):
        path, ext = os.path.splitext(filename)
        if filename == 'merged.pdf':
            os.remove(filename)
            continue
        if ext in ['.jpg', '.pdf']:
            if ext == '.jpg':
                filename = conv_img2pdf(path, ext)
            file_list.append(filename)

    # 按文件名中的数字排序
    file_list = sorted(file_list, key=lambda i: int(re.findall(r'^(\d+).*?', i)
                                                    [0]) if re.findall(r'^(\d+).*?', i) else -1)
    return file_list


def merge_pdf(file_list):
    merged_file = pw()

    for pdf_file in file_list:
        print(pdf_file)
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
    return merged_file


def save_pdf(merged_file):
    with open('merged.pdf', "wb") as outputfile:
        # 注意这里的写法和正常的上下文文件写入是相反的
        merged_file.write(outputfile)


if __name__ == '__main__':
    # 设置存放多个pdf文件的文件夹
    dir_path = r'.'
    main(dir_path)
