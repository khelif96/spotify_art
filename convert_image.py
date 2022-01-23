# using PIL to convert image to black and white
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from random import sample
def pixelate(im):
    # Resize smoothly down to 16x16 pixels
    imgSmall = im.resize((32,32),resample=Image.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(im.size,Image.NEAREST)
    return result

def blur(im):
    imgBlur = im.filter(ImageFilter.GaussianBlur(radius=10))
    return imgBlur

# def writeText(im, text, pos):
#     font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
#     draw = ImageDraw.Draw(im)
#     draw.text(pos, text, font=font, fill=(255,255,255))
#     return im

def transformAll():
    im = Image.open("track.png")
    im = im.convert("L")
    im.save("track_bw.png")

    im = Image.open("track.png")
    im = pixelate(im)
    im.save("track_pixelated.png")

    im = Image.open("track.png")
    im = blur(im)
    im.save("track_blurred.png")


def attachSpotifyCode(im, code):
    im = Image.open(im)
    codeIm = Image.open(code)
    imHeight = im.height
    codeImHeight = codeIm.height
    result = Image.new(im.mode, (im.width, imHeight + codeImHeight), (255,255,255))
    result.paste(im, (0,0))
    result.paste(codeIm, (0,imHeight))

    result.save("track_code.png")


def wordFilter(im, phrase, color = (255,255,255)):
    im = Image.open(im).convert('RGBA')
    textOverlay = Image.new('RGBA', im.size, (*color,255))
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    draw = ImageDraw.Draw(textOverlay)
    xPos = 0
    yPos = 0
    while yPos < im.height:
        while xPos < im.width:
            draw.text((xPos, yPos), phrase, font=font, fill=(0,0,0, 0))
            xPos += font.getsize(phrase)[0]
        if xPos > im.width:
            xPos = 0
            yPos += font.getsize(phrase)[1]
    result = Image.composite(textOverlay, im, textOverlay)
    result.save("track_word.png")

def combineImages():
    im = Image.open("track.png")
    imBlurred = Image.open("track_blurred.png")
    imPixelated = Image.open("track_pixelated.png")
    imWord = Image.open("track_word.png")
    result = Image.new(im.mode, (im.width*2, im.height*2), (255,255,255))
    result.paste(im, (0,0))
    result.paste(imBlurred, (im.width,0))
    result.paste(imPixelated, (0, im.height))
    result.paste(imWord, (im.width, im.height))
    result.save("track_combined.png")

def circle(im):
    im = Image.open(im)
    im = im.convert("RGBA")
    circle = Image.new('L', (im.size[0], im.size[1]), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, im.size[0], im.size[1]), fill=255)
    alpha = Image.new('L', im.size, 255)
    alpha.paste(circle, mask=circle)
    result = Image.composite(im, alpha, alpha)
    result.save("track_circle.png")

def getAverageColor(im):
    im = Image.open(im)
    im = im.convert("RGB")
    colors = im.getcolors(im.height * im.width)
    colorSample = sample(colors, 500)
    mostCommonColor = colorSample[0]
    for color in colorSample:
        if colorSample.count(color) > colorSample.count(mostCommonColor):
            mostCommonColor = color

    # Image.new('RGB', (1, 1), mostCommonColor[1]).save("track_color.png")
    print(mostCommonColor)
    return mostCommonColor