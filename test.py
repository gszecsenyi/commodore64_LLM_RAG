import serial
import time

def replace_special_characters(text):
    replacements = {
        'Ö': 'O', 'Ü': 'U', 'É': 'E', 'Á': 'A',
        'ö': 'o', 'ü': 'u', 'é': 'e', 'á': 'a'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

ser = serial.Serial('/dev/ttys016', baudrate=300, timeout=2)

duration = 300  # Duration in seconds
interval = 3  # Interval in seconds

start_time = time.time()

while time.time() - start_time < duration:
    question = ser.readline().decode('ascii').rstrip()
    print(f"Received from VICE: {question}")
    time.sleep(interval)
    
    if question:
        answer = f"This was the original question: {question}"
        answer = replace_special_characters(answer)
        text = answer.upper().encode('ascii', 'ignore')
        
        ser.write(text)
        print(f"Sent to VICE: {answer}")

print("Exiting...")

ser.close()