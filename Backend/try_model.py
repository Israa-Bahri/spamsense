# Import joblib to load the saved model
import joblib

# Load the pipeline we saved earlier (safe: we created this file ourselves)
pipeline = joblib.load("spam_pipeline.joblib")

# The class names the model knows: ['ham', 'spam']
classes = list(pipeline.classes_)


def check(message):
    """Predict one message and print the result."""
    # The pipeline expects a LIST of messages, so we wrap it in [ ]
    prediction = pipeline.predict([message])[0]

    # predict_proba gives the model's confidence for each class
    probs = pipeline.predict_proba([message])[0]
    spam_prob = probs[classes.index("spam")]

    print(f"\nMessage:    {message}")
    print(f"Prediction: {prediction}")
    print(f"Spam score: {spam_prob:.0%}")


# ===== PART 1: a fixed list of examples =====
examples = [
    "URGENT! You have won a free prize. Click here to claim now",
    "Are we still meeting at 5pm?",
    "Congratulations! Reply WIN to get a free ticket",
    "Can you send me the notes from class?",
    "Your bank account is locked. Verify your password now",
]

for text in examples:
    check(text)

# ===== PART 2: type your own messages =====
print("\n--- Type your own messages (type 'q' to quit) ---")
while True:
    text = input("\nYour message: ")
    if text.strip().lower() == "q":   # stop when you type q
        break
    if text.strip() == "":            # ignore empty input
        continue
    check(text)