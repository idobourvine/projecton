import TurretMotor
import struct

t = TurretMotor.TurretMotor(5,2000000)



def read():
    f= int(t.ser.read(2))==11#true if finish
    angle=((int(t.ser.read(5))-10000))/10.0#angle like xyz.d
    encoder = int(t.ser.read(6))-150000#the encoder
    return (f,angle,encoder)

#print read()


def NumberTosend(numToSend):
    '''

    :param numToSend: send to arduino
    :return: void
    '''
    temp=numToSend
    b1=temp/(2**16)
    temp=temp%(2**16)
    b2=temp/(2**8)
    temp=temp%(2**8)
    b3=temp
    t.ser.write(struct.pack('>B', int(b1)))
    t.ser.write(struct.pack('>B', int(b2)))
    t.ser.write(struct.pack('>B', int(b3)))
    #print(b1,b2,b3)


def send(angle,distance,isReverse):
    """
    :param angle: the angle to send
    :param distance: the distance in cm include dir

    :return: void
    """
    temp = int(angle)*5*4096+distance
    if(isReverse):
        temp=temp+2048
    NumberTosend(temp)



send(120000)
print(read())