# import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests


WEATHER_KEY = os.getenv('OPENWEATHERMAP_KEY')


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def weather(self, ctx, *, location):
        ''' Get weather information '''
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + location + "&appid=" + WEATHER_KEY
        response = requests.get(URL)
        data = response.json()
        if data["cod"] != "404":
            main_data = data["main"]
            temperature_avg = main_data["temp"] - 273.15
            temperature_min = main_data["temp_min"] - 273.15
            temperature_max = main_data["temp_max"] - 273.15
            pressure = main_data["pressure"]
            humidity = main_data["humidity"]
            visibility = data["visibility"] / 1000
            weather_data = data["weather"]
            weather_description = weather_data[0]["description"]
            weather_report = (
                f"Location: {location}\n"
                f"Temperature: {temperature_avg:.2f}°C ({temperature_min:.2f} - {temperature_max:.2f}°C)\n"
                f"Pressure: {pressure} hPa\n"
                f"Humidity: {humidity}%\n"
                f"Visibility: {visibility} km\n"
                f"Description: {weather_description}\n"
            )
            await ctx.send(weather_report)
        else:
            await ctx.send(f"Could not find weather information for {location}")


async def setup(bot):
    await bot.add_cog(Weather(bot))
