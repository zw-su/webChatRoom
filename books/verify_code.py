from PIL import Image, ImageFont, ImageFilter, ImageDraw
import random
import math
import string

font_path = '/usr/share/fonts/truetype/chineses/SIMKAI.TTF'
# STFANGSO.TTF: 华文仿宋,STXINGKA.TTF: 华文行楷,STCAIYUN.TTF'  # 华文彩云

# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (90, 40)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (random.randrange(20, 100), random.randrange(50, 150), 255)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 3)

# Python3中String模块ascii_letters和digits方法，
# 其中ascii_letters是生成所有字母，从a-z和A-Z,digits是生成所有数字0-9.


def gen_text():
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))
# number是生成验证码的位数

# 用来绘制干扰线


def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


def generate_code(save_path, filename):
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片

    font = ImageFont.truetype(font_path, 25)  # 验证码的字体和字体大小
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gen_text()  # 生成字符串
    print(text)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=fontcolor)  # 填充字符串

    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)

        image = image.transform((width + 20, height + 10), Image.AFFINE,
                                (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        image.save('%s/%s.png' % (save_path, filename))  # 保存验证码图片
        # print("savepath:", save_path)
        return text


if __name__ == "__main__":
    generate_code('/home/tarena/HelloWorld/static/verifCode',
                  'test')  # 会把生成的图片存成/tmp/test.png
