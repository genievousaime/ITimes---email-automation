import csv
import random
import json
import datetime
from urllib import request
import tweepy


#function for getting a random quote.
def get_random_quote(quotes_file='/Users/shashwathbhaskar/cpp:c vs code/ITimes/quotes_temp.csv'):# load motivational quotes from csv file 
    try: # load motivational quotes from csv file 
       with open(quotes_file) as csvfile:
           quotes = [{'author': line[0],
                      'quote': line[1]} for line in csv.reader(csvfile, delimiter='|')]

    except Exception as e: # use a default quote to help things turn out for the best
        quotes = [{'author': 'Eric Idle',
                   'quote': 'Always Look on the Bright Side of Life.'}]
    
    return random.choice(quotes)



#function to get the weather report of the given location( 3hr interval)
def get_weather_forecast(coords={'lat': 23.077690141460607, 'lon': 76.8512637110035}): # default location at VIT Bhopal
    try: # retrieve forecast for specified coordinates
        api_key = 'cabd63d512db5b3272467b5cd073e194'
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {'city': data['city']['name'], # city name
                    'country': data['city']['country'], # country name
                    'periods': list()} # list to hold forecast data for future periods

        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        
        return forecast
    except Exception as e:
        print(e)   
        
        
        
#function to get Top 10 twitter trends in India
def get_twitter_trends(woeid=2295407): # default WOEID for INDIA
    try: # retrieve Twitter trends for specified location
        api_key = 'ZlJRDgHE97PDymRGrqpHXTcLz'
        api_secret_key = 'Bqw4sexqoEOV26BAWl5StkNJwTJTcNatGFdHtgznBeDWMAzScM'
        auth = tweepy.AppAuthHandler(api_key, api_secret_key)
        return tweepy.API(auth).trends_place(woeid)[0]['trends'] # NOTE: Tweepy 4.0.0 renamed the 'trends_place' method to 'get_place_trends'

    except Exception as e:
        print(e)

if __name__ == '__main__':
    ##### test get_random_quote() #####
    print('\nTesting quote generation...')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')
    
    
    ##### test get_weather_forecast() #####
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')
            
    
    ##### test get_twitter_trends() #####
    print('\nTesting Twitter trends retrieval...')

    trends = get_twitter_trends() # get trends for default location of India
    if trends:
        print('\nTop 10 Twitter trends in India are...')
        for trend in trends[0:10]: # show top ten
            print(f' - {trend["name"]}: {trend["url"]}')

    
    
