The model can't read words. It only understands numbers. TF-IDF turns each message into a list of numbers, where each number says how important a word is in that message.
exemple:
1. "win a free prize now"
2. "are you free today"
3. "see you at the meeting"

Word	        Where it appears	    Score
prize	        only message 1	        High (rare, so distinctive)
free	        messages 1 and 2	    Medium
you	            messages 2 and 3	    Low-medium
the / a / at	common filler           Low

    What the output looks like

Each message becomes a row of numbers, one column per word:

              prize   free   you   meeting  ...
message 1     0.62    0.48   0.00   0.00
message 2     0.00    0.44   0.52   0.00
message 3     0.00    0.00   0.41   0.60