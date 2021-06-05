#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <math.h>

#include "ICNT86X.h"
#include "EPD_2in9_V2.h"
#include "GUI_Paint.h"

extern ICNT86_Dev ICNT86_Dev_Now, ICNT86_Dev_Old;

void pthread_irq(void)
{
	if(!DEV_Digital_Read(TP_INT_PIN))
		ICNT86_Dev_Now.Touch = 1;
	else
		ICNT86_Dev_Now.Touch = 0;
}

UBYTE get_key(UBYTE *key_value)
{
	if(DEV_Digital_Read(KEY0) == 0) {
		*key_value = 1;
		// printf("KEY0 ...\r\n");
	}
	else if(DEV_Digital_Read(KEY1) == 0) {
		*key_value = 2;
		// printf("KEY1 ...\r\n");
	}
	else if(DEV_Digital_Read(KEY2) == 0) {
		*key_value = 3;
		// printf("KEY2 ...\r\n");
	}
	else {
		*key_value = 0;
		return 1;
	}
	return 0;
}

// I2C reserves some addresses for special purposes. We exclude these from the scan.
// These are any addresses of the form 000 0xxx or 111 1xxx
bool reserved_addr(uint8_t addr) {
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}

void scan_i2c(void)
{
	printf("\nI2C Bus Scan\n");
	printf("   0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");

	for (int addr = 0; addr < (1 << 7); ++addr) {
		if (addr % 16 == 0) {
			printf("%02x ", addr);
		}

		// Perform a 1-byte dummy read from the probe address. If a slave
		// acknowledges this address, the function returns the number of bytes
		// transferred. If the address byte is ignored, the function returns
		// -1.

		// Skip over any reserved addresses.
		int ret;
		uint8_t rxdata;
		if (reserved_addr(addr))
			ret = PICO_ERROR_GENERIC;
		else
			ret = i2c_read_blocking(i2c1, addr, &rxdata, 1, false);

		printf(ret < 0 ? "." : "@");
		printf(addr % 16 == 15 ? "\n" : "  ");
	}
	printf("Done.\n");
	sleep_ms(1000);
}

int main()
{
	UDOUBLE j=0;
	UBYTE ReFlag = 0, SelfFlag = 0;
	UBYTE NumSelect = 1, temp=0;
	UBYTE key_value = 0;
	UBYTE isHide = 0;
	char buf[10] = {'$', '1', '9', '.', '8', '9'};
	
	DEV_Module_Init();
	ICNT_Init();
	
    EPD_2IN9_V2_Init();
	EPD_2IN9_V2_Clear();
	
	gpio_set_irq_enabled_with_callback(TP_INT_PIN, 0b0100, true, pthread_irq);
	
	DEV_Delay_ms(100);
    //Create a new image cache
    UBYTE *BlackImage;
    /* you have to edit the startup_stm32fxxx.s file and set a big enough heap size */
    UWORD Imagesize = ((EPD_2IN9_V2_WIDTH % 8 == 0)? (EPD_2IN9_V2_WIDTH / 8 ): (EPD_2IN9_V2_WIDTH / 8 + 1)) * EPD_2IN9_V2_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return -1;
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, EPD_2IN9_V2_WIDTH, EPD_2IN9_V2_HEIGHT, 90, WHITE);
    Paint_SelectImage(BlackImage);

    Paint_Clear(WHITE);
	// 128*296
	Paint_DrawRectangle(10, 10, 76, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
	Paint_DrawString_EN(10, 13, "Select", &Font16, WHITE, BLACK);
	Paint_DrawRectangle(109, 10, 188, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
	Paint_DrawString_EN(109, 13, "Display", &Font16, WHITE, BLACK);
	Paint_DrawRectangle(220, 10, 286, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
	Paint_DrawString_EN(220, 13, "Adjust", &Font16, WHITE, BLACK);
	Paint_DrawRectangle(10, 100, 110, 120, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
	Paint_DrawString_EN(10, 103, "Show/Hied", &Font16, WHITE, BLACK);

	Paint_DrawString_EN(40, 38, "On Sale!!!", &Font24, WHITE, BLACK);
	Paint_DrawString_EN(40, 70, "Price: ", &Font24, WHITE, BLACK);
	Paint_DrawString_EN(160, 70, buf, &Font24, WHITE, BLACK);
	
	EPD_2IN9_V2_Display_Base(BlackImage);
	
	while(1) {
		if(ReFlag) {
			EPD_2IN9_V2_Display_Partial(BlackImage);
			j++;
			ReFlag = 0;
			printf("*** Draw Refresh ***\r\n");
		}else if(j > 100 || SelfFlag) {
			SelfFlag = 0;
			j = 0;
			EPD_2IN9_V2_Init();
			EPD_2IN9_V2_Display_Base(BlackImage);
			printf("--- Self Refresh ---\r\n");
		}
		
		DEV_Delay_ms(200);
		ICNT_Scan();
		if(get_key(&key_value) && (ICNT86_Dev_Now.X[0] == ICNT86_Dev_Old.X[0] && ICNT86_Dev_Now.Y[0] == ICNT86_Dev_Old.Y[0])) { // No new touch
			continue;
		}

		if(ICNT86_Dev_Now.TouchCount || key_value) {
			if(key_value) {
				ICNT86_Dev_Now.X[0] = EPD_2IN9_V2_HEIGHT + 1;
				ICNT86_Dev_Now.Y[0] = EPD_2IN9_V2_WIDTH + 1;
			}
			ICNT86_Dev_Now.TouchCount = 0;
			
			
			if((ICNT86_Dev_Now.X[0] > 10 && ICNT86_Dev_Now.Y[0] > 10 && ICNT86_Dev_Now.X[0] < 76 && ICNT86_Dev_Now.Y[0] < 30) || key_value == 1) { // Select
				key_value = 0;
				NumSelect++;
				if(NumSelect > 4)
					NumSelect = 1;
				Paint_ClearWindows(160, 105, 262, 125, WHITE);
				if(NumSelect < 3)
					Paint_DrawString_EN(161 + NumSelect*17, 105, "^", &Font20, WHITE, BLACK);
				else
					Paint_DrawString_EN(161 + (NumSelect+1)*17, 105, "^", &Font20, WHITE, BLACK);
				ReFlag = 1;
				printf("Numer Select ...\r\n");
			}
			if((ICNT86_Dev_Now.X[0] > 109 && ICNT86_Dev_Now.Y[0] > 10 && ICNT86_Dev_Now.X[0] < 188 && ICNT86_Dev_Now.Y[0] < 30) || key_value == 2) { // Display
				key_value = 0;
				SelfFlag = 1;
				Paint_ClearWindows(160, 70, 262, 125, WHITE);
				Paint_DrawString_EN(160, 70, buf, &Font24, WHITE, BLACK);
				printf("Display ...\r\n");
			}
			if((ICNT86_Dev_Now.X[0] > 220 && ICNT86_Dev_Now.Y[0] > 10 && ICNT86_Dev_Now.X[0] < 286 && ICNT86_Dev_Now.Y[0] < 30) || key_value == 3) { // Adjust
				key_value = 0;
				temp = NumSelect;
				if(NumSelect>2)
					temp++;
				if(++buf[temp] == ':')
					buf[temp] = '0';
				
				Paint_ClearWindows(160, 70, 262, 99, WHITE);
				Paint_DrawString_EN(160, 70, buf, &Font24, WHITE, BLACK);
				ReFlag = 1;
				printf("Numer Adjust ...\r\n");
			}
			if(ICNT86_Dev_Now.X[0] > 10 && ICNT86_Dev_Now.Y[0] > 100 && ICNT86_Dev_Now.X[0] < 110 && ICNT86_Dev_Now.Y[0] < 120) { // Show/Hied
				if(isHide % 2) {
					Paint_DrawRectangle(10, 10, 76, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
					Paint_DrawString_EN(10, 13, "Select", &Font16, WHITE, BLACK);
					Paint_DrawRectangle(109, 10, 188, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
					Paint_DrawString_EN(109, 13, "Display", &Font16, WHITE, BLACK);
					Paint_DrawRectangle(220, 10, 286, 30, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
					Paint_DrawString_EN(220, 13, "Adjust", &Font16, WHITE, BLACK);
					Paint_DrawRectangle(10, 100, 110, 120, BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
					Paint_DrawString_EN(10, 103, "Show/Hied", &Font16, WHITE, BLACK);
				}
				else {
					Paint_ClearWindows(9, 9, 291, 31, WHITE);
					Paint_ClearWindows(9, 99, 111, 121, WHITE);
				}
				isHide++;
				SelfFlag = 1;
			}
		}
	}
    EPD_2IN9_V2_Init();
	EPD_2IN9_V2_Clear();
	DEV_Delay_ms(1000);
	EPD_2IN9_V2_Sleep();
	return 0;
}
