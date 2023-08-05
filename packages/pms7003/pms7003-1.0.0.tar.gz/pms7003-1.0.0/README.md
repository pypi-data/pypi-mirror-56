# A minimalistic python interface for PMS7003 sensor

The code reads PM values from serial port. Tested on Raspberry Pi, but it should work on any machine with Python and serial port.

Device description: <https://aqicn.org/sensor/pms5003-7003/>

## Usage example

```python
from pms7003 import Pms7003Sensor, PmsSensorException

if __name__ == '__main__':

    sensor = Pms7003Sensor('/dev/serial0')

    while True:
        try:
            print(sensor.read())
        except PmsSensorException:
            print('Connection problem')

    sensor.close()
```

The read function has an option of returning values as a dict or OrderedDict.

```python
sensor.read(ordered=True)
```

## Threading

Threading support is currently __very unstable__.
