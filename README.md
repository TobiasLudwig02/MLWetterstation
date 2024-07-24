# ML_Wetterstation

University project for the course "Machine Learning Project"

Weather app:
Arduino_code has the code which runs on the arduino to collect and send the data
apiappwetterstation.py is an app hosted on azure which works as an api endpoint and collects the data from the arduino and sends it into an db
test_connection.py is a local programm to test if the api endpoints works
streamlitapp.py is the app hosted on azure to visualize the collected data
requirements.txt contains all necessary libs to deploy both apps
folder assets contains some assets for the streamlit app

Training of forecast models
model_train.ipynb contains the training and evaluation of different models for weather forecast
folder data contains the training data
folder models contains the trained models
train_requirements.txt contains all necessary libs for training

The app should be availible via: streamlitwetterstation.azurewebsites.net

A presentation video is available via: https://youtu.be/Qb1l3KKBpUI![image](https://github.com/user-attachments/assets/f7f3a8b3-7ec5-45c3-bff3-891419735055)
