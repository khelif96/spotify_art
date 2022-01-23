# using PIL to convert image to black and white
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps
from random import sample
import util

def grayscale(path, output="out/track_grayscale.png"):
    im = Image.open(path)
    im = im.convert("L")
    im.save(output)

def pixelate(path, output="out/track_pixelated.png", size=10):
    im = Image.open(path)
    # Resize smoothly down to 16x16 pixels
    imgSmall = im.resize((32,32),resample=Image.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(im.size,Image.NEAREST)
    result.save(output)

def blur(path, radius=10, output="out/track_blurred.png"):
    im = Image.open(path)
    imgBlur = im.filter(ImageFilter.GaussianBlur(radius=radius))
    imgBlur.save(output)

def invert(path, output="out/track_inverted.png"):
    im = Image.open(path)
    im = im.convert("RGB")
    im = ImageOps.invert(im)
    im.save(output)

def wordFilter(im, phrase, output="out/track_word.png", color = (255,255,255), background=(0,0,0)):
    im = Image.open(im).convert('RGBA')
    textOverlay = Image.new('RGBA', im.size, (*background,255))
    font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    draw = ImageDraw.Draw(textOverlay)
    xPos = 0
    yPos = 0
    while yPos < im.height:
        while xPos < im.width:
            draw.text((xPos, yPos), phrase, font=font, fill=(*color, 0))
            xPos += font.getsize(phrase)[0]
        if xPos > im.width:
            xPos = 0
            yPos += font.getsize(phrase)[1]
    result = Image.composite(textOverlay, im, textOverlay)
    result.save(output)

def mirror(path, output="out/track_mirrored.png"):
    im = Image.open(path)
    im = im.convert("RGBA")
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im.save(output)

def circleCropped(path, output="out/track_circle.png"):
    im = Image.open(path)
    offset = 0
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, im.size[0] - offset, im.size[1] - offset), fill=255)

    result = im.copy()
    result.putalpha(mask)

    result.save(output)

def attachSpotifyCode(im, code, color = None):
    im = Image.open(im)
    codeIm = Image.open(code)
    imHeight = im.height
    codeImHeight = codeIm.height
    result = Image.new(im.mode, (im.width, imHeight + codeImHeight), (255,255,255))
    result.paste(im, (0,0))
    if color != None:
        coloredCode = codeIm.convert("RGBA")
        pixels = coloredCode.load()
        for y in range(codeIm.height):
            for x in range(codeIm.width):
                if pixels[x, y] != (255, 255, 255, 255):
                    pixels[x, y] = (*color, 255)
        codeIm = coloredCode

    result.paste(codeIm, (0,imHeight))

    result.save("track_code.png")



def combineImages(images = [], output="out/track_combined.png", path="", background=(255,255,255)):
    if len(images) == 0:
        return
    if len(images) %2 != 0:
        # throw error
        return
    
    openImages = []
    for image in images:
        im = Image.open(path + image)
        im = im.convert("RGBA")
        openImages.append(im)
    imageSize = openImages[0].size
    for image in openImages:
        if image.size != imageSize:
            # throw error
            return

    size = util.calculateDimensions(imageSize, len(images))
    result = Image.new(openImages[0].mode, size, background)

    for index, image in enumerate(openImages):
        result.paste(image, (int(index % 2) * imageSize[0], int(index/2) * imageSize[1]))

    result.save(output)


def getAverageColor(im):
    im = Image.open(im)
    im = im.convert("RGB")
    colors = im.getcolors(im.height * im.width)
    colorSample = sample(colors, 5000)
    mostCommonColor = colorSample[0]
    for color in colorSample:
        if colorSample.count(color) > colorSample.count(mostCommonColor):
            mostCommonColor = color

    return mostCommonColor[1]

