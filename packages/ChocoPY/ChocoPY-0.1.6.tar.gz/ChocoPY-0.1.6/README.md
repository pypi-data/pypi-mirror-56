[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ff39f9b1d7814063bae9cb7c4a18e7c3)](https://www.codacy.com/manual/mallycrip/ChocoPY?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mallycrip/ChocoPY&amp;utm_campaign=Badge_Grade)

# CHOCOPY

The chocoPY is easy and simple development tool for Chatbot

## How to install

> pip install chocopy



## Minimal Application

```python
from flask import Flask
from chocopy import ChocoPY

app = Flask(__name__)
ChocoPY(app)
```