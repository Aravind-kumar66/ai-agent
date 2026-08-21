import requests


def get_weather(latitude: float, longitude: float) -> str:
    """
    Get current weather for a latitude and longitude
    using Open-Meteo.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "auto",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        description = weather_code_to_description(weather_code)

        return (
            f"Temperature: {temperature}°C\n"
            f"Condition: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Wind speed: {wind_speed} km/h"
        )

    except requests.RequestException as e:
        return f"Weather API error: {e}"

    except (KeyError, TypeError, ValueError) as e:
        return f"Weather data error: {e}"


def weather_code_to_description(code: int) -> str:
    """
    Convert Open-Meteo weather codes into readable descriptions.
    """

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_codes.get(
        code,
        "Unknown weather condition"
    )
