/*****************************************************************************
* | File      	:   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*----------------
* |	This version:   V3.0
* | Date        :   2019-07-31
* | Info        :   
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of theex Software, and to permit persons to  whom the Software is
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
******************************************************************************/
#include "DEV_Config.h"

#define SPI_PORT spi1
#define I2C_PORT i2c1
/**
 * GPIO
**/
int EPD_RST_PIN;
int EPD_DC_PIN;
int EPD_CS_PIN;
int EPD_BUSY_PIN;
int EPD_CLK_PIN;
int EPD_MOSI_PIN;

int TP_RST_PIN;
int TP_INT_PIN;
int TP_SDA_PIN;
int TP_SCL_PIN;

int KEY0;
int KEY1;
int KEY2;
/**
 * GPIO read and write
**/
void DEV_Digital_Write(UWORD Pin, UBYTE Value)
{
	gpio_put(Pin, Value);
}

UBYTE DEV_Digital_Read(UWORD Pin)
{
	return gpio_get(Pin);
}

/**
 * SPI
**/
void DEV_SPI_WriteByte(uint8_t Value)
{
    spi_write_blocking(SPI_PORT, &Value, 1);
}

void DEV_SPI_Write_nByte(uint8_t *pData, uint32_t Len)
{
    spi_write_blocking(SPI_PORT, pData, Len);
}

UBYTE I2C_Write_Byte(UWORD Reg, char *Data, UBYTE len)
{
    char wbuf[50]={(Reg>>8)&0xff, Reg&0xff};
	for(UBYTE i=0; i<len; i++) {
		wbuf[i+2] = Data[i];
	}
    if(i2c_write_blocking(I2C_PORT , IIC_Address, wbuf, len+2, false) != len+2) {
		printf("WRITE ERROR \r\n");
		// return -1;
	}
	return 0;
}

UBYTE I2C_Read_Byte(UWORD Reg, char *Data, UBYTE len)
{
	char *rbuf = Data;
	I2C_Write_Byte(Reg, 0, 0);
    if(i2c_read_blocking(I2C_PORT , IIC_Address, rbuf, len, false) != len) {
		printf("READ ERROR \r\n");
		// return -1;
	}
	return 0;
}

/**
 * GPIO Mode
**/
void DEV_GPIO_Mode(UWORD Pin, UWORD Mode)
{
    gpio_init(Pin);
	if(Mode == 0 || Mode == GPIO_IN) {
		gpio_set_dir(Pin, GPIO_IN);
	} else {
		gpio_set_dir(Pin, GPIO_OUT);
	}
}

/**
 * delay x ms
**/
void DEV_Delay_ms(UDOUBLE xms)
{
	sleep_ms(xms);
}

void DEV_GPIO_Init(void)
{
	EPD_RST_PIN     = 12;
	EPD_DC_PIN      = 8;
	EPD_BUSY_PIN    = 13;
	EPD_CS_PIN      = 9;
	
	EPD_CLK_PIN		= 10;
	EPD_MOSI_PIN	= 11;
	
	TP_RST_PIN = 16;
	TP_INT_PIN = 17;
	
	TP_SDA_PIN = 6;		//6,1 * 20,0
	TP_SCL_PIN = 7;		//7,1 * 21,0
	
	KEY0 = 2;
	KEY1 = 3;
	KEY2 = 15;
	
	DEV_GPIO_Mode(EPD_RST_PIN, 1);
	DEV_GPIO_Mode(EPD_DC_PIN, 1);
	DEV_GPIO_Mode(EPD_CS_PIN, 1);
	DEV_GPIO_Mode(EPD_BUSY_PIN, 0);
	
	DEV_GPIO_Mode(TP_RST_PIN, 1);
	DEV_GPIO_Mode(TP_INT_PIN, 0);
	
	DEV_GPIO_Mode(KEY0, 0);
	DEV_GPIO_Mode(KEY1, 0);
	DEV_GPIO_Mode(KEY2, 0);
	gpio_pull_up(KEY0);
	gpio_pull_up(KEY1);
	gpio_pull_up(KEY2);
	// DEV_Digital_Write(EPD_CS_PIN, 1);
}

/******************************************************************************
function:	Module Initialize, the library and initialize the pins, SPI protocol
parameter:
Info:
******************************************************************************/
UBYTE DEV_Module_Init(void)
{
    stdio_init_all();

	// GPIO Config
	DEV_GPIO_Init();
	
    spi_init(SPI_PORT, 5 * 1000 * 1000);
    gpio_set_function(EPD_CLK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(EPD_MOSI_PIN, GPIO_FUNC_SPI);
	
	i2c_init(I2C_PORT, 100 * 1000); 
	gpio_set_function(TP_SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(TP_SCL_PIN, GPIO_FUNC_I2C);

    printf("DEV_Module_Init OK \r\n");
	return 0;
}

/******************************************************************************
function:	Module exits, closes SPI and BCM2835 library
parameter:
Info:
******************************************************************************/
void DEV_Module_Exit(void)
{
	DEV_Digital_Write(EPD_RST_PIN, 0);
	DEV_Digital_Write(TP_RST_PIN, 0);
}
