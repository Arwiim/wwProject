from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import requests
import math

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_verified)


generate_token = TokenGenerator()


def temperature():
    
    str = requests.get("http://api.openweathermap.org/data/2.5/weather?q=cordoba&appid=0d7b64c422033b206d4dcd4641394197")
    data_temp = str.json()
    
    temp = math.trunc(data_temp['main']['temp'] - 273.25)
    min = math.trunc(data_temp['main']['temp_min'] - 273.25)
    max = math.trunc(data_temp['main']['temp_max'] - 273.25)
    
    return {"temp": temp,
            "min": min,
            "max": max}