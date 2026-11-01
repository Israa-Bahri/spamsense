# Dataset Limitations: SMS Spam Collection

**Source:** UCI Machine Learning Repository
**Task:** classify an SMS as spam or ham

## Key facts (confirm on the UCI page)
- About 5,500 English SMS messages, each labelled spam or ham
- Collected from a few public sources, mainly the UK and Singapore
- Far more ham than spam (roughly 87% ham, 13% spam)

## Limitations
- **Spam is not the same as fraud.** Spam is unwanted messages, such as ads and
  promotions. Fraud is deception to steal money or data. Many scams are spam, but
  not all spam is fraud, and some fraud is not labelled spam.
- **Dataset bias.** The messages come from specific countries, time periods, and
  writing styles. Messages from Nigeria, Tunisia, or in other languages may look
  different, so the model may perform worse on them.
- **Old data.** Scam tactics change, and newer ones (WhatsApp links, fake
  payment alerts) may not appear.
- **Class imbalance.** With few spam examples, accuracy alone can look good even
  when the model misses spam.
- **Text only.** It has no links, sender details, or transaction data.

## Claims to avoid
- "FraudGuard detects fraud"
- "The model is 98% accurate" (without saying on which data)

## Safe wording
- "A spam/ham classifier trained on the SMS Spam Collection dataset."
- "Demo only. Not a reliable fraud detector."