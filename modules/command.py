import gc
import datetime
import uuid
import piexif
import piexif.helper
import discord

from modules.translator import translate
from modules.webui import generate

TIMESPAN = datetime.timedelta(minutes=3)

rentou_seigen = {}
queue = []

async def summon(message, raw_prompt):
    global queue
    global rentou_seigen

    if len(queue) > 1:
        await message.reply("今忙しいから後にして！", silent=True)
        return

    now = datetime.datetime.now()

    previous_datetime = rentou_seigen.get(message.author.id)
    if previous_datetime:
        if now - previous_datetime <= TIMESPAN:
            rentou_seigen[message.author.id] = previous_datetime + datetime.timedelta(minutes=2)
            next_datetime = previous_datetime + datetime.timedelta(minutes=3) + TIMESPAN
            await message.reply(f"{next_datetime.strftime('%H時%M分%S秒')}まで我慢しなさい。", silent=True)
            return

    queue.append(message.id)
    rentou_seigen[message.author.id] = now

    print(raw_prompt)
    translated = translate(raw_prompt)
    print(translated)

    if translated:
        single_line = translated.replace('\n', ' ')
        title = f"**{raw_prompt}** `{single_line}`"
    else:
        title = f"**{raw_prompt}**"

    reply = await message.reply(f"{title} 召喚開始…", silent=True)

    try:
        images, pnginfos = generate(translated or raw_prompt)

        filenames = []
        for i, image in enumerate(images):
            filename = f"outputs/{now.strftime('%y%m%d_%H%M%S')}-{uuid.uuid1()}.webp"
            image.save(filename, quality=85)
            exif_bytes = piexif.dump({
                "Exif": {
                    piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(pnginfos[i] or "", encoding="unicode")
                },
            })
            piexif.insert(exif_bytes, filename)

            filenames.append(filename)

        await reply.edit(
            content=f"{title} 召喚！",
            attachments=list(map(lambda x: discord.File(x), filenames))
        )
    except Exception as e:
        print(e)
        await reply.edit(content=f"{title} はなんか失敗しました")

    try:
        queue.remove(message.id)
    except ValueError:
        pass

    gc.collect()
