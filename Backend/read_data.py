import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

#LOAD THE DATA
df = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="latin-1",
)

#INSPECT
print("Rows before cleaning:", len(df))
print(df["label"].value_counts())
print(df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

#CLEAN
df = df.dropna()
df = df.drop_duplicates(subset="message")
print("Rows after cleaning:", len(df))

# SPLIT
X = df["message"]   # input
y = df["label"]     # label

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)
print("Train size:", len(X_train), "| Test size:", len(X_test))

#PIPELINE+TRAIN
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("model", LogisticRegression(max_iter=1000)),
])
pipeline.fit(X_train, y_train)   # capital X_train, small y_train

#TEST
y_pred = pipeline.predict(X_test)
pd.set_option("display.max_colwidth", None)

test_size_before = len(X_test)

#Confusion matrix, with clear labels
cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
cm_df = pd.DataFrame(
    cm,
    index=["true ham", "true spam"],       # rows = the real label
    columns=["pred ham", "pred spam"],     # columns = the model's prediction
)
print("\nConfusion matrix:")
print(cm_df)

#Pull out the four numbers (spam is the "positive" class)
tn, fp, fn, tp = cm.ravel()
print(f"\nCorrect ham: {tn} | Correct spam: {tp}")
print(f"False alarms (ham called spam): {fp}")
print(f"Missed spam (spam called ham): {fn}")

#results table 
results = pd.DataFrame({
    "message": X_test,
    "label": y_test,
    "prediction": y_pred,
})

#Prediction prob(0.00 to 1.00)
spam_col = list(pipeline.classes_).index("spam")
results["spam_prob"] = pipeline.predict_proba(X_test)[:, spam_col].round(2)

#Split the mistakes into the two types
false_alarms = results[(results["label"] == "ham") & (results["prediction"] == "spam")]
missed_spam = results[(results["label"] == "spam") & (results["prediction"] == "ham")]

#Inspect a few of each 
print("\nFALSE ALARMS (real ham, predicted spam):")
print(false_alarms.head(5))

print("\nMISSED SPAM (real spam, predicted ham):")
print(missed_spam.head(5))

# Compare average message length (in words): mistakes vs all test messages
results["words"] = results["message"].str.split().str.len()
wrong = results[results["label"] != results["prediction"]]
print("\nAverage words, all test messages:", round(results["words"].mean(), 1))
print("Average words, wrong predictions: ", round(wrong["words"].mean(), 1))

#Prove the test set was not changed
print("\nTest set size before/after:", test_size_before, "/", len(X_test))
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

results = pd.DataFrame({
    "message": X_test,
    "label": y_test,
    "prediction": y_pred,
})
print("\nFirst 10 test results:")
print(results.head(10))

print("\nConfusion matrix (rows=true, cols=predicted):")
print(confusion_matrix(y_test, y_pred, labels=["ham", "spam"]))

wrong = results[results["label"] != results["prediction"]]
print("\nWrong predictions:", len(wrong), "out of", len(results))
print(wrong.head(10))



#THE TRAINED PIPELINE
#TF-IDF + model together into ONE file in the Backend folder
joblib.dump(pipeline, "spam_pipeline.joblib")
print("Model saved to spam_pipeline.joblib")

#CHECK THE SAVED FILE WORKS 
# Load it back (safe here: we created this file ourselves)
loaded = joblib.load("spam_pipeline.joblib")

test_message = ["URGENT! You won a free prize, click here to claim"]
print("Prediction from loaded model:", loaded.predict(test_message)[0])