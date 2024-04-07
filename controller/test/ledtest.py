from gpiozero import LED

led0 = LED(13)
led1 = LED(6)
led2 = LED(16)

while True:
    led0.on()
    led1.on()
    led2.on()

