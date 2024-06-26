# WhatsApp Chat Analyzer

This script allows you to analyze your WhatsApp chat messages and visualize various statistics using Python. 

Here are some examples of the graphs that are created:

![hist_mess_per_day](https://github.com/WeridFire/WhatsAppChatAnalyzer/assets/69721649/608f3fe4-d15f-4612-94c2-b19eab417683)

![pie_mess](https://github.com/WeridFire/WhatsAppChatAnalyzer/assets/69721649/3b3dc426-f44e-4f63-b5b8-d7696a97055a)

![hist_most_words](https://github.com/WeridFire/WhatsAppChatAnalyzer/assets/69721649/93d55e80-88c1-4c6a-9e02-b8de306edf38)

## Features

- Analyze message frequency over time
- Calculate word counts and most frequent words
- Visualize chat activity using matplotlib

## Requirements

- Python 3
- matplotlib

## Installation

You can install the required packages using pip:

```bash
pip install matplotlib
```

## Analyze your first chat

### Base Configuration

1. Clone this Repository.
2. Export the relevant chat from WhatsApp and rename it "chat.txt".
3. Place the "chat.txt" file in the cloned folder.

### Personalize your Data

- "stopwords.txt": write here the words you DON'T want to count in the graphs.

- "specialwords.txt": including words here will create a special hist about them. Too many words here can lead to worst results.
