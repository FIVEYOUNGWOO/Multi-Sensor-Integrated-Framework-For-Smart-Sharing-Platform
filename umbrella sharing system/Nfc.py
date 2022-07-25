import time
import signal
import sys
 
from pirc522 import RFID
from subprocess import check_output

def ReadNfc():
    """
    Returns:
        Tuple
            nfc Type    1 = Fixed, 3 = Phone
            Uid         8 Hex   string
    """
    try:
        while True:
            TerminalVal = str(check_output('nfc-poll'))
            lines = TerminalVal.split('\\n')
            UidLine = ""
            uid = ""
            for i in lines:
                if "UID" in i:
                    UidLine = i
            for i in range(1, 4):
                if 'NFCID' + str(i) in UidLine:
                    uid = UidLine.split("UID (NFCID" + str(i) + "):")[1].replace(' ', '')
                    return (i, uid)
    except Exception as e:
        print("Error ", e)

if __name__ == "__main__":
    a = ReadNfc()
    print('type =', a[0])
    print('uid =', a[1])
