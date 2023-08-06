# digicom

## What it is

This project is a collection of equations, calculations, and static variables
used in digital signals and communications.

## How to use

Most of the function in this module as oneline anonymous functions, the input
and output for each function are self explanitory.

#### Example of Use:
```python3
>> L = parse_sym('27.44 m') # H
>> C = parse_sym('891.7 p') #F, 

>> r_fr = round(resonant_freq(L,C)/10**3,3)
>> print('Resonant Frequency:\n\t fr =',r_fr,'kHz')

Resonant Frequency:
	 fr = 32.175 kHz

```

## Install

##### Local
```bash
$ pip install -r requiremnts.txt
$ pip install digicom/.
```

##### pip via PyPi
```bash
$ pip install digicom
```

