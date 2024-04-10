import socket

#define host
HOST = "172.20.10.2"
#define port
PORT = 6969
BUFFSIZE = 128

valid_characters = set('0123456789abcdefABCDEF')

def twos_complement(hexstr, bits):
    value = int(hexstr, 16)
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value

def is_hexadecimal(s):
    for c in s:
        if c not in valid_characters:
            return False

    return True

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
   
    msg = "recvd" 
    
    while 1:
        data = s.recvfrom(BUFFSIZE)
        if (len(data[0])):
            print("Received packet from " + str(data[1]))

            packet = bytearray(data[0]).decode(encoding='utf-8', errors='strict')
            print("Raw packet: " + str(packet))

            if (not is_hexadecimal(str(packet))):
                continue

            if (packet[0:2] == "01"):
                packet_source = "IMU"
            else:
                packet_source = "BAD"

            if (packet[2:4] == "0a"):
                packet_type = "Accl"
                data_type = "m/s^2"
                conv_factor = 160563.2 # 16384 * 9.8 @ +/-2g
            elif (packet[2:4] == "0b"):
                packet_type = "Gyro"
                data_type = "deg/s"
                conv_factor = 262.144 # @ +/- 125 dps
            else:
                packet_type = "BAD"

            #x_data = int(packet[4:8], 16)
            x_data = twos_complement(packet[4:8], 16) / conv_factor
            y_data = twos_complement(packet[8:12], 16) / conv_factor
            z_data = twos_complement(packet[12:16], 16) / conv_factor

            print(packet_type + ": (" + str(x_data) + ", " + str(y_data) + ", " + str(z_data) + ") + " data_type + "\n")







