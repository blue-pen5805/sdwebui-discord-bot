import re
from discord import Intents
from discord.ext import commands

from modules.command import summon
import modules.env as env
from modules.webui import loras

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='魔法陣',
    intents=intents,
)

SPELLS = [
    '出でよ', 'いでよ', 'ででよ', '出ろ',
    '来い', 'こい', 'きて', 'きなさい',
    'おいでなさい', 'おいでよ', 'おいで',
    '生まれろ', 'うまれろ', '生み出せ',
    '生成', '召喚', 'summon',
    '顕現せよ',
]
SPELL_SUFFIX = [
    '!', '！', 'っ！', '～', 'ー'
]
SPELL_PATTERN = re.compile(f"^({'|'.join(SPELLS)})({'|'.join(SPELL_SUFFIX)})?")

def check_spell(text):
    return SPELL_PATTERN.match(text)

def prompt_from_spell(text):
    return SPELL_PATTERN.sub('', text).strip()

CHANNEL_IDS = [
    1076729588832542743, # なんでもいいよ
    1106890735745237002, # テスト用
    1093901037791871026, # 確認用
]

@bot.event
async def on_message(message):
    if message.channel.id not in CHANNEL_IDS:
        return

    if message.content == '教えて呪文':
        pattern = ' '.join([x + y for x in SPELLS for y in SPELL_SUFFIX])
        return await message.reply(f"以下の詠唱が使えます\n`{pattern}`", silent=True)

    if message.content == '教えてLoRA':
        lora_names = await loras()
        codes = list(map(lambda x: f"`{x}`", lora_names))
        return await message.reply(f"使えるLoRAはこちら！\n{' '.join(codes)}", silent=True)

    if check_spell(message.content):
        return await summon(message, prompt_from_spell(message.content))

DISCORD_TOKEN= env.get("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)
