import os, time, email, smtplib, ssl, pyaudio, threading, sys
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

# wave, tksheet,sys,io,
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AppTemplate:
    """
    This App is Designed to read the output file of an EL-USB-RT Temperature and Humidity Sensor and sound an Alarm aswell as send a warning email
    if the Temperature or Humidity is detected to be out of the input range.
    """

    def __init__(self, win):
        self.style = ttkb.Style(theme="yeti")
        self.notebook = ttk.Notebook(win)
        self.frame1 = ttk.Frame(win)
        self.notebook.add(self.frame1, text="Temperature/Humidity Sensor")
        self.notebook.pack()
        self.lbl = Label(text="Temperature and Humidity Sensor reader")
        self.lbl.pack()
        self.SensorReader("Go")

    def EmailSender(self):
        WarnSub = (
            "WARNING! The Temperature/Humidity sensor has Alerted in the Pre-Preg Store"
        )
        NoFileSub = "Sensor Broken"
        if self.BodyRead == "TempHigh":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the room Temperature is too High!!! \n--- Please ensure that the Temperature is back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "TempLow":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the room Temperature is too Low!!! \n--- Please ensure that the Temperature is back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "HumidHigh":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Humidity in the room is too High!!! \n--- Please ensure that the Humidity is back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "HumidLow":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Humidity in the room is too Low!!! \n--- Please ensure that the Humidity is back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "LowTempLowHumid":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Humidity and the Temperature in the room are too Low!!! \n--- Please ensure that the Temperature and Humidity are back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "HighTempHighHumid":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Humidity and the Temperature in the room are too High!!! \n--- Please ensure that the Temperature and Humidity are back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "HighTempLowHumid":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Temperature in the room is too High and the Humidity is too Low!!! \n--- Please ensure that the Temperature and Humidity are back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "LowTempHighHumid":
            body = "WARNING\n!!! The Temperature/Humidity sensor has detected that the Temperature in the room is too Low and the Humidity is too High!!! \n--- Please ensure that the Temperature and Humidity are back within range as soon as possible ---\n--- This is Alerting for the Pre-Preg Store ---"
            subject = WarnSub
        elif self.BodyRead == "TempFileGone":
            body = "WARNING\n!!! The Sensor has stopped recording Data "
            subject = NoFileSub

        sender_email = "merlintemphumidcontrol@gmail.com"
        reciever_email = [
            "mike.potter@merlinpcb.com",
            "vikki.jones@merlinpcb.com",
            "mctpurchasing@merlinpcb.com",
            "becky.jones@merlinpcb.com",
            "jonathan.griffiths@merlinpcb.com",
            "nick.mclean@merlinpcb.com",
            "matthew.beadel@merlinpcb.com",
            "callum.roberts@merlinpcb.com",
        ]  #
        apppassword = "zxizhocsatckymzt"
        message = MIMEMultipart()

        message["From"] = sender_email
        message["To"] = ",".join(reciever_email)
        message["Subject"] = subject
        message["Bcc"] = ",".join(reciever_email)

        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, apppassword)
            server.sendmail(sender_email, reciever_email, text)

    def AlarmPlayer(self):
        filename = os.path.join(
            getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))),
            "Audio.wav",
        )
        CHUNK_SIZE = 1024
        FORMAT = pyaudio.paInt16
        RATE = 70000

        p = pyaudio.PyAudio()
        output = p.open(
            format=FORMAT, channels=1, rate=RATE, output=True
        )  # frames_per_buffer=CHUNK_SIZE
        with open(filename, "rb") as fh:
            while fh.tell() != os.path.getsize(
                filename
            ):  # get the file-size from the os module
                AUDIO_FRAME = fh.read(CHUNK_SIZE)
                output.write(AUDIO_FRAME)

    def SensorReader(self, Check):
        self.Check = Check
        LogFile = f"C:\Documents and Settings\mct-purchasing\Local Settings\Application Data\EL-USB-RT\EL-USB-RT_Current_Session.txt"
        if os.path.exists(LogFile):
            file = open(
                LogFile,
                "r",
            )
            FLength = file.readlines()
            time.sleep(5)
            main.withdraw()
            oldtime = time.time()
            while True:
                if self.Check == "Go":
                    X = len(FLength) - 14
                    line = file.readline()
                    if not line:
                        time.sleep(1)
                    else:
                        time.sleep(1)
                        elements = line.split(",")
                        CurrentTemp = elements[2]
                        HighTempLimitVar = 21
                        LowTempLimitVar = 0
                        CurrentHumid = elements[5]
                        HighHumidLimitVar = 75
                        LowHumidLimitVar = 0
                        if len(elements) == 11:
                            if elements[0] != "Temperature\Humidity Graph":
                                if int(elements[0]) >= X:
                                    if (
                                        float(LowTempLimitVar) >= float(CurrentTemp)
                                        or float(CurrentTemp) >= float(HighTempLimitVar)
                                        or (
                                            float(LowHumidLimitVar)
                                            >= float(CurrentHumid)
                                            or float(CurrentHumid)
                                            >= float(HighHumidLimitVar)
                                        )
                                    ):
                                        if float(CurrentTemp) <= float(
                                            LowTempLimitVar
                                        ) and (
                                            (
                                                float(LowHumidLimitVar)
                                                <= float(CurrentHumid)
                                                or float(CurrentHumid)
                                                <= float(HighHumidLimitVar)
                                            )
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "TempLow"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif float(CurrentTemp) >= float(
                                            HighTempLimitVar
                                        ) and (
                                            float(LowHumidLimitVar)
                                            <= float(CurrentHumid)
                                            or float(CurrentHumid)
                                            <= float(HighHumidLimitVar)
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "TempHigh"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif float(CurrentHumid) <= float(
                                            LowHumidLimitVar
                                        ) and (
                                            (
                                                float(LowTempLimitVar)
                                                <= float(CurrentTemp)
                                                or float(CurrentTemp)
                                                <= float(HighTempLimitVar)
                                            )
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "HumidLow"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif float(CurrentHumid) >= float(
                                            HighHumidLimitVar
                                        ) and (
                                            (
                                                float(LowTempLimitVar)
                                                <= float(CurrentTemp)
                                                or float(CurrentTemp)
                                                <= float(HighTempLimitVar)
                                            )
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "HumidHigh"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif (
                                            float(LowTempLimitVar) <= float(CurrentTemp)
                                        ) and (
                                            float(LowHumidLimitVar)
                                            <= float(CurrentHumid)
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "LowTempLowHumid"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif (
                                            float(HighTempLimitVar)
                                            >= float(CurrentTemp)
                                        ) and (
                                            float(HighHumidLimitVar)
                                            >= float(CurrentHumid)
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "HighTempHighHumid"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif (
                                            float(LowTempLimitVar) <= float(CurrentTemp)
                                        ) and (
                                            float(HighHumidLimitVar)
                                            >= float(CurrentHumid)
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "LowTempHighHumid"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                                        elif (
                                            float(HighTempLimitVar)
                                            >= float(CurrentTemp)
                                        ) and (
                                            float(LowHumidLimitVar)
                                            <= float(CurrentHumid)
                                        ):
                                            if time.time() - oldtime > 1800:
                                                self.BodyRead = "HighTempLowHumid"
                                                self.EmailSender()
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                oldtime = time.time()
                                                continue
                                            else:
                                                threading.Thread(
                                                    target=self.AlarmPlayer()
                                                ).start()
                                                continue
                else:
                    break
        elif not os.path.exists(self.PATH):
            Messagebox.show_error(
                "The Log File for the EL-USB Sensor is not there. Please check that the app is creating it.",
                "!!! ERROR !!!",
            )
            self.BodyRead = "TempFileGone"
            self.EmailSender()


main = Tk()
window = AppTemplate(main)
main.title("Room Conditions Sensor Check")
main.mainloop()
