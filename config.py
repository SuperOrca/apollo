import discord


VIEW_TIMEOUT = 180

TOKEN = ""
DAGPI = ""
PREFIX = ''
OWNER_IDS = ()
COLOR = 

DESCRIPTION = """
An open-source general-use discord.py bot.
"""

NEWS_TITLE = ""
NEWS_VALUE = """
"""

INTENTS = discord.Intents(
	guilds=True,
	members=True,
	bans=True,
	emojis=True,
	voice_states=True,
	messages=True,
	reactions=True
)

MENTIONS = discord.AllowedMentions.none()

STRIP_AFTER_PREFIX = True
CASE_INSENSITIVE = True
MAX_MESSAGES = 10000

EIGHT_BALL = (
	"It is certain",
	"It is decidedly so",
	"Without a doubt",
	"Yes, definitely",
	"You may rely on it",
	"As I see it, yes",
	"Most likely",
	"Outlook good",
	"Yes",
	"Signs point to yes",
	"Reply hazy try again",
	"Ask again later",
	"Better not tell you now",
	"Cannot predict now",
	"Concentrate and ask again",
	"Don't count on it",
	"My reply is no",
	"My sources say no",
	"Outlook not so good",
	"Very doubtful"
)
