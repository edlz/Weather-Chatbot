import requests

# replace with your own key here from http://api.weatherstack.com/
access_key = 'cf80e95cd3b4b958399b4b07034cb876'


class APIConnectionProblem(Exception):
    pass


def get_weather(location, units):
    api_result = requests.get(
        f'http://api.weatherstack.com/current?access_key={access_key}&query={location}&units={units}')

    api_response = api_result.json()

    # print(api_response)
    if 'success' in api_response:
        print(api_response)
        raise APIConnectionProblem
    return api_response


get_weather('irvine', 'm')
