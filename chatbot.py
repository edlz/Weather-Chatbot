import CYKParse
import Tree

import WeatherRequest


class UnknownParse(Exception):
    pass


requestInfo = {
    'requested_parameter': '',
    'chance_query': False,
    'metric': False,
    'location': '',
    'wind_speed': '',
    'humidity': '',
    'weather': '',
    'query': True
}
haveGreeted = False

# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.


def getSentenceParse(T):
    sentenceTrees = {k: v for k, v in T.items() if k.startswith('S/0')}
    # print(T)
    try:
        completeSentenceTree = max(sentenceTrees.keys())
    except ValueError:
        raise UnknownParse("Could not find full parse tree")
    # print(T[completeSentenceTree])

    return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.


def updateRequestInfo(Tr):
    global requestInfo
    requestInfo['query'] = True
    requestInfo['chance_query'] = False
    requestInfo['average'] = False
    lookingForLocation = False
    lookingForChance = False
    requested_parameter = ''

    for leaf in Tr.getLeaves():
        while type(leaf[1]) is Tree.Tree:
            leaf = leaf[1].getLeaves()[0]
        # print(leaf)
        if leaf[0] == 'Adverb':
            requestInfo['time'] = leaf[1]

        if lookingForLocation and (leaf[0] == 'Name' or leaf[0] == 'Unknown'):
            requestInfo['location'] = leaf[1]

        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False

        if leaf[1] == 'imperial' or leaf[1] == 'fahrenheit':
            requestInfo['query'] = False
            requestInfo['metric'] = False
        if leaf[1] == 'metric' or leaf[1] == 'celsius':
            requestInfo['query'] = False
            requestInfo['metric'] = True

        if lookingForChance:
            if leaf[1] == 'snow':
                requestInfo['additional_info'] = 'snow'
                requested_parameter += 'snow'
            if leaf[1] == 'rain':
                requestInfo['additional_info'] = 'rain'
                requested_parameter += 'rain'

        if leaf[1] == 'chance':
            lookingForChance = True
            requestInfo['chance_query'] = True
            requested_parameter = 'chance of '

        if leaf[1] == 'wind' or leaf[1] == 'speed':
            requested_parameter = 'wind speed'
        elif leaf[1] == 'temperature':
            requested_parameter = 'temperature'
        elif leaf[1] == 'weather':
            requested_parameter = 'weather'
        elif leaf[1] == 'humidity':
            requested_parameter = 'humidity'
        elif leaf[1] == 'precipitation' or leaf[1] == 'precip' or leaf[1] == 'rain':
            requested_parameter = 'precipitation'
        elif leaf[1] == 'pressure':
            requested_parameter = 'pressure'

    requestInfo['requested_parameter'] = requested_parameter

# Data request


def getTemperature(location):
    global requestInfo
    if requestInfo['metric']:
        units = 'm'
    else:
        units = 'f'

    data = WeatherRequest.get_weather(location, units)

    if 'current' in data.keys():
        requestInfo['location'] = data['location']['name']
        return str(data['current']['temperature'])
    else:
        return 'unknown'


def getHumidity(location):
    global requestInfo
    if requestInfo['metric']:
        units = 'm'
    else:
        units = 'f'

    data = WeatherRequest.get_weather(location, units)
    if 'current' in data.keys():
        requestInfo['location'] = data['location']['name']
        return str(data['current']['humidity'])
    else:
        return 'unknown'


def getWindSpeed(location):
    global requestInfo
    if requestInfo['metric']:
        units = 'm'
    else:
        units = 'f'

    data = WeatherRequest.get_weather(location, units)
    if 'current' in data.keys():
        requestInfo['location'] = data['location']['name']
        return str(data['current']['wind_speed'])
    else:
        return 'unknown'


