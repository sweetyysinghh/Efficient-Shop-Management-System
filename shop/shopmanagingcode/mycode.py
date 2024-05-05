import serial
import datetime
import csv

ser = serial.Serial('COM5', 9600)  # Replace 'COM5' with your Arduino's serial port

with open('output.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    # Add "Day" to the CSV header
    writer.writerow(["Date", "Day", "Time", "Millis Since Start", "Customer Count", "Article Purchased"])

    while True:
        if ser.inWaiting() > 0:
            line = ser.readline().decode('utf-8').strip()
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            day_str = now.strftime("%A")  # Retrieves full weekday name
            time_str = now.strftime("%H:%M:%S")
            millis, customerCount, articlePurchased = line.split(',')
            # Include day_str in the data list
            data = [date_str, day_str, time_str, millis, customerCount, articlePurchased]
            writer.writerow(data)
            print(data)
