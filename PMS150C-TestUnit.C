UART_Out BIT PA.7;                  /* PA7 is used as UART TX */
UART_In BIT PA.4;                   /* PA4 is used as UART RX */

void UART_TX (void);
void UART_RX (void);

static BYTE UART_Data_In;

void OK()
{
    A = 'O'; UART_TX();
    A = 'K'; UART_TX();
    // UART < "CR/LF"
    A = 0x0D; UART_TX();
    A = 0x0A; UART_TX();
}

void FPPA0 (void)
{

	.ADJUST_IC	SYSCLK=IHRC/2, IHRC=16000000Hz , VDD=5V

	$ UART_Out High, Out;
	$ PA.3 High, Out;

	while (1)
	{

        UART_RX();
		switch (UART_Data_In)
		{
			case 'T':
			case 't':
				OK();
				break;
			case '0':
				$ TM2C Disable
				OK();
				break;
			case '1':
				$ TM2C IHRC, PA3, Period
				$ TM2S 8BIT, /1, /1
				tm2b = 1;
				OK();
				break;
			case '2':
				$ TM2C IHRC, PA3, Period
				$ TM2S 8BIT, /2, /1
				tm2b = 1;
				OK();
				break;
			case '4':
				$ TM2C IHRC, PA3, Period
				$ TM2S 8BIT, /4, /1
				tm2b = 1;
				OK();
				break;
			case '8':
				$ TM2C IHRC, PA3, Period
				$ TM2S 8BIT, /8, /1
				tm2b = 1;
				OK();
				break;
			case 'H':
			case 'h':
				$ TM2C Disable
				$ PA.3 High, Out;
				OK();
				break;
			case 'L':
			case 'l':
				$ TM2C Disable
				$ PA.3 Low, Out;
				OK();
				break;

		}
	}
}

System_Clock => 8000000; // Synchronize with .ADJUST_IC

FPPA_Duty    => _SYS(INC.FPPA_NUM);
.errnz    FPPA_Duty > 1

Baud_Rate    => 9600;
UART_Delay   => ((System_Clock / FPPA_Duty) + (Baud_Rate/2) ) / Baud_Rate;
Test_V0      => System_Clock / 1000 * 999;
Test_V1      => UART_Delay * Baud_Rate * FPPA_Duty;
Test_V2      => System_Clock / 1000 * 1001;

#if    (Test_V1 < Test_V0) || (Test_V1 > Test_V2)
    .echo    %Test_V0 <= %Test_V1 <= %Test_V2
    .error    Baud_Rate do not match to System Clock
#endif

void UART_TX (void)
{
    BYTE UART_Data_Out = A;
    set0 UART_Out;                   //    1       Start bit
    BYTE cnt = 8;                    //    2 ~ 3
    .Delay 3;                        //    4 ~ 6
    do
    {    
        .Delay UART_Delay - 10;      //            Data Bit x 8
        sr UART_Data_Out;            //    7
        if (CF)
        {
            nop;                     //    10
            UART_Out = 1;            //    1
        }
        else
        {
            UART_Out = 0;            //    1
            .delay 2;                //    2 ~ 3
        }
    } while (--cnt);                 //    4 ~ 6
    .Delay UART_Delay - 5;
    set1 UART_Out;                   //    1       Stop Bit
    .Delay 2 * UART_Delay - 2;
} 


static void UART_RX(void)
{
	BYTE	cnt;

	while (1)
	{
		cnt	=	8;

		if (! UART_In)
		{
err:		//	receive UART error, so ...;
			continue;
		}
		//	Wait Start Bit
		while (UART_In) NULL;
		.Delay	(UART_Delay / 2) -2;
		if (UART_In) goto err;			//	1, 2
		.Delay	UART_Delay - 3;
		CF	=	0;						//	3
		do
		{
			t0sn	UART_In;			//	1
			CF	=	1;					//	2
			src		UART_Data_In;		//	3
			.Delay	UART_Delay - 6;
		} while (--cnt);				//	4 ~ 6

		A	=	UART_Data_In;			//	4
		//	Check Stop Bit
		if (! UART_In) goto err;
		return;
	}
}
