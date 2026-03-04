"""
weather_collector_v2.py - With DynamoDB support
Stores weather data in both S3 cache and DynamoDB history
"""

import json
import os
import logging
from datetime import datetime, timezone
from decimal import Decimal
import time
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

class WeatherCollector:
    def __init__(self):
        self.api_key = os.environ['OPENWEATHER_API_KEY']
        self.bucket = os.environ['S3_BUCKET_NAME']
        self.table_name = os.environ['DYNAMODB_TABLE']
        self.table = dynamodb.Table(self.table_name)
        
        cities_str = os.environ['CITIES']
        self.cities = [city.strip() for city in cities_str.split(',')]
        
        logger.info(f"Initialized for {len(self.cities)} cities")
        logger.info(f"DynamoDB table: {self.table_name}")
    
    def kelvin_to_celsius(self, kelvin):
        return round(kelvin - 273.15, 1)
    
    def fetch_weather(self, city, max_retries=3):
        """Fetch weather with retry logic"""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key}
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Fetching {city} (attempt {attempt}/{max_retries})")
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                weather_data = {
                    "city": data.get("name", city),
                    "country": data.get("sys", {}).get("country"),
                    "timestamp": int(time.time()),
                    "timestamp_iso": datetime.now(timezone.utc).isoformat(),
                    "temperature": {
                        "celsius": self.kelvin_to_celsius(data["main"]["temp"]),
                        "feels_like": self.kelvin_to_celsius(data["main"]["feels_like"]),
                        "min": self.kelvin_to_celsius(data["main"]["temp_min"]),
                        "max": self.kelvin_to_celsius(data["main"]["temp_max"])
                    },
                    "weather": {
                        "main": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"]
                    },
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data.get("wind", {}).get("speed", 0),
                    "clouds": data.get("clouds", {}).get("all", 0),
                    "visibility": data.get("visibility", 0)
                }
                
                logger.info(f"✅ {city}: {weather_data['temperature']['celsius']}°C")
                return weather_data
                
            except Exception as e:
                logger.error(f"❌ Error fetching {city}: {e}")
                if attempt < max_retries:
                    time.sleep(2 ** (attempt - 1))
                    
        return None
    
    def save_to_s3(self, city, weather_data):
        """Save to S3 cache"""
        try:
            city_key = city.lower().replace(' ', '_')
            s3_key = f"cache/{city_key}.json"
            
            s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=json.dumps(weather_data, indent=2),
                ContentType="application/json"
            )
            
            logger.info(f"✅ S3: {s3_key}")
            return True
        except Exception as e:
            logger.error(f"❌ S3 failed for {city}: {e}")
            return False
    
    def save_to_dynamodb(self, city, weather_data):
        """Save to DynamoDB history"""
        try:
            # Convert floats to Decimal for DynamoDB
            item = {
                'city': city,
                'timestamp': weather_data['timestamp'],
                'timestamp_iso': weather_data['timestamp_iso'],
                'temperature': Decimal(str(weather_data['temperature']['celsius'])),
                'feels_like': Decimal(str(weather_data['temperature']['feels_like'])),
                'humidity': weather_data['humidity'],
                'pressure': weather_data['pressure'],
                'weather_main': weather_data['weather']['main'],
                'weather_description': weather_data['weather']['description'],
                'wind_speed': Decimal(str(weather_data['wind_speed'])),
                'clouds': weather_data['clouds'],
                'ttl': weather_data['timestamp'] + (90 * 24 * 3600)  # 90 days TTL
            }
            
            self.table.put_item(Item=item)
            logger.info(f"✅ DynamoDB: {city}")
            return True
            
        except Exception as e:
            logger.error(f"❌ DynamoDB failed for {city}: {e}")
            return False
    
    def collect_all(self):
        """Collect weather for all cities"""
        results = {
            "total": len(self.cities),
            "s3_success": 0,
            "dynamodb_success": 0,
            "failed": 0,
            "cities": []
        }
        
        for city in self.cities:
            weather_data = self.fetch_weather(city)
            
            if weather_data:
                s3_ok = self.save_to_s3(city, weather_data)
                db_ok = self.save_to_dynamodb(city, weather_data)
                
                if s3_ok:
                    results["s3_success"] += 1
                if db_ok:
                    results["dynamodb_success"] += 1
                    
                results["cities"].append({
                    "city": city,
                    "s3": s3_ok,
                    "dynamodb": db_ok,
                    "temp": weather_data['temperature']['celsius']
                })
            else:
                results["failed"] += 1
                results["cities"].append({"city": city, "status": "failed"})
            
            time.sleep(1)
        
        return results

def handler(event, context):
    """Lambda handler"""
    logger.info("=" * 70)
    logger.info("WEATHER COLLECTOR V2 - WITH DYNAMODB")
    logger.info("=" * 70)
    
    try:
        collector = WeatherCollector()
        results = collector.collect_all()
        
        logger.info("=" * 70)
        logger.info("RESULTS:")
        logger.info(f"S3: {results['s3_success']}/{results['total']}")
        logger.info(f"DynamoDB: {results['dynamodb_success']}/{results['total']}")
        logger.info(f"Failed: {results['failed']}/{results['total']}")
        logger.info("=" * 70)
        
        return {
            "statusCode": 200,
            "body": json.dumps(results)
        }
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
