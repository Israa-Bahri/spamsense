# ML Task: Spam Classification

**Task type:** Classification (supervised learning, 2 classes)

## Definitions
- **input** = message (the text of an SMS or email)
- **label** = spam or ham (the true answer; ham = a normal, legitimate message)
- **prediction** = estimated label (the model's guess for a new message)

## Examples
| input | label (true) | prediction (model) |
|---|---|---|
| "URGENT! You won a prize, click here" | spam | spam |
| "Are we still meeting at 5pm?" | ham | ham |

## How it works
1. Train the model on messages that already have labels.
2. Give it a new message (input).
3. It returns a prediction: spam or ham.
4. Compare prediction with label to measure accuracy.

## Goal
Understand the ML task: given a message, classify it as spam or ham.