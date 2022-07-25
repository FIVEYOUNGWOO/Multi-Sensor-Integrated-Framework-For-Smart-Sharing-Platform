import serial
import threading
import time
import binascii

############
# 들어가는 화살표       - 라즈베리 TX
# 나가는   화살표       - 라즈베리 RX
############


def AddCheckSum(Command, AddByte = []) -> bytearray:
    cmd = bytearray([ord(i) for i in Command] + AddByte + [0])
    
    #CheckSum Append Last Index
    cmd[4] = (cmd[1] + cmd[2] + cmd[3]) % 256
    return cmd

class CM:
    def __init__(self):
        self.ser = serial.Serial(
            port = '/dev/ttyS0',
            baudrate = 9600,
            timeout = 1
        )
        self.Result = -1
    
    def __GetCheck(self, Mode) -> False or bytes:
        CheckValue = bytearray([ord(i) for i in "$g" + Mode.lower()])
        Result = [0, 0, 0, 0, 0]
        for i in range(5):
            Result[i] = self.ser.read()
        for i in range(3):
            if Result[i][0] != CheckValue[i]:
                print("Fail", Result[i], CheckValue[i])
                return False
        return Result[3][0]

    def __SetCheck(self, Mode) -> bool:
        if Mode == "B":
            Mode = "A"
        CheckValue = bytearray([ord(i) for i in "$OK" + Mode.lower()])
        Result = [0, 0, 0, 0, 0]
        for i in range(5):
            Result[i] = self.ser.read()
        for i in range(4):
            if Result[i][0] != CheckValue[i]:
                return False
        return True
    
    def __GetCommand(self, Mode) -> False or bytes:
        cmd = AddCheckSum("$G" + Mode, [ord("?")])
        for i in range(3):
            self.ser.write(cmd)
            r = self.__GetCheck(Mode)
            if r != False:
                return r
        return False

    def __SetCommand(self, Mode, AddByte) -> bool:
        cmd = AddCheckSum("$S" + Mode, [AddByte])
        self.ser.write(cmd)
        for i in range(3):
            if not self.__SetCheck(Mode):
                time.sleep(0.6)
                self.ser.write(cmd)
            else: return True
        return False
    
    def SetActive(self, AddByte) -> bool:
        return self.__SetCommand("A", AddByte)       
    
    def Enable(self, Usable: bool = True) -> bool:
        return self.SetActive(0x0D) if Usable else\
                self.SetActive(0x0E)

    def Escrow(self, Usable: bool) -> bool:
        """
        Args
            Usable
                True
                    지페 반환
                False
                    지폐 입수
        """
        return self.SetActive(0x06) if Usable else\
                self.SetActive(0x09)

    def SetConfig(self, ConfigByte) -> bool:
        ConfigByte = 0b11010001
        return self.__SetCommand("C", ConfigByte)

    def Bill(self):
        return self.__GetCommand("B")
    
    def GetActive(self):
        return self.__GetCommand("A")

    def Clear(self, Total:bool = True):
        """
        Args
            Total
                True 총 금액 초기화
                False 현재 들어온 금액 초기화
        """
        return self.__SetCommand('T', ord('R')) \
                if Total else self.SetCommand('B', ord('C'))

# Bill 투입된 금액 확인
# Enable 사용 상태 변경, 투입시 자동 사용불가 상태 -> Enable로 사용 가능 상태로 변경
# SetConfig 최초 전원 공급시만 사용	설정값도 고정
# Escrow, Clear 사용안함

# Cash = CM()
# Cash.SetConfig(0)
# Cash.Enable()

# while True:
#     time.sleep(2)
#     A = Cash.GetActive()
#     B = Cash.Bill()
#     print(f"Active {A}\tBill {B}")