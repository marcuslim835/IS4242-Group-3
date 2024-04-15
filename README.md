# Academic Year 2023/2024 Semester 2
**IS4242 Group 3**

## EmoVoice: Human Voice Emotion Recognition
![alt text](favicon.png)

![alt text](readme_resources/tkinter1.png)
![alt text](readme_resources/tkinter2.png)

## Initial Setup
1. Run `pip install -r requirements.txt` in command prompt
2. Run the command `mlflow ui` in command prompt to start mlflow on localhost
3. Run `initialModelTraining.py` to create and store the model on mlflow

## To run the application to predict audio
1. Run the command `mlflow ui` in command prompt to start mlflow on localhost (if it has not already been started)
2. Run `tkinter_frontend.py`

## To check on the model

### Manually checking model training performance
1. Go to `localhost:5000` on your browser
2. Under `Experiments` >> `Training - Audio Emotion Predictor`, select the only model.

![alt text](readme_resources/model1.png)

3. The model parameter and metrics are displayed here. You can view the model metrics and artifacts by clicking on the tabs on the top.

![alt text](readme_resources/model2.png)

### Manually checking predictions
1. Go to `localhost:5000` on your browser
2. Under `Experiments` >> `Predictions - Audio Emotion Predictor`, pick the run you are interested in.

![alt text](readme_resources/experiment1.png)

3. The prediction is stored as the metric `Prediction`. The following is the mapping: {"angry": 1, "happy": 2, "neutral": 3, "sad": 4}.

![alt text](readme_resources/experiment2.png)