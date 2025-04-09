import discord
import requests
from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from datetime import datetime

load_dotenv()
UID = os.getenv('UID_KEY')
SECRET = os.getenv('SECRET_KEY')
LOGIN = os.getenv('LOGIN')
SEND_ID = os.getenv('SEND_ID')
TOKEN=os.getenv('TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

discord_client = discord.Client(intents=intents)
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
    token_url='https://api.intra.42.fr/oauth/token',
    client_id=UID,
    client_secret=SECRET
)

access_token = token['access_token']
headers = {
    'Authorization': f'Bearer {access_token}'
}

params = {
    "per_page": 100,
    "page": 1
}

url = f'https://api.intra.42.fr/v2/users/{LOGIN}'
response = requests.get(url, headers=headers).json()
blackhole_date = datetime.strptime(response['cursus_users'][1]['blackholed_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
now = datetime.now()
remaining = blackhole_date - now
message = f'BHまで残り{remaining}'

@discord_client.event
async def on_ready():
    print(f'ログイン成功: {discord_client.user}')

    try:
        user = await discord_client.fetch_user(SEND_ID)
        await user.send(message)
        print(message)
        print("DM送信成功！")
    except discord.Forbidden:
        print("⚠️ DM送信に失敗しました（相手がDM拒否？）")
    except Exception as e:
        print(f"エラー発生: {e}")

    await discord_client.close()
discord_client.run(TOKEN)
