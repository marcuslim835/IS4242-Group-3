import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve, auc, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import label_binarize
from itertools import cycle
import mlflow
from mlflow.models import infer_signature

def loadData():
    data = pd.read_csv('Notebooks/IS4242 Data.csv')
    data.shape
    # Data Splitting
    X = data.drop(columns=["label", "speech"])
    y = data["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y)
    return X_train, X_test, y_train, y_test

def evaluate_model(model, model_name, x_test, y_test):
    # Binarize the output
    classes = np.unique(y_test)
    y_test_binarized = label_binarize(y_test, classes=classes)

    # Predict probabilities for each class
    y_probs = model.predict_proba(x_test)

    # Compute ROC curve and ROC area for each class
    n_classes = y_test_binarized.shape[1]
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_binarized[:, i], y_probs[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_binarized.ravel(), y_probs.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    # Plot ROC curve for a specific class
    plt.figure(figsize=(10, 8))
    colors = cycle(['blue', 'red', 'green', 'orange'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})'.format(classes[i], roc_auc[i]))
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Receiver Operating Characteristic for {model_name}')
    plt.legend(loc="lower right")
    plt.show()

    # Additional evaluation metrics
    y_pred = model.predict(x_test)
    print(f'Accuracy Score for {model_name}: {model.score(x_test, y_test)}')
    print(f'Classification Report for {model_name}:\n{classification_report(y_test, y_pred)}')
    print(f'Confusion Matrix for {model_name}:\n{confusion_matrix(y_test, y_pred)}')
    print(f'F1 Score (weighted) for {model_name}: {f1_score(y_test, y_pred, average="weighted")}')

def trainModel(X_train, X_test, y_train, y_test):
    # Set tracking server uri for logging
    mlflow.set_tracking_uri(uri="http://localhost:5001")
    # Create a new MLflow Experiment
    mlflow.set_experiment(f"Training - Audio Emotion Predictor")
    with mlflow.start_run():
        mlflow.autolog()
        mlflow.set_tag("Training Info", f"Initialize Random Forest Predictor")
        # Initialize the Random Forest model with a random state
        random_forest_model = RandomForestClassifier(random_state=42)
        random_forest_model.fit(X_train, y_train)
        evaluate_model(random_forest_model, "Random Forest", X_test, y_test)
        # make predictions
        trainPredict = random_forest_model.predict(X_train)
        # Infer the model signature
        signature = infer_signature(X_train, trainPredict)
        # Log the model
        model_info = mlflow.sklearn.log_model(
            sk_model=random_forest_model,
            artifact_path=f"random_forest_model",
            signature=signature,
            input_example=X_train,
            registered_model_name=f"random_forest_model"
        )
        # Note down this model uri to retrieve the model in the future for scoring
        print(model_info.model_uri)

def main():
    X_train, X_test, y_train, y_test = loadData()
    trainModel(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()