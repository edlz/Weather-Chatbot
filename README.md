# Weather Chatbot using CYK algorithm

## Requirements

1. Need a working internet connection

2. Python needs to be installed, used python version 3.8.2 but any compatible version should work

3. The python module Requests needs to be installed using pip

   - open terminal in the folder containing the chatbot files
   - run the command bellow in the terminal
   - `python -m pip install requests`

4. Must replace `access_key` in [`./WeatherRequest.py`](./WeatherRequest.py) with an API key from [weatherstack API](https://weatherstack.com/product).

## Running

1. Open the terminal in the folder containing the chatbot files
2. Run the command `python chatbot.py`

## Limitations

1.  This chatbot only supports words defined in [CYKParse.py](./CYKParse.py) under the `getGrammarWeather` function. Any words not supported are parsed as locations. See input handling below for more details.

2.  When asking for weather data, locations need to be 1 word with no spaces in between. Consider hyphens or removing the space between the words.

    ### Input Handling

    - The chatbot makes the assumption that the unknown category is a location. It is implemented this way because the weatherstack api allows misspellings in its query so it will be easier to make queries this way.

## Example Inputs

- `What is the weather in Irvine?`
  - Chatbot: `The weather in irvine is Rain, Mist.`
- `How much rain?`
  - Chatbot: `The precipitation in Irvine is 0 inches.`
- `Use the metric system`
  - Chatbot: `Data will be in metric.`
- `How much rain?`
  - Chatbot: `The precipitation in Irvine is 0.3 mm.`
- `What is the temperature in Chicago?`
  - Chatbot: `The temperature in chicago is 1 degrees celsius.`
- `What is the wind speed`
  - Chatbot: `The wind speed in Chicago is 30 km/h.`
- `What is the humidity?`
  - Chatbot: `The humidity in Chicago is 38%.`

## Supported words

### (not including locations)

```
a
am
average
be
celsius
chance
fahrenheit
frost
height
hello
hi
highest
how
humidity
I
imperial
in
is
last
lowest
man
metric
much
my
name
next
now
of
overcast
precip
precipitation
pressure
rain
snow
speed
sunshine
system
temperature
the
this
thunder
today
tomorrow
use
weather
week
weekly
what
when
which
will
wind
with
yesterday
```
