import time

from Nfc import ReadNfc
from Servo import ServoCls
from CashMachine import CM

class Hw:
    def __init__(self):
        self.Motor = ServoCls()
        self.CM = CM()
    
    def ExtractCheck(self) -> bool:
        self.CM.Enable()
        total = 0
        while True:
            time.sleep(0.2)
            ActiveStatus = self.CM.GetActive()
            if total == 2:
                time.sleep(0.1)
                self.CM.Enable(False)
                self.CM.Clear()
                return True
            if ActiveStatus == 11:
                TotalBill = self.CM.Bill()
                total += TotalBill
                print(total)
                self.CM.Enable()

    def Lental(self):
        if self.ExtractCheck():
            self.Motor.Act(True)
            uid = ReadNfc()[1]
            self.Motor.Act(False)
            return uid
    
    def Return(self):
        self.Motor.Act(True)
        uid = ReadNfc()
        self.Motor.Act(False)
        if '08' == uid[1][:2]:
            # Umbrella Uid Check
            print('핸드폰')

# Lental, Return만 사용
if __name__ == "__main__":
    a = Hw()
    a.Lental()
