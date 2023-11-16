#source env/bin/activate
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
import os

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

print("{:>5}\t{:>5}".format('raw', 'v'))
print("Disconnect the power from the supercap now!")

try:
    with open("/home/pi/vanpi/adc_readings.txt", "a") as file:
        while True: 
            timestamp = datetime.now().isoformat()
            reading_raw = chan.value
            reading_voltage = chan.voltage
            print("{:>5}\t{:>5.3f}".format(reading_raw, reading_voltage))
            file.write(f"{timestamp} {reading_raw} {reading_voltage}\n")
            file.flush()  # Ensure the reading is written to the file immediately
            os.fsync(file.fileno())  # Ensure the changes are flushed to disk immediately
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")