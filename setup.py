from setuptools import setup

setup (
  name="WeatherProcessor",
  version="1.0",
  description="Weather Application with GUI to generate graphs",
  author="Harsh Patel, Robert Kaufman",
  py_modules=["db_operations", "plot_operations", "scrape_weather.py", "weather_processor"]
)