# commodore64 LLM RAG application with Python backend

## The C64 application
![Screenshot](img/screenshot_with_issue.png)

## Setup the environment

### Configure the serial port

```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

Two serial devices will appear, one to be typed into the emulator and the other into the Python code.

### Setup the C64 emulator

![Vice emulator](img/vice_screenshot.png)

## Sample file

Sample file is from here: https://pickledlight.blogspot.com/p/commodore-64-guides.html

## Connection test

There is a test.py file to test the connection between the C64 emulator and the Python environment. 



