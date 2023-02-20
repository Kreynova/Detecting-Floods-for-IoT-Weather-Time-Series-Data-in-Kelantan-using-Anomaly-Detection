!pip install -U pysad
!pip install combo
!pip install paho-mqtt #IoT Broker

import pandas as pd
# Import modules.
from pyod.models.iforest import IForest
from pysad.models.integrations import ReferenceWindowModel
from pysad.utils import Data
from tqdm import tqdm
import numpy as np
#from pysad.transform.probability_calibration import ConformalProbabilityCalibrator   #CHANGE CALIBRATORS HERE
from pysad.transform.probability_calibration import GaussianTailProbabilityCalibrator

#Internet of Things Hive MQTT
import paho.mqtt.client as paho
import time
import random

df= pd.read_csv('Daily Data Kelantan_FloodDetection.csv') #UPLOAD DATASET HERE. Remember to add file first
df

datas = []
# Init probability calibrator.
calibrator = ConformalProbabilityCalibrator(windowed=True, window_size=300) #CHANGE HERE TOO
#calibrator = GaussianTailProbabilityCalibrator(running_statistics=True, window_size=300)  #CHANGE CLASS AND BE MINDFUL OF THE DIFFERENCE IN CODE
# Init isolation forest anomaly detection model.
model = ReferenceWindowModel(model_cls=IForest, window_size=240, sliding_size=30)

def calculate_score(index,data):
    values = [data['Total Rain (mm)'], data['Humidity (%)'], data['Pressure (mb)']] #ADD ATTRIBUTES HERE (MAX 3)
    model.fit_partial(values)  # Fit to the instance.
    score = model.score_partial(values)  # Score the instance.
    calibrated_score = calibrator.fit_transform(np.array([score]))  # Fit & calibrate score.
    df.loc[index, ["score"]] = score
    df.loc[index, ["calibrate_score"]] = calibrated_score

    # Output if the instance is anomalous.
    if calibrated_score > 0.99:  # If probability of being normal is less than 1/5/10%.
      print("Alert: the data point is anomalous.") #will only show up if an anomaly is detected.
      print(score)
      df.loc[index, ["anomaly"]] = 'yes'

    else:
      df.loc[index, ["anomaly"]] = 'no'

for index,data in df.iterrows():
    calculate_score(index,data)

df #if calibrated_score passes the 0.90/0.95/0.99 threshold = anomaly, the value of which is referenced back from the score

df.to_csv('./Conformal_0.99.csv',index=False)