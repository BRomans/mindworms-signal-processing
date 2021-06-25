# Mindworms Signal Processing
Module that handles signal processing and streams EEG data to the Unity game client.

## Setup 

- Create a folder for virtual environment:

   
`mkdir vpy-3.7`

- Create virtual environment using virtual env:

(Windows)
    `virtualenv -p C:\Users\{your-user-name}\AppData\Local\Programs\Python\Python37\python.exe vpy-3.7`

(Unix)
    `virtualenv --python=//opt/pyenv/python/3.7/bin/python vpy-3.7`

- Activate virtual environment:

(Windows)
    `source vpy-3.7/Scripts/active`

(Unix)
    `source vpy-3.7/bin/active`

- Install dependencies:

`pip install -r requirements.txt`

- Run the application:

`python mindworms_signal_processing.py`