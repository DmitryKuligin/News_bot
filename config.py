import telebot
from telebot import types

from datetime import datetime
from random import randint

import requests
import json
from time import sleep
from DataBase import *


#Bot Token
TOKEN = '5021646895:AAF3VO-BH2jfxnRW03k8b5QzoHbWek1epWo'


#New's Api Token
API_TOKEN = 'b30e14ab7ce3432baa253a37bca69098'


#New's Sphere list
SPHERES = ['Apple', 'Tesla', 'Top Business Headlines US', 'Top Business Headlines TC', 'WallStreet News'] 