def getWeather(location):
    global requestInfo

    data = WeatherRequest.get_weather(location, 'm')
    if 'current' in data.keys() and len(data['current']['weather_descriptions']) > 0:
        requestInfo['location'] = data['location']['name']
        return str(data['current']['weather_descriptions'][0])
    else:
        return 'unknown'


def getPrecipitation(location):
    global requestInfo
    if requestInfo['metric']:
        units = 'm'
    else:
        units = 'f'

    data = WeatherRequest.get_weather(location, units)
    if 'current' in data.keys():
        requestInfo['location'] = data['location']['name']
        return str(data['current']['precip'])
    else:
        return 'unknown'


def getPressure(location):
    global requestInfo

    data = WeatherRequest.get_weather(location, 'm')
    if 'current' in data.keys():
        requestInfo['location'] = data['location']['name']
        return str(data['current']['pressure'])
    else:
        return 'unknown'

# Format a reply to the user, based on what the user wrote.


def reply():
    global requestInfo
    # print(requestInfo)
    if not requestInfo['query']:    # not a query means settings change
        if requestInfo['metric']:
            print('Data will be in metric.')
        else:
            print('Data will be in imperial.')
        return
    if requestInfo['requested_parameter'] == '':
        print('Did not find any parameter to query.')
        return
    if requestInfo['location'] == '':
        print('Did not find any location to query.')
        return
    # print(requestInfo)

    rp = requestInfo['requested_parameter']

    response = 'The ' + rp + ' in ' + requestInfo['location'] + ' is '

    if requestInfo['chance_query']:
        response += 'unknown, data not accessible for free.'
    else:  # data for single point
        if rp == 'temperature':
            response += getTemperature(requestInfo['location']) + (
                ' degrees fahrenheit' if not requestInfo['metric'] else ' degrees celsius') + '.'
        if rp == 'humidity':
            response += getHumidity(requestInfo['location']) + '%.'
        if rp == 'wind speed':
            response += getWindSpeed(requestInfo['location']) + \
                f' {"km/h" if requestInfo["metric"] else  "mph"}.'
        if rp == 'weather':
            response += getWeather(requestInfo['location']) + '.'
        if rp == 'precipitation':
            response += getPrecipitation(requestInfo['location']) + \
                f' {"mm" if requestInfo["metric"] else  "inches"}.'
        if rp == 'pressure':
            response += getPressure(requestInfo['location']) + ' MB.'
    print(response)


def main():
    global requestInfo
    print('LOCATION NAMES MUST BE 1 WORD (no spaces). Unknown words are considered locations.')
    print('Enter "words" for list of words in lexicon. Need to use these words to create sentences. "q" to exit.')
    print('Enter "keywords" for list of parameters you can query.')

    while True:
        i = input('\n---:')
        if i == 'q':
            break
        elif i == 'words':
            for i in sorted(CYKParse.getGrammarWeather()['lexicon'], key=lambda x: x[1].lower()):
                print(i[1])
        elif i == 'keywords':
            for i in [['Noun', 'temperature', 0.6],
                      ['Noun', 'weather', 0.6],
                      ['Noun', 'precipitation', 0.6],
                      ['Noun', 'pressure', 0.6],
                      ['Noun', 'precip', 0.6],
                      ['Noun', 'rain', 0.6],
                      ['Noun', 'height', 0.6],
                      ['Noun', 'wind', 0.6],
                      ['Noun', 'speed', 0.6],
                      ['Noun', 'humidity', 0.6]]:
                print(i[1])

        else:
            i = i.rstrip("?.").lower()
            T = CYKParse.CYKParse(
                i.split(' '), CYKParse.getGrammarWeather())[0]
            try:
                sentenceTree = getSentenceParse(T)
                updateRequestInfo(sentenceTree)
                reply()
            except UnknownParse:
                print(
                    "Did not understand the sentence. Unknown words or grammer not implemented.")
            except WeatherRequest.APIConnectionProblem:
                print("Error connecting to API")


if __name__ == '__main__':
    main()
