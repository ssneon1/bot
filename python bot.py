import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

# ✅ Load environment variables
load_dotenv()
token = os.environ['discordkey']

# ✅ Set up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# ✅ Banned word list
banned_words = [
    "fuck","bitch", "asshole", "dick", "slut", "nigga", "madarchod", "bhosdike", "chutiya",
    "lund", "beti chod", "gaand", "randi", "bhenchod", "bhench*d", "mc", "bc", "chootiya",
    "kutte", "gandu", "lode", "lauda", "maa ka bhosda", "teri maa", "teri behen", "chodu",
    "randwa", "bol teri gand kaise maru", "gandmara", "chdmarike", "choot chatora",
    "gel chodi gand andhi rand", "lavde", "madar chod", "gand maar lunga", "tere baap ki chut hai",
    "tere maa market me nanga nach kr rahi hai", "kutta kamine bsdk chutiya", "teri maa randwi hai",
    "lund ke tope", "chut ke kitde", "chinal ki aulad", "chutmari ka choda", "teri chut", "bhg bsdk",
    "bhen ka lavda", "chut chatora", "jhaat bara bar", "me toh chut ka shikari hu", "bhosda", "chutad",
# English
    "bastard", "moron", "jerk", "retard", "dumbass", "shithead", "fucker", "mf", "stfu", "wtf", "fuckoff",

    # Hindi + Hinglish
    "chod", "behen ke lode", "behnchod", "madarchod", "chodna", "gaand mara", "randy", "kutti", "kamine", "bhadwe",
    "madharchod", "bahanchod", "chutia", "gand", "randi ke bacche", "chinal", "laundiya", "gand fat", "kutta kamina",

    # Short forms & WhatsApp slangs
    "mc", "bc", "bkl", "bsdk", "lodu", "loda", "gandu", "gand", "gaandu", "chomu", "chu", "chuu", "mch", "rndi", "chodu", "lund", "choot", "chod", "randi", "bhosdi",

    # Phonetic obfuscations
    "b3hnchod", "mad@rch0d", "m@darchod", "g@nd", "g@ndu", "fuk", "fuq", "fking", "fk u", "b!tch", "bit*h", "b!t*h",

    # Split word forms
    "ma chudaye", "be hnchod", "b h o s d i k e", "ch ut", "g andu", "ch od", "g and", "m ch", "mad@rchod"
]

# ✅ Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# ✅ Bot Setup
bot = commands.Bot(command_prefix='!', intents=intents)

# ✅ Allowed Server ID
ALLOWED_GUILD_ID = 752891683888431124  # Replace with your server ID

# 🧠 For Mod Mail replies
modmail_user_map = {}

# ✅ Friendly trigger-response pairs
friendly_triggers = {
    ("hello", "hi", "hey", "yo", "oye"): [
        "Hey {mention}, kya haal hai? 😊",
        "Hello hello {mention}, kaise ho? 🤗",
        "Heyyy! {mention}, kya chal raha hai? 👋",
        "Namaste {mention}, swagat hai! 🙏"
    ],
    ("or", "or kya", "or batao", "or bhai"): [
        "Or kya scene hai {mention}? 🤔",
        "Batao bhai, sab thik? 😄",
        "Or bhai {mention}, kya chal raha hai? 😎",
        "Aaj ka kya plan hai {mention}? 🎮"
    ],
    ("how are you", "kaisa hai", "kya haal hai"): [
        "Main mast hoon! Tu suna {mention}? 😁",
        "Main theek, tu bata {mention}! 😇",
        "Zinda hoon bas 😎, tu kaisa hai {mention}?"
    ],
    ("who made you", "creator", "banaya kisne"): [
        "Mujhe banaya Neon ne! 😎",
        "Neon is my boss! 💻",
        "I'm powered by Neon 🔥"
    ],
    ("koi hai", "anyone here", "kaun hai"): [
        "Main hoon yaha, aapka bot {mention} 😄",
        "Bolo kya chahiye? 😁",
        "Haan haan, sab sun raha hoon! 👂"
    ],
    ("aaj stream karega", "aaj steam karoga"): [
        "Shayad, dekhte hain 😁",
        "Iska jawab to sirf Neon de sakta hai! 🎥",
        "Mausam thik hua to stream on hogi 😄"
    ],
    ("bye", "good night", "gn", "see you"): [
        "Good night {mention}, sweet dreams! 🌙",
        "Bye bye {mention}, milte hain phir! 👋",
        "Chalo fir {mention}, kal milte hain! 😴"
    ],
    ("thanks", "thank you", "ty", "shukriya"): [
        "You’re welcome {mention}! 😊",
        "Koi baat nahi {mention}, anytime! 🙏",
        "Bas yahi to kaam hai mera 😄"
    ],
    ("love you", "i love you bot", "ily bot"): [
        "Love you too {mention} ❤️",
        "Aww 🥺, you’re the best {mention}!",
        "Dil jeet liya tumne {mention} 😍"
    ]
}

@bot.event
async def on_ready():
    print(f"✅ Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        await member.send(f'Welcome to the server, {member.name}!')
    except discord.Forbidden:
        print(f"⚠️ Could not DM {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ✅ Ignore messages from other servers
    if message.guild and message.guild.id != ALLOWED_GUILD_ID:
        return

    msg_content = message.content.lower()

    # ✅ Check for banned words
    if any(word in msg_content for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please avoid using bad words.")
        return

    # ✅ Handle DM to bot (modmail)
    if isinstance(message.channel, discord.DMChannel):
        guild = discord.utils.get(bot.guilds, id=ALLOWED_GUILD_ID)
        mod_channel = discord.utils.get(guild.text_channels, name="mod-mail")

        if mod_channel:
            embed = discord.Embed(title="📬 New Mod Mail", description=message.content, color=discord.Color.blue())
            embed.set_author(name=f"{message.author} ({message.author.id})", icon_url=message.author.display_avatar.url)
            msg = await mod_channel.send(embed=embed)
            modmail_user_map[msg.id] = message.author.id
            await message.channel.send("✅ Your message has been sent to the moderators!")
        else:
            await message.channel.send("❌ Could not find a mod-mail channel.")
        return

    # ✅ Only respond to triggers if bot is mentioned or in DM or it's a command
    should_reply = (
        bot.user in message.mentions or
        isinstance(message.channel, discord.DMChannel) or
        message.content.startswith('!')
    )

    if should_reply:
        for trigger_group, responses in friendly_triggers.items():
            if any(trigger in msg_content for trigger in trigger_group):
                response = random.choice(responses).format(mention=message.author.mention)
                await message.channel.send(response)
                return

    await bot.process_commands(message)

# 📨 Modmail reply command
@bot.command(name="reply")
@commands.has_permissions(manage_messages=True)
async def reply(ctx, message_id: int, *, response: str):
    user_id = modmail_user_map.get(message_id)
    if not user_id:
        await ctx.send("❌ That message ID wasn't found in active modmail.")
        return

    try:
        user = await bot.fetch_user(user_id)
        await user.send(f"📩 Moderator reply:\n{response}")
        await ctx.send(f"✅ Replied to {user.name}")
    except discord.Forbidden:
        await ctx.send("❌ Cannot DM this user.")

# 📜 Command to show all trigger phrases
@bot.command(name="triggers")
async def show_triggers(ctx):
    response = "**Here are the phrases I respond to (only if you tag me or DM me):**\n"
    for group in friendly_triggers:
        response += "• " + ", ".join(group) + "\n"
    await ctx.send(response)

# ▶️ Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
