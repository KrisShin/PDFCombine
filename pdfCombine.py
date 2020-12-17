import os
import re
from PyPDF4.pdf import PdfFileReader as pr, PdfFileWriter as pw
from io import BytesIO
from PIL import Image, ImageDraw


def MergePDF(dir_path):
    pdf_files = list()
    merged_file = pw()
    for filename in os.listdir(dir_path):
        ext = filename.split('.')[-1]
        if filename in ['merged.pdf', 'tempImg.pdf']:
            os.remove(filename)
            continue
        if ext.lower() in ['pdf', 'jpg', 'jpeg', 'tiff']:
            pdf_files.append(filename)

    # 按文件名中的数字排序
    pdf_files = sorted(pdf_files, key=lambda i: int(re.findall(r'^(\d+).*?', i)
                                     [0]) if re.findall(r'^(\d+).*?', i) else -1)

    for pdf_file in pdf_files:
        print(pdf_file)
        ext = pdf_file.split('.')[-1]
        if ext.lower() in ['jpg', 'png', 'jpeg', 'tiff']:
            bimg = open(pdf_file, 'rb')
            img = Image.open(BytesIO(bimg))
            stream = BytesIO()
            img.save(stream, ext)
            img.close()
            pg = pr().

            for i in range(0, pdf.getNumPages()):
                pg = pdf.getPage(i)
                obj = pg['/Resources']['/XObject']

                for j in obj:
                    img = obj[j].getData()
                    stream = covertImg(img)

                    # 在PyPDF4 1.27.0中，此方法未实现，需要修改
                    obj[j].setData(stream)

                newpdf.addPage(pg)
            
            def covertImg(bimg):
                img = Image.open(BytesIO(bimg))

                # 看你想实现什么功能了
                im = doSomething(img)
                
                stream = BytesIO()

                # 将图片保存到stream中
                # 注意，保存的格式要和pdf中原图片的格式保持一致
                im.save(stream, 'jpeg')

                img.close()
                return stream.getvalue()
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

    # input()


if __name__ == '__main__':
    # 设置存放多个pdf文件的文件夹
    dir_path = r'.'
    MergePDF(dir_path)
