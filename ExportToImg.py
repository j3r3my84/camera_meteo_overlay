from PIL import Image, ImageDraw, ImageFilter, ImageFont
from io import BytesIO
import PyWeather
import requests

bg = Image.new('RGBA', (1024, 1024), color = (0,0,0,0))

def addIconToImage():
    icon = Image.open(BytesIO(requests.get('https://openweathermap.org/img/wn/'+ PyWeather.getIconName() +'@2x.png').content))
    icon = createIconBorder(icon,3,(0,0,0,255))
    bg.paste(icon,(0,0),icon)


def createIconBorder(icon, border_size, border_color):
    iconBd = icon.convert('RGBA')
    pixels = iconBd.getdata()
    newPixels = []
    for pixel in pixels:
        if pixel[3] > 10:
            newPixels.append(border_color)
        else:
            newPixels.append(pixel)
    iconBd.putdata(newPixels)
    iconBd = iconBd.resize((icon.height+border_size*2,icon.width+border_size*2)).filter(ImageFilter.SMOOTH_MORE)
    iconBd = iconBd.crop((border_size,border_size,icon.width+border_size,icon.height+border_size))
    iconBd.paste(icon,(0,0),icon)
    iconBd.save('icon.png')
    return iconBd
    
    


def add_subtitle(text,xy,font_size,font_color=(0,0,0),stroke=0,stroke_color=(0, 0, 0),shadow=(0, 0),shadow_color=(25, 25, 25)):
    font="font.ttf"
    stroke_width = stroke
    xy = list(xy)
    W, H = bg.width, bg.height
    font = ImageFont.truetype(str(font), font_size)
    w, h = font.getsize(text, stroke_width=stroke_width)
    if xy[0] == "center":
        xy[0] = (W - w) // 2
    if xy[1] == "center":
        xy[1] = (H - h) // 2
    draw = ImageDraw.Draw(bg)
    if shadow:
        draw.text(
            (xy[0] + shadow[0], xy[1] + shadow[1]), text, font=font, fill=shadow_color
        )
    draw.text(
        (xy[0], xy[1]),
        text,
        font=font,
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )
    return bg

    
def drawLine(vPosition,bg):
    draw = ImageDraw.Draw(bg)
    draw.line((0, vPosition) + (bg.width,vPosition), fill=(0,0,0), width=3)
    draw.line((1, vPosition) + (bg.width-2,vPosition), fill=(255,0,0), width=1)


def getImageContent():
    addIconToImage()
    add_subtitle(PyWeather.getCityName(),(100,2),13)
    add_subtitle(PyWeather.getCurrentCondition().capitalize(),(100,15),30)
    add_subtitle(PyWeather.getCurrentTempForImg().capitalize() + " °C",(100,50),18)
    add_subtitle(PyWeather.getFeelsLikeForImg().capitalize() + " °C",(100,75),18)
    add_subtitle(PyWeather.getWindSpeed().capitalize().replace("\n","") + " dinspre " + PyWeather.getWindDirValue(),(5,100),15)
    add_subtitle(PyWeather.getPressure().capitalize().replace("\n","") + "  |  " + PyWeather.getHumidity().capitalize(),(5,120),15)
    add_subtitle(PyWeather.getVisibility().capitalize(),(5,140),15)
    add_subtitle(PyWeather.getLastUpdate().capitalize(),(5,162),10)
    bg1 = bg.crop(bg.getbbox())
    drawLine(95,bg1)
    drawLine(156,bg1)
    bg2 = Image.new('RGBA', (bg1.size[0]+10,bg1.size[1]+10), color = (255,255,255,200))
    bg2.paste(bg1,(5,5),bg1)
    return bg2


def createImage(position = "left"):
    img = Image.new('RGBA', (800, 200), color = (0,0,0,0))
    content = getImageContent()
    if position == "left":
        img.paste(content,(5,5),content)
    elif  position == "right":
        img.paste(content,(img.width-content.width-5,5),content)
    return img



image = createImage(position="right")
image.save('img.png')