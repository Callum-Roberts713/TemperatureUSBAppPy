import pandas as pd
import numpy as np

dfub = pd.read_csv("EL-USB-RT_Current_Session.csv")
dftt = pd.read_csv("TinyTagData.csv")
print(dftt)
Humidity = dfub["Humidity(%rh)"]
HumidityT = dftt["Humidity"].iloc[391:573].str.replace(" %RH", "")
HumidityTT = HumidityT.astype(float)
HMeanub = np.mean(Humidity)
Hmedianub = np.median(Humidity)
HMeanTT = np.mean(HumidityTT)
HMedianTT = np.median(HumidityTT)
MeanDiff = HMeanub - HMeanTT
MedianDiff = HMeanub - HMedianTT

if HMeanub > HMeanTT:
    print(
        f"For Humidity:\nMean Calibration Requirements = {MeanDiff}\nMedian Calibration Requirements = {MedianDiff}"
    )
else:
    print(
        f"For Humidity:\nMean Calibration Requirements = {MeanDiff}\nMedian Calibration Requirements = {MedianDiff}"
    )

TempUB = dfub["Celsius(°C)"]
TempT = dftt["Temperature"].str.replace(" °C", "")
TempTT = TempT.astype(float)
TMeanUB = np.mean(TempUB)
TMedianUB = np.median(TempUB)
TMeanTT = np.mean(TempTT)
TMedianTT = np.median(TempTT)

MeanDiffT = TMeanUB - TMeanTT
MedianDiffT = TMedianUB - TMedianTT

if TMeanUB > TMeanTT:
    print(
        f"For Temperature:\nMean Calibration Requirements = {MeanDiffT}\nMedian Calibration Requirements = {MedianDiffT}"
    )
else:
    print(
        f"For Temperature:\nMean Calibration Requirements = {MeanDiffT}\nMedian Calibration Requirements = {MedianDiffT}"
    )
