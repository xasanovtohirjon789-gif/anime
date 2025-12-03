import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN', 'YOUR_BOT_TOKEN_HERE')

ADMIN_ID = int(os.getenv('ADMIN_ID', '5763542336'))

ADMIN_IDS = [5763542336]

MANDATORY_CHANNELS = [
    {
        'channel_id': -1002179331541,
        'link': 'https://t.me/+yWlBa7lZF9tlN2M6',
        'name': 'ANITOX CHANEL'
    }
]

DATABASE_PATH = 'anime_bot.db'

MAX_MESSAGE_LENGTH = 4096

PARTS_PER_PAGE = 10

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
