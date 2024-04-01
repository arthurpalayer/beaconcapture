from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep
from PIL import ImageFont

serial = i2c(port=1, address=0x3c)
spidev2 = i2c(port=1, address=0x27)
device = ssd1306(serial)
longboi = (spidev2)

x = 2
y = 15
status = "1000"
while True:
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        font = ImageFont.truetype("font.ttf", 14)
        draw.text((x,y), "hello"+status, fill="white", font=font)
        status = str(int(status) + 1)
        sleep(0.05)
        
        
