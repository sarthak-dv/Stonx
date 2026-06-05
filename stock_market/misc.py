from dotenv import load_dotenv
import os, requests, json

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
api_request = requests.get(f"http://newsapi.org/v2/everything?q=stocks&apiKey={NEWS_API_KEY}")
api = json.loads(api_request.content)
print(api['articles'])