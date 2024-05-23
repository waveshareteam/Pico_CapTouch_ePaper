# *****************************************************************************
# * | File        :	  Pico_CapTouch_ePaper_Test_2in9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-02
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI, I2C
import framebuf
import utime

# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 296
  
WF_PARTIAL_2IN9 = [
    0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0A,0x0,0x0,0x0,0x0,0x0,0x0,  
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
    0x22,0x17,0x41,0xB0,0x32,0x36,
]

WF_PARTIAL_2IN9_Wait = [
0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0A,0x0,0x0,0x0,0x0,0x0,0x2,  
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x1,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
0x22,0x17,0x41,0xB0,0x32,0x36,
]

WS_20_30 = [									
0x80,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,
0x10,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x20,0x0,0x0,0x0,
0x80,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,
0x10,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x20,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x14,0x8,0x0,0x0,0x0,0x0,0x2,
0xA,0xA,0x0,0xA,0xA,0x0,0x1,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x14,0x8,0x0,0x1,0x0,0x0,0x1,
0x0,0x0,0x0,0x0,0x0,0x0,0x1,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x0,0x0,0x0,0x0,0x0,0x0,0x0,
0x44,0x44,0x44,0x44,0x44,0x44,0x0,0x0,0x0,
0x22,0x17,0x41,0x0,0x32,0x36
]

Gray4 = [										
0x00,0x60,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x20,0x60,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x28,0x60,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x2A,0x60,0x15,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x02,0x00,0x05,0x14,0x00,0x00,
0x1E,0x1E,0x00,0x00,0x00,0x00,0x01,
0x00,0x02,0x00,0x05,0x14,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x24,0x22,0x22,0x22,0x23,0x32,0x00,0x00,0x00,
0x22,0x17,0x41,0xAE,0x32,0x28		
]	

# e-Paper
RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

# TP
TRST    = 16
INT     = 17

# key
KEY0 = 2
KEY1 = 3
KEY2 = 15

class config():
    def __init__(self, i2c_addr):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)

        self.trst_pin = Pin(TRST, Pin.OUT)
        self.int_pin = Pin(INT, Pin.IN)

        self.key0 = Pin(KEY0, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(KEY1, Pin.IN, Pin.PULL_UP)
        self.key2 = Pin(KEY2, Pin.IN, Pin.PULL_UP)
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.address = i2c_addr
        self.i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100_000)

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def i2c_writebyte(self, reg, value):
        wbuf = [(reg>>8)&0xff, reg&0xff, value]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_write(self, reg):
        wbuf = [(reg>>8)&0xff, reg&0xff]
        self.i2c.writeto(self.address, bytearray(wbuf))

    def i2c_readbyte(self, reg, len):
        self.i2c_write(reg)
        rbuf = bytearray(len)
        self.i2c.readfrom_into(self.address, rbuf)
        return rbuf

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)
        self.digital_write(self.trst_pin, 0)


class EPD_2in9:
    def __init__(self):
        self.config = config(0x48)

        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        
        self.lut = WF_PARTIAL_2IN9
        self.lut_l = WF_PARTIAL_2IN9_Wait

        self.buffer_4Gray = bytearray(self.height * self.width // 4)
        self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)
        self.buffer = bytearray(self.height * self.width // 8)
        self.image1Gray_Portrait = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        

    # Hardware reset
    def reset(self):
        self.config.digital_write(self.config.reset_pin, 1)
        self.config.delay_ms(50) 
        self.config.digital_write(self.config.reset_pin, 0)
        self.config.delay_ms(2)
        self.config.digital_write(self.config.reset_pin, 1)
        self.config.delay_ms(50)   

    def send_command(self, command):
        self.config.digital_write(self.config.dc_pin, 0)
        self.config.digital_write(self.config.cs_pin, 0)
        self.config.spi_writebyte([command])
        self.config.digital_write(self.config.cs_pin, 1)

    def send_data(self, data):
        self.config.digital_write(self.config.dc_pin, 1)
        self.config.digital_write(self.config.cs_pin, 0)
        self.config.spi_writebyte([data])
        self.config.digital_write(self.config.cs_pin, 1)
        
    def ReadBusy(self):
        # print("e-Paper busy")
        while(self.config.digital_read(self.config.busy_pin) == 1):      #  0: idle, 1: busy
            self.config.delay_ms(10) 
        # print("e-Paper busy release")  

    def TurnOnDisplay(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xF7)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.ReadBusy()

    def TurnOnDisplay_Partial(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.ReadBusy()

    def TurnOnDisplay_4Gray(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xC7)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.ReadBusy()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def SendLut(self, isQuick):
        self.send_command(0x32)
        if(isQuick):
            lut = self.lut    
        else:
            lut = self.lut_l

        for i in range(0, 153):
            self.send_data(lut[i])
        self.ReadBusy()

    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start>>3) & 0xFF)
        self.send_data((x_end>>3) & 0xFF)
        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x>>3) & 0xFF)
        
        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.ReadBusy()

    def SetLut(self, lut):
        self.send_command(0x32)
        for i in range(0, 153):
            self.send_data(lut[i])
        self.ReadBusy()
        self.send_command(0x3f)
        self.send_data(lut[153])
        self.send_command(0x03);	# gate voltage
        self.send_data(lut[154])
        self.send_command(0x04);	# source voltage
        self.send_data(lut[155])	# VSH
        self.send_data(lut[156])	# VSH2
        self.send_data(lut[157])	# VSL
        self.send_command(0x2c);		# VCOM
        self.send_data(lut[158])

    def init(self):
        # EPD hardware init start     
        self.reset()

        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)
    
        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width-1, self.height-1)

        self.send_command(0x21) #  Display update control
        self.send_data(0x00)
        self.send_data(0x80)	
    
        self.SetCursor(0, 0)
        self.ReadBusy()
        # EPD hardware init end
        return 0
    
    def init_4Gray(self):
        self.reset()

        self.ReadBusy()
        self.send_command(0x12)  #SWRESET
        self.ReadBusy() 

        self.send_command(0x01) #Driver output control      
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)
    
        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)
        
        self.SetWindow(8, 0, self.width, self.height-1)

        self.send_command(0x3C)
        self.send_data(0x04)
    
        self.SetCursor(8, 0)
        self.ReadBusy()

        self.SetLut(Gray4)
        # EPD hardware init end
        return 0

    def display(self, image):
        if (image == None):
            return            
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            # for i in range(0, int(self.width / 8)):
            self.send_data(image[i])   
        self.TurnOnDisplay()

    def display_Base(self, image):
        if (image == None):
            return   
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.send_command(0x26) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay()
        
    def display_Partial(self, image):
        if (image == None):
            return
            
        self.config.digital_write(self.config.reset_pin, 0)
        self.config.delay_ms(0.2)
        self.config.digital_write(self.config.reset_pin, 1) 
        
        self.SendLut(1)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)  
        self.send_data(0x00)  
        self.send_data(0x00) 
        self.send_data(0x00)  	
        self.send_data(0x40)  
        self.send_data(0x00)  
        self.send_data(0x00)   
        self.send_data(0x00)  
        self.send_data(0x00)

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22) 
        self.send_data(0xC0)   
        self.send_command(0x20) 
        self.ReadBusy()

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)
        
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(image[i])
        self.TurnOnDisplay_Partial()


    def display_4Gray(self, image):
        self.send_command(0x24)
        for i in range(0, 4736):
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1
                    temp1 >>= 2
            self.send_data(temp3)
            
        self.send_command(0x26)	       
        for i in range(0, 4736):
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2  
                    if(j!=1 or k!=1):                    
                        temp3 <<= 1
                    temp1 >>= 2
            self.send_data(temp3)

        self.TurnOnDisplay_4Gray()

    def Clear(self, color):
        self.send_command(0x24) # WRITE_RAM
        for i in range(0, self.height * int(self.width/8)):
            self.send_data(color)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE
        self.send_data(0x01)
        
        self.config.delay_ms(2000)
        self.module_exit()


class ICNT_Development():
    def __init__(self):
        self.Touch = 0
        self.TouchGestureid = 0
        self.TouchCount = 0
        
        self.TouchEvenid = [0, 1, 2, 3, 4]
        self.X = [0, 1, 2, 3, 4]
        self.Y = [0, 1, 2, 3, 4]
        self.P = [0, 1, 2, 3, 4]
    

class ICNT86():
    def __init__(self):
        self.config = config(0x48)
    
    def ICNT_Reset(self):
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 0)
        self.config.delay_ms(100)
        self.config.digital_write(self.config.trst_pin, 1)
        self.config.delay_ms(100)

    def ICNT_Write(self, Reg, Data):
        self.config.i2c_writebyte(Reg, Data)

    def ICNT_Read(self, Reg, len):
        return self.config.i2c_readbyte(Reg, len)
        
    def ICNT_ReadVersion(self):
        buf = self.ICNT_Read(0x000a, 4)
        print(buf)

    def ICNT_Init(self):
        self.ICNT_Reset()
        self.ICNT_ReadVersion()

    def ICNT_Scan(self, ICNT_Dev, ICNT_Old):
        buf = []
        mask = 0x00
        
        if(ICNT_Dev.Touch == 1):
            ICNT_Dev.Touch = 0
            buf = self.ICNT_Read(0x1001, 1)
            
            if(buf[0] == 0x00):
                self.ICNT_Write(0x1001, mask)
                self.config.delay_ms(1)
                # print("buffers status is 0")
                return
            else:
                ICNT_Dev.TouchCount = buf[0]
                
                if(ICNT_Dev.TouchCount > 5 or ICNT_Dev.TouchCount < 1):
                    self.ICNT_Write(0x1001, mask)
                    ICNT_Dev.TouchCount = 0
                    # print("TouchCount number is wrong")
                    return
                    
                buf = self.ICNT_Read(0x1002, ICNT_Dev.TouchCount*7)
                self.ICNT_Write(0x1001, mask)
                
                ICNT_Old.X[0] = ICNT_Dev.X[0]
                ICNT_Old.Y[0] = ICNT_Dev.Y[0]
                ICNT_Old.P[0] = ICNT_Dev.P[0]
                
                for i in range(0, ICNT_Dev.TouchCount, 1):
                    ICNT_Dev.TouchEvenid[i] = buf[6 + 7*i] 
                    # ICNT_Dev.X[i] = ((buf[2 + 7*i] << 8) + buf[1 + 7*i])
                    # ICNT_Dev.Y[i] = ((buf[4 + 7*i] << 8) + buf[3 + 7*i])
                    ICNT_Dev.X[i] = 127 - ((buf[4 + 7*i] << 8) + buf[3 + 7*i])
                    ICNT_Dev.Y[i] = ((buf[2 + 7*i] << 8) + buf[1 + 7*i])
                    ICNT_Dev.P[i] = buf[5 + 7*i]

                print(ICNT_Dev.X[0], ICNT_Dev.Y[0], ICNT_Dev.P[0])
                return
        return


flag_t = NumSelect = 1
ReFlag = SelfFlag  = temp = isHide = key_value = 0
buf = ['$', '1', '9', '.', '8', '9']

epd = EPD_2in9()
# tp = ICNT86()
# icnt_dev = ICNT_Development()
# icnt_old = ICNT_Development()

  
'''
    Because the touch display requires a relatively fast refresh speed, the default 
    needs to use partial refresh, and four gray levels cannot be used in this mode. 
    Here, only four gray level picture refresh demonstration is used
'''
# epd.init_4Gray()
# epd.image4Gray.fill_rect(0, 0, 127, 74, epd.black)  
# epd.image4Gray.text('GRAY1',10, 33, epd.white)
# epd.image4Gray.fill_rect(0, 74, 127, 74, epd.darkgray)
# epd.image4Gray.text('GRAY2',10, 107, epd.grayish)
# epd.image4Gray.fill_rect(0, 148, 127, 74, epd.grayish)
# epd.image4Gray.text('GRAY3',10, 181, epd.darkgray)
# epd.image4Gray.fill_rect(0, 222, 127, 74, epd.white)
# epd.image4Gray.text('GRAY4',10, 255, epd.black)
# epd.display_4Gray(epd.buffer_4Gray)
# epd.delay_ms(500)


def pthread_irq():
    if(tp.config.digital_read(tp.config.int_pin) == 0):
        icnt_dev.Touch = 1
    else:
        icnt_dev.Touch = 0

def get_key():
    if(tp.config.digital_read(tp.config.key0) == 0):
        return 1
    elif(tp.config.digital_read(tp.config.key1) == 0):
        return 2
    elif(tp.config.digital_read(tp.config.key2) == 0):
        return 3
    else:
        return 0

epd.init()
tp.ICNT_Init()
# epd.image1Gray_Portrait.Clear(0xff)

# tp.config.int_pin.irq(pthread_irq(), Pin.IRQ_FALLING)

epd.image1Gray_Portrait.fill(0xff)
epd.image1Gray_Portrait.rect(5, 10, 51, 14, 0x00)
epd.image1Gray_Portrait.text("Select", 7, 13, 0x00)
epd.image1Gray_Portrait.rect(72, 10, 51, 14, 0x00)
epd.image1Gray_Portrait.text("Adjust", 74, 13, 0x00)

epd.image1Gray_Portrait.rect(30, 240, 66, 18, 0x00)
epd.image1Gray_Portrait.text("Display", 35, 245, 0x00)

epd.image1Gray_Portrait.rect(21, 270, 82, 18, 0x00)
epd.image1Gray_Portrait.text("Show/Hied", 26, 275, 0x00)

epd.image1Gray_Portrait.text("On Sale!!!", 10, 50, 0x00)
epd.image1Gray_Portrait.text("Discount %30", 10, 75, 0x00)
epd.image1Gray_Portrait.text("Price: ", 10, 100, 0x00)
epd.image1Gray_Portrait.text(''.join(buf), 66, 100, 0x00)

for i in range(0, 5):
    epd.image1Gray_Portrait.fill_rect(10 + 50, 135 + i*10, 50, 5, 0x00)
for i in range(0, 5):
    epd.image1Gray_Portrait.fill_rect(10 + i*10, 135 + 50, 5, 50, 0x00)

epd.display_Base(epd.buffer)

while(1):
    if(ReFlag):
        epd.display_Partial(epd.buffer)
        ReFlag = 0
    elif(SelfFlag):
        epd.init()
        epd.display_Base(epd.buffer)
        SelfFlag = 0
    
    pthread_irq()
    tp.ICNT_Scan(icnt_dev, icnt_old)
    key_value = get_key()
    if(key_value == 0 and icnt_dev.X[0] == icnt_old.X[0] and icnt_dev.Y[0] == icnt_old.Y[0]):
        continue

    if(icnt_dev.TouchCount or key_value):
        if(key_value):
            icnt_dev.X[0] = epd.width + 1
            icnt_dev.Y[0] = epd.height + 1
        icnt_dev.TouchCount = 0

        if((icnt_dev.X[0] > 5 and icnt_dev.Y[0] > 10 and icnt_dev.X[0] < 61 and icnt_dev.Y[0] < 24) or key_value == 1): # Select
            key_value = 0
            NumSelect += 1
            if(NumSelect > 4):
                NumSelect = 1
            epd.image1Gray_Portrait.fill_rect(70, 115, 50, 15, 0xff)
            if(NumSelect < 3):
                epd.image1Gray_Portrait.text("^", 66 + NumSelect*8, 115, 0x00)
            else:
                epd.image1Gray_Portrait.text("^", 66 + (NumSelect+1)*8, 115, 0x00)
            ReFlag = 1
            print("Numer Select ...\r\n")
        
        if((icnt_dev.X[0] > 30 and icnt_dev.Y[0] > 240 and icnt_dev.X[0] < 66 and icnt_dev.Y[0] < 258) or key_value == 2): # Display
            key_value = 0
            SelfFlag = 1
            epd.image1Gray_Portrait.fill_rect(66, 100, 50, 30, 0xff)
            epd.image1Gray_Portrait.text(''.join(buf), 66, 100, 0x00)
            print("Display ...\r\n")
        
        if((icnt_dev.X[0] > 72 and icnt_dev.Y[0] > 10 and icnt_dev.X[0] < 123 and icnt_dev.Y[0] < 24) or key_value == 3): # Adjust
            key_value = 0
            temp = NumSelect
            if(NumSelect>2):
                temp += 1
            if((buf[temp]) == '9'):
                buf[temp] = '0'
            else:
                buf[temp] = chr(ord(buf[temp]) + 1)
            
            epd.image1Gray_Portrait.fill_rect(66, 100, 50, 10, 0xff)
            epd.image1Gray_Portrait.text(''.join(buf), 66, 100, 0x00)
            ReFlag = 1
            print("Numer Adjust ...\r\n")
        
        if(icnt_dev.X[0] > 21 and icnt_dev.Y[0] > 270 and icnt_dev.X[0] < 103 and icnt_dev.Y[0] < 288): # Show/Hied
            if(isHide % 2):
                epd.image1Gray_Portrait.rect(5, 10, 51, 14, 0x00)
                epd.image1Gray_Portrait.text("Select", 7, 13, 0x00)
                epd.image1Gray_Portrait.rect(72, 10, 51, 14, 0x00)
                epd.image1Gray_Portrait.text("Adjust", 74, 13, 0x00)

                epd.image1Gray_Portrait.rect(30, 240, 66, 18, 0x00)
                epd.image1Gray_Portrait.text("Display", 35, 245, 0x00)

                epd.image1Gray_Portrait.rect(21, 270, 82, 18, 0x00)
                epd.image1Gray_Portrait.text("Show/Hied", 26, 275, 0x00)

                epd.image1Gray_Portrait.text("On Sale!!!", 10, 50, 0x00)
                epd.image1Gray_Portrait.text("Discount %30", 10, 75, 0x00)
                epd.image1Gray_Portrait.text("Price: ", 10, 100, 0x00)
                epd.image1Gray_Portrait.text(''.join(buf), 66, 100, 0x00)
            else:
                epd.image1Gray_Portrait.fill_rect(0, 0, 127, 30, 0xff)
                epd.image1Gray_Portrait.fill_rect(0, 240, 127, 55, 0xff)
            isHide += 1
            SelfFlag = 1
        
    
    

