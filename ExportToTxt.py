import PyWeather
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
defaultConf = config['Default']
fileLocation = defaultConf['file_path']+defaultConf['file_name']
f = open(fileLocation,'w+')
f.write(PyWeather.getCityName())
f.write(PyWeather.getCurrentCondition())
f.write(PyWeather.getCurrentTemp())
f.write(PyWeather.getFeelsLike())
f.write(PyWeather.getWindSpeed())
f.write(PyWeather.getWindDirection())
f.write(PyWeather.getPressure())
f.write(PyWeather.getHumidity())
f.write(PyWeather.getVisibility())
f.write(PyWeather.getLastUpdate())
f.close()