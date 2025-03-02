import configparser
import os



config_file = 'config.ini'

config = configparser.ConfigParser()

config.read(config_file)

print(f"Sections found: {config.sections()}")