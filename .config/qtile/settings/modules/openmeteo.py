# -*- coding:utf-8 -*-
# Copyright (c) 2020 Himanshu Chauhan
# Copyright (c) 2020 Stephan Ehlers
# Copyright (c) 2024 Hans Matzen adapted to openmeteo.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
from typing import Any
from urllib.parse import urlencode
from libqtile.widget.generic_poll_text import GenPollUrl
import json
from qtile_extras.widget.mixins import TooltipMixin
from libqtile.log_utils import logger
    
#
# class for fetching weatherdata from openemeteo.com and display it as a widget
# including simple weather forecast data a widget tooltip
#
class OpenMeteo(GenPollUrl, TooltipMixin):
    """A widget for the Qtile windowmanager to display weather data and a simple forecast from openmeteo.com.
    
        Place the file openmeteo.py in your .config/qtile directory and add the following to you config.py:
        
        import openmeteo
        ...
        
        widgets_list = [
        ...
        ...
        ...
        # openmeteo weather widget
        openmeteo.OpenMeteo( foreground='#dfdfdf', background='#000000', lat=50.1109, lon=8.6821, location='Frankfurt am Main', 
                             metric=True, tooltip_fontsize=12, update_interval=600, language='de' ),
        ...
        ...
        ...
        ]
        
        See defaults below for a list of parameters.
        update_interval is in seconds, if you leave language unset it defaults to english.
    """


    # WMO Weather interpretation codes (WW)
    # Code	        Description
    # 0	            Clear sky
    # 1, 2, 3	    Mainly clear, partly cloudy, and overcast
    # 45, 48	    Fog and depositing rime fog
    # 51, 53, 55	Drizzle: Light, moderate, and dense intensity
    # 56, 57	    Freezing Drizzle: Light and dense intensity
    # 61, 63, 65	Rain: Slight, moderate and heavy intensity
    # 66, 67	    Freezing Rain: Light and heavy intensity
    # 71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
    # 77	        Snow grains
    # 80, 81, 82	Rain showers: Slight, moderate, and violent
    # 85, 86	    Snow showers slight and heavy
    # 95 	        Thunderstorm: Slight or moderate
    # 96, 99 	    Thunderstorm with slight and heavy hail

    wmo_symbols_day= {
       "Default": "✨",
        "0": "☀️",
        "1": "🌤️", "2": "🌤️", "3": "🌤️",
        "45": "🌫", "48": "🌫",
        "51": "🌧️", "53": "🌧️", "55": "🌧️",
        "56": "❄️","57": "❄️",
        "61": "🌧️", "63": "🌧️", "65": "🌧️",
        "66": "❄️","67": "❄️",
        "71": "❄️","73": "❄️","75": "❄️",
        "77": "❄️",
        "80": "🌧️", "81": "🌧️", "82": "🌧️",
        "85": "❄️", "86": "❄️",
        "95": "⛈", 
        "96": "🌩", "99": "🌩",
    }
    
    wmo_symbols_night= {
       "Default": "✨",
        "0": "🌕",
        "1": "☁️️", "2": "☁️️", "3": "☁️️",
        "45": "🌫", "48": "🌫",
        "51": "🌧️", "53": "🌧️", "55": "🌧️",
        "56": "❄️","57": "❄️",
        "61": "🌧️", "63": "🌧️", "65": "🌧️",
        "66": "❄️","67": "❄️",
        "71": "❄️","73": "❄️","75": "❄️",
        "77": "❄️",
        "80": "🌧️", "81": "🌧️", "82": "🌧️",
        "85": "❄️", "86": "❄️",
        "95": "⛈", 
        "96": "🌩", "99": "🌩",
    } 
     
    symbols_owm = {
        "Unknown": "✨",
        "01d": "☀️",
        "01n": "🌕",
        "02d": "🌤️",
        "02n": "☁️",
        "03d": "🌥️",
        "03n": "☁️",
        "04d": "☁️",
        "04n": "☁️",
        "09d": "🌧️",
        "09n": "🌧️",
        "10d": "⛈",
        "10n": "⛈",
        "11d": "🌩",
        "11n": "🌩",
        "13d": "❄️",
        "13n": "❄️",
        "50d": "🌫",
        "50n": "🌫",
    }

    defaults: list[tuple[str, Any, str]] = [
        (
            "lat",
            None,
            """The latitude of the location, e.g. lat=50.23 """,
        ),
        (
            "lon",
            None,
            """The longitude of the location, e.g. lon=8.6 """,
        ),
        (
            "location",
            '',
            """Name of your location as text, e.g. location="somewhere" """,
        ),
        (
            "format",
            "{location}: {temp} °C {icon} {weather_details}",
            "Display format",
        ),
        (
            "format_forecast",
            "{day} {temp}°C {weather_details}",
            "Display format for forecast",
        ),
        (
            "metric", 
            True, 
            "True to use metric/C, False to use imperial/F",
        ),
        (
            "dateformat",
            "%d.%m",
            """Format for dates as in strftime""",
        ),
        (
            "timeformat",
            "%H:%M",
            """Format for times, as in strftime""",
        ),
        (
            "language",
            "en",
            """Language of response, e.g. 'en'""",
        ),
    ]

    # See documentation: https://open-meteo.com
    query_url = 'https://api.open-meteo.com/v1/forecast?';

    # wind directions
    wind_directions_en = [ "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", ]
    wind_directions_de = [ "N", "NNO", "NO", "ONO", "O", "OSO", "SO", "SSO", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", ]
    
    # constructor
    def __init__(self, **config):
        GenPollUrl.__init__(self, **config)
        self.add_defaults(OpenMeteo.defaults)
        
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.tooltip_background='#888888'
        
        if not self.lat or not self.lon:
            return None

        # build url
        urlparms = '&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m'
        urlparms = urlparms + '&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,&timeformat=unixtime&timezone=auto';
		# add non metric parms to url.
        if not self.metric:
            urlparms = urlparms + '&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch';
		
        url = self.query_url + 'latitude=' + str( self.lat ) + '&longitude=' + str( self.lon ) + urlparms;
        self.url = url
        

    def parse(self, response):
        data = response
        data["location_lat"] = self.lat
        data["location_lon"] = self.lon
        data["sunrise"] = time.strftime(self.timeformat, time.localtime( data['daily']['sunrise'][0] )) 
        data["sunset"] = time.strftime(self.timeformat, time.localtime( data['daily']['sunset'][0] )) 
        data["isotime"] = time.strftime(self.dateformat + self.timeformat, time.localtime( data['current']['time'] ))
        data["wind_direction"] = self.degrees_to_direction(data['current']['wind_direction_10m'])
        data["weather"] = data["current"]["weather_code"]
        data["weather_details"] = self.wmocode2text( data["current"]["weather_code"] )
        data["humidity"] = data["current"]["relative_humidity_2m"]
        data["pressure"] = data["current"]["pressure_msl"]
        data["temp"] = data["current"]["temperature_2m"]
                
        data["units_temperature"] = "C" if self.metric else "F"
        data["units_wind_speed"] = "Km/h" if self.metric else "m/h"
        data["location"] = self.location
        data['icon'] = self.wmo_symbols_day["Default"]
        if data['current']['is_day'] == 1:
            data["icon"] = self.wmo_symbols_day[str(data["current"]["weather_code"])]
        else:
            data["icon"] = self.wmo_symbols_night[str(data["current"]["weather_code"])]

        # forecast
        fc=""
        fc1=""
        
        for i in range(1,4):
            d=dict()
            d['day'] = time.strftime(self.dateformat, time.localtime( data['daily']['time'][i] ))
            d['temp'] = str( data["daily"]["temperature_2m_max"][i] )
            d['icon'] = self.wmo_symbols_day[str(data["daily"]["weathercode"][i])]
            d['weather_details'] = self.wmocode2text( data["daily"]["weathercode"][i] )
            fc = fc + self.format_forecast.format(**d) + "\n"

        fc = fc[:-1] # cut last newline
        self.tooltip_text = fc

        return self.format.format(**data)

    # convert the wind direction in degrees to a direction
    def degrees_to_direction(self, degrees):
        val = int(degrees / 22.5 + 0.5)
        
        if self.language=='en':
            wdir = self.wind_directions_en[(val % 16)]
        if self.language=='de':
            wdir = self.wind_directions_de[(val % 16)]
            
        return wdir

    # convert a WMO weathercode to a textual description
    def wmocode2text(self, wmocode):
        # WMO Weather interpretation codes (WW)
        # Code	        Description
        # 0	            Clear sky
        # 1, 2, 3	    Mainly clear, partly cloudy, and overcast
        # 45, 48	    Fog and depositing rime fog
        # 51, 53, 55	Drizzle: Light, moderate, and dense intensity
        # 56, 57	    Freezing Drizzle: Light and dense intensity
        # 61, 63, 65	Rain: Slight, moderate and heavy intensity
        # 66, 67	    Freezing Rain: Light and heavy intensity
        # 71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
        # 77	        Snow grains
        # 80, 81, 82	Rain showers: Slight, moderate, and violent
        # 85, 86	    Snow showers slight and heavy
        # 95 	        Thunderstorm: Slight or moderate
        # 96, 99 	    Thunderstorm with slight and heavy hail
    
        wmo_text_en = {
           "Default": "missing",
            "0": "clear sky️",
            "1": "mainly clear️", "2": "partly cloudy", "3": "overcast️",
            "45": "fog", "48": "rime fog",
            "51": "light drizzle️", "53": "moderate drizzle️", "55": "dense drizzle️",
            "56": "light freezing drizzle️", "57": "dense freezing drizzle️",
            "61": "light rain️", "63": "moderate rain️", "65": "heavy rain️",
            "66": "light freezing rain️", "67": "heavy freezing rain️",
            "71": "slight snow fall️", "73": "moderate snow fall️", "75": "heavy snow fall️",
            "77": "snow grains️",
            "80": "slight showers️", "81": "moderate showers️", "82": "heavy showers️",
            "85": "slight snow showers️", "86": "heavy snow showers",
            "95": "thunderstorm", 
            "96": "thunderstorm with slight hail",  "99": "thunderstorm with heavy hail",
        }
        
        wmo_text_de = {
           "Default": "fehlt",
            "0": "klar️",
            "1": "überwiegend klar️", "2": "teilweise bewölkt", "3": "bewölkt️",
            "45": "Nebel", "48": "Reifnebel",
            "51": "leichter Niesel️", "53": "Niesel️", "55": "starker Niesel️",
            "56": "gefrierender Niesel️", "57": "stark gefrierender Niesel️",
            "61": "leichter Regen️", "63": "Regen️", "65": "Starkregen️",
            "66": "gefrierender Regen️", "67": "stark gefrierender Regen️",
            "71": "leicher Schneefall️", "73": "Schneefall️", "75": "starker Schneefall️",
            "77": "Graupel️",
            "80": "leichte Schauer️", "81": "Schauer️", "82": "starke Schauer️",
            "85": "leichte Schneeschauer️", "86": "starke Schneeschauer", 
            "95": "Gewitter", 
            "96": "Gewitter mit leichtem Hagel", "99": "Gewitter mit Hagel",
        }
        
        # select language dictionary
        if self.language == 'en':
            wmo_text = wmo_text_en
        if self.language == 'de':
            wmo_text = wmo_text_de
        
        # return translated weather description    
        if str(wmocode) in wmo_text.keys():
            return wmo_text[ str(wmocode) ]
        else:
            return wmo_text['Default']
