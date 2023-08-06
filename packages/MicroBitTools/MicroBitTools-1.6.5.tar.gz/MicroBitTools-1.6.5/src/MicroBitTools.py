import os
import shutil
import uflash
import requests
import serial
import microfs
import time

readymicrobithexurl = "https://cdn.discordapp.com/attachments/249832375272472576/648205212280160256" \
                      "/microbitserialsystem.hex "


class InternalTools:
    def yntoboolean(data="no"):
        data = data.lower()
        if data == "y":
            return True
        elif data == "n":
            return False
        else:
            return "ERROR: \nInput was not either y or n"


def flash(pythonfile):
    drive = InternalTools.get_mb()
    tryn = 0
    while drive == "":
        if tryn == 1:
            print("Please plug in a microbit")
        tryn = tryn + 1
        input()
        drive = InternalTools.get_mb()

    pyfilenoext = pythonfile[:-3]
    os.system("cd " + os.getcwd())
    os.system('py2hex "' + pythonfile + '"')
    print("Moving to microbit.")
    shutil.move(pyfilenoext + ".hex", drive)
    print("Done!")


def flashF(folder):
    import microfs, uflash, os, time
    # SerialSystem.ser.close()

    print("MicroBit is at: " + microfs.find_microbit()[0] + "\nMicroBit directory is at: " + uflash.find_microbit())
    # try:
    mfiles = microfs.ls()
    print("Removing old stuff: " + str(mfiles))
    for file in mfiles:
        microfs.rm(file)

    files = os.listdir(folder)
    print("Flashing new stuff: " + str(files))
    for file in files:
        microfs.put(folder + "\\" + file)

    print("Flashed new stuff: " + str(microfs.ls()) + "\n")

    time.sleep(0.1)
    print("Done!" + "\n" +
         "Don't forget to name your main file \"main.py\"" + "\n" +
         "Reset your MicroBit to apply changes!"
         )
    # except OSError as e:
    #     exit(str(e) + "\n\nReplug microbit")
    # except TypeError as e:
    #     exit(str(e) + "\n\nReplug microbit")
    # SerialSystem.ser.open()


def export(arg1):
    flash(arg1)


# class SerialSystem:
#     ser = serial.Serial()
#     ser.baudrate = 115200
#     ser.port = "COM3"
#     ser.open()
#
#     microbitpath = "F:\\"
#
#     # FIXA
#     def readyMicroBit(self, printb=False):
#         # shutil.copyfile(os.getcwd() + "\\src\\" + "microbitserialsystem.hex", self.microbitpath+"SerialSystem.hex")
#         # shutil.copy
#         if printb:
#             print("Downloading HEX")
#         url = readymicrobithexurl
#         r = requests.get(url)
#         if printb:
#             print("Downloaded HEX")
#             print("Fixing HEX")
#         content = ""
#         contentb = r.content
#         contentb = str(contentb)
#         contentb = contentb[:-1]
#         contentb = contentb[2:]
#         contentsplit = contentb.split("\\n")
#         for i in contentsplit:
#             content = content + i + "\n"
#         if printb:
#             print("Fixed HEX\n" + str(r.content))
#             print("Moving HEX to microbit")
#
#         outF = open(self.microbitpath + "SerialSystem.hex", "w")
#         outF.write(content)
#         if printb:
#             print("Moved HEX to microbit")
#
#     def display(self):
#         self.ser.writeline("")
#
#     def read(self):
#
#         try:
#             mbd = str(self.ser.readline())
#         except serial.serialutil.SerialException:
#             return {"error": "Can not find MicroBit"}
#         except IndexError:
#             return {"error": "Unknown error"}
#
#         try:
#             mbdf = mbd[2:]
#             # mbdf = mbdf.replace(" ", "")
#             mbdf = mbdf.replace("'", "")
#             mbdf = mbdf.replace("\\r\\n", "")
#             mbdf = mbdf.replace("\\xc2", "")
#         except IndexError:
#             return {"error": "Could not read!"}
#
#         if mbdf.startswith("}"):
#             mbdf = mbdf[1:]
#             mbdfsplit = mbdf.split("\\xa7")
#             try:
#                 temp = int(mbdfsplit[0])
#                 try:
#                     brightness = int(mbdfsplit[1])
#                 except ValueError:
#                     brightness = ""
#                 ButtonA = InternalTools.yntoboolean(mbdfsplit[2][2:])
#                 ButtonB = InternalTools.yntoboolean(mbdfsplit[3][2:])
#                 CmpsH = int(mbdfsplit[4])
#
#                 dicmbd = {
#                     "temp": temp,
#                     "brightness": brightness,
#                     "Buttons": {
#                         "A": ButtonA,
#                         "B": ButtonB
#                     },
#                     "CompassHeading": CmpsH
#                 }
#
#                 return dicmbd
#             except IndexError:
#                 return {"error": "Could not read!"}
#         else:
#             return {"error": "Could not read!"}


def test():
    print("SUCCESS")
