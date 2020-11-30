import json
import requests
import configparser
import datetime
from datetime import timezone

config = configparser.ConfigParser()
translation = configparser.ConfigParser()
config.read('config.ini')
defaultConf = config['Default']
unitsConf = config[defaultConf['units']]
translation.read(defaultConf['language']+'.lang')
wCond = translation['condition codes']
tDef = translation['Default']

payload = {'id':defaultConf['cityId'],'appid':defaultConf['apiKey'],'units':defaultConf['units']}

response = requests.get('https://api.openweathermap.org/data/2.5/weather',payload)

weatherJson = response.json()
weatherId = weatherJson['weather'][0]['id']

def calculateWindDirection(dir_deg):
    if dir_deg < 15:
        return "N"
    elif dir_deg < 35:
        return "N/NE"
    elif dir_deg < 55:
        return "NE"
    elif dir_deg < 75:
        return "E/NE"
    elif dir_deg < 105:
        return "E"
    elif dir_deg < 125:
        return "E/SE"
    elif dir_deg < 145:
        return "SE"
    elif dir_deg < 165:
        return "S/SE"
    elif dir_deg < 165:
        return "S/SE"
    elif dir_deg < 195:
        return "S"
    elif dir_deg < 215:
        return "S/SW"
    elif dir_deg < 235:
        return "SW"
    elif dir_deg < 255:
        return "W/SW"
    elif dir_deg < 285:
        return "W"
    elif dir_deg < 305:
        return "W/NW"
    elif dir_deg < 325:
        return "NW"
    elif dir_deg < 345:
        return "N/NW"
    else:
        return "N"


def getWindSpeedUnitConvert():
    speed = weatherJson['wind']['speed']
    if defaultConf['units'] == 'metric':
        return round(speed*3.6,1)
    else:
        return round(speed,1)


def getVisibilityDistance():
    visibility = weatherJson['visibility']
    if defaultConf['units'] == 'metric':
        if visibility < 1000:
            return (str(visibility) + ' ' + unitsConf['vUnit'])
        else:
            return (str(round(visibility/1000,1)) + ' ' + unitsConf['vSupUnit'])
    elif defaultConf['units'] == 'imperial':
        if visibility < 1609:
            return (str(round(visibility*3.2808399)) + ' ' + unitsConf['vUnit'])
        else:
            return (str(round(visibility/1609,1)) + ' ' + unitsConf['vSupUnit'])
    elif defaultConf['units'] == 'standard':
        return (str(visibility) + ' ' + unitsConf['vUnit'])


def getUpdateTime():
    tsUpdate = weatherJson['dt']
    tUpdateUTC = datetime.datetime.fromtimestamp(tsUpdate,tz=timezone.utc)
    d=tUpdateUTC.replace(tzinfo=datetime.timezone.utc)
    d=d.astimezone()
    return d.strftime("%d/%m/%Y %H:%M")


def getCityName():
    return weatherJson['name'] + '\n'


def getCurrentCondition():
    return wCond[str(weatherId)] + '\n'


def getCurrentTempForImg():
    return tDef['temperature'] + ': ' +  str(round(weatherJson['main']['temp']))


def getCurrentTemp():
    return tDef['temperature'] + ': ' +  str(round(weatherJson['main']['temp'])) + ' ' + unitsConf['tUnit'] + '\n'


def getFeelsLikeForImg():
    return tDef['feels'] + ': ' +  str(round(weatherJson['main']['feels_like']))


def getFeelsLike():
    return tDef['feels'] + ': ' +  str(round(weatherJson['main']['feels_like'])) + ' ' + unitsConf['tUnit'] + '\n'


def getWindSpeed():
    return tDef['wind'] + ': ' + str(getWindSpeedUnitConvert()) + " " + unitsConf['wUnit'] + '\n'

def getWindDirValue():
    return calculateWindDirection(weatherJson['wind']['deg'])

def getWindDirection():
    return tDef['direction'] + ': ' + calculateWindDirection(weatherJson['wind']['deg']) + '\n'


def getPressure():
    return tDef['pressure'] + ': ' + str(weatherJson['main']['pressure']) + ' hPa\n'


def getHumidity():
    return tDef['humidity'] + ': ' + str(weatherJson['main']['humidity']) + '%\n'



def getVisibility():
    return tDef['visibility'] + ': ' + getVisibilityDistance() + '\n'


def getLastUpdate():
    return tDef['update'] + ': ' + getUpdateTime()

def getIconName():
    return weatherJson['weather'][0]['icon']