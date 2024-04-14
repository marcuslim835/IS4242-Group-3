import mlflow
import pandas as pd
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')


class DataML:
    """
    Class for data processing and prediction
    """
    def __init__(self, path):
        self.predictionMapper = {"angry": 1, "happy": 2, "neutral": 3, "sad": 4}
        self.path = path

    def processAudioClip(self, path):
        def extract_mfcc(filename):
            y, sr = librosa.load(filename, duration=3, offset=0.5)
            mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
            return mfcc
        def extract_chroma(filename):
            y, sr = librosa.load(filename)
            chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
            return chroma
        def extract_spectral_contrast(filename):
            y, sr = librosa.load(filename)
            contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)
            return contrast
        def extract_tonnetz(filename):
            y, sr = librosa.load(filename)
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
            return tonnetz
        def processData(df):
            # mfcc
            mfcc_columns = ['mfcc_' + str(i) for i in range(1, 41)]
            mfcc_df = pd.DataFrame(df['speech'].apply(lambda x: extract_mfcc(x)).tolist(), columns=mfcc_columns)
            new_df = pd.concat([df, mfcc_df], axis=1)

            # chroma 
            chroma_columns = ['chroma_' + str(i) for i in range(1, 13)]
            chroma_df = pd.DataFrame(df['speech'].apply(lambda x: extract_chroma(x)).tolist(), columns=chroma_columns)
            new_df = pd.concat([new_df, chroma_df], axis=1)

            # spectral_contrast
            spectral_columns = ['spectral_' + str(i) for i in range(1, 8)]
            spectral_df = pd.DataFrame(df['speech'].apply(lambda x: extract_spectral_contrast(x)).tolist(), columns=spectral_columns)
            new_df = pd.concat([new_df, spectral_df], axis=1)

            # tonnetz
            tonnetz_columns = ['tonnetz_' + str(i) for i in range(1, 8)]
            tonnetz_df = pd.DataFrame(df['speech'].apply(lambda x: extract_spectral_contrast(x)).tolist(), columns=tonnetz_columns)
            new_df = pd.concat([new_df, tonnetz_df], axis=1)
            return new_df
        data = processData(pd.DataFrame({"speech": [path]}))
        data = data[['mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5',
                    'mfcc_6', 'mfcc_7', 'mfcc_9', 'mfcc_10', 'mfcc_12', 'mfcc_14',
                    'mfcc_15', 'mfcc_17', 'mfcc_19', 'mfcc_20', 'mfcc_22', 'mfcc_23',
                    'mfcc_24', 'mfcc_25', 'mfcc_26', 'mfcc_27', 'mfcc_28', 'mfcc_29',
                    'mfcc_30', 'mfcc_31', 'mfcc_32', 'mfcc_33', 'mfcc_34', 'mfcc_36',
                    'mfcc_37', 'mfcc_38', 'mfcc_39', 'mfcc_40', 'chroma_1', 'chroma_8',
                    'spectral_1', 'spectral_2']]
        return data

    def getPredictionResults(self) -> int:
        data = self.processAudioClip(self.path)
        # Set tracking server uri for logging
        mlflow.set_tracking_uri(uri="http://localhost:5000")
        # Create a new MLflow Experiment
        mlflow.set_experiment(f"Predictions - Audio Emotion Predictor")
        # Start an MLflow run
        with mlflow.start_run():
            mlflow.autolog()
            mlflow.set_tag("Testing Info", f"Predicting using Random Forest Predictor")
            model = mlflow.pyfunc.load_model(model_uri=f"models:/random_forest_model/latest")
            testPredict = model.predict(data).item()
            mlflow.log_metric("Prediction", int(self.predictionMapper.get(testPredict, 0)))
        return self.predictionMapper.get(testPredict, 0)