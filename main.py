from processes import FararuProcess
from processes import Varzesh3Process
import os
import time
def main():
    if not os.path.exists("files/"):
        os.mkdir("files")
    if not os.path.exists("files/fararu/"):
        os.mkdir("files/fararu/")
    if not os.path.exists("files/varzesh3/"):
        os.mkdir("files/varzesh3/")
    if not os.path.exists("links/"):
        os.mkdir("links")






if __name__ == "__main__":
    main()
    # prcs = [FararuProcess.FararuProcess(1),TasnimProcess.TasnimProcess(2),Varzesh3Process.VarzeshProcess(3)]
    prcs = [FararuProcess.FararuProcess(1),Varzesh3Process.VarzeshProcess(3)]
    for prc in prcs:
        prc.start()
        time.sleep(0.5)
