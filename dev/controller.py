import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

values = [0x01]

try:
    while True:
        print(spi.xfer(values, 25000, 0, 8))
        print(values)
finally:
    spi.close()
