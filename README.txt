Detecting Floods for IoT Weather Time Series Data in Kelantan using Anomaly Detection
- This code is written in Python and performs online (streaming) anomaly detection using the iForest and Conformal Probability Calibration algorithms.

The code first installs several packages using pip, including "pysad", "combo", and "paho-mqtt", which are used for anomaly detection, data preprocessing, and communication with the Internet of Things (IoT) respectively.
Next, the code imports several modules, including the IForest model from the "pyod" package and the Conformal Probability Calibrator from the "pysad" package. It initializes the calibrator with a window size of 300 and initializes the iForest model with a window size of 240 and a sliding size of 30.
The function "calculate_score" takes in a row of data and calculates the score of the input data using the iForest model. The score is then calibrated using the Conformal Probability Calibrator and checked to see if it is above 0.99. If the calibrated score is above 0.99, the data is considered anomalous, and a message indicating this is printed. If the score is not above 0.99, the data is considered normal.
Finally, the code iterates through each row in the dataframe "df" and calls the function "calculate_score" on each row, updating the scores and anomaly status in the dataframe.

Getting Started

1. Prerequisities
- Python
- Google Colab (platform used to perform this task)
- Weather data in .csv

2. Installing
Using Python,

!pip install -U pysad
!pip install combo
!pip install paho-mqtt #IoT

import pandas as pd
# Import modules.
from pyod.models.iforest import IForest
from pysad.models.integrations import ReferenceWindowModel
from pysad.utils import Data
from tqdm import tqdm
import numpy as np

3. Change these according to which desired calibrator
A) In lines 12 and 13,

#from pysad.transform.probability_calibration import ConformalProbabilityCalibrator   #CHANGE CALIBRATORS HERE
from pysad.transform.probability_calibration import GaussianTailProbabilityCalibrator

B) In lines 25 and 26,

calibrator = ConformalProbabilityCalibrator(windowed=True, window_size=300) #CHANGE HERE TOO
#calibrator = GaussianTailProbabilityCalibrator(running_statistics=True, window_size=300)  #CHANGE CLASS AND BE MINDFUL OF THE DIFFERENCE IN CODE

4. Change these according to which THREE (3) desired attributes for calibrated_score
In line 31,

values = [data['Total Rain (mm)'], data['Humidity (%)'], data['Pressure (mb)']] #ADD ATTRIBUTES HERE (MAX 3)

5. Change these according to which desired confidence interval
In line 39,

if calibrated_score > 0.99:

6. And repeat these until obtained desired amount of output for all calibrators and confidence intervals
A) In line 47,

for index,data in df.iterrows():
    calculate_score(index,data)

B) In line 52,

df.to_csv('./Conformal_0.99.csv',index=False)

7. Built With
- Google Colab online

8. Version
- 2.6 (2nd overhaul, 6th attempt at changes)
- 

9. Authors
- Iman Shafiq bin Zulkifli - Initial work

10. Acknowledgements
- To Yunus, a student under the tutelage of Dr.Azliza Mohd Ali (supervisor) for guiding me through the implementation of IoT using mqtt
- To Zubli Quzaini, a batchmate of CS259 in UiTM for aiding me in refining the code provided by Yunus to produce a version 2.0.

