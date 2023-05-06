from flask import Flask
from datetime import datetime
import csv
import requests
app = Flask(__name__)

@app.route('/master')
def master():
    url = "http://localhost:5000/monitor"
    k = 1  # default interval value
    response = requests.get(url, params={"k": k})
    data = response.text.split(" | ")
    cpu_percent = float(data[0].split(": ")[1].strip("%"))
    mem_percent = float(data[1].split(": ")[1].strip("%"))

    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')

    # Write data to CSV file
    with open('monitor_log.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu_percent, mem_percent])

    return "Resource utilization logged successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    time.sleep= (10)