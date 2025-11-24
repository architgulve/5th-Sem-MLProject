import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve, auc
import matplotlib.pyplot as plt

MODEL_DIR = "../models"
PROC_DIR = "../data/processed"

def load():
    model = joblib.load(MODEL_DIR + "/best_model.joblib")
    df = pd.read_parquet(PROC_DIR + "/oulad_per_student.parquet")
    X = df.drop(columns=["dropout","id_student","code_module","code_presentation"], errors="ignore")
    y = df["dropout"].astype(int)
    return model,X,y

def evaluate():
    model,X,y = load()
    p = model.predict_proba(X)[:,1]
    y_pred = (p >= 0.5).astype(int)  # default threshold
    print(classification_report(y, y_pred, digits=4))
    print("ROC AUC:", roc_auc_score(y, p))
    # precision-recall curve
    prec, rec, th = precision_recall_curve(y, p)
    pr_auc = auc(rec, prec)
    print("PR AUC:", pr_auc)
    # plot PR curve
    plt.figure()
    plt.plot(rec, prec)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall curve (PR AUC=%.4f)" % pr_auc)
    plt.savefig("pr_curve.png")

if __name__ == "__main__":
    evaluate()
