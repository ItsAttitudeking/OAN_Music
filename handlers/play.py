# Copyright ©️ @itsattitudeking

import os
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.callsmusic import callsmusic, queues
from modules.callsmusic.callsmusic import client as USER
from modules.helpers.admins import get_administrators
import requests
import aiohttp
import yt_dlp
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from modules.helpers.channelmusic import get_chat_id
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

# plus
chat_id = None
useer = "NaN"



def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:70]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: @Attitude_Network",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/ytp", "Play", "OAN"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer

    lel = await message.reply("**🔄𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐭𝐨 𝐀𝐭𝐭𝐢𝐭𝐮𝐝𝐞 𝐬𝐞𝐫𝐯𝐞𝐫.........**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "OAN_Music"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
     
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+","https://t.me/joinchat/")
                except:
                    await lel.edit(
                        "<b>ᴘʟᴇᴀꜱᴇ ᴀᴛ ꜰɪʀꜱᴛ ᴍᴀᴋᴇ ᴍᴇ \n ᴀɴ ᴀᴅᴍɪɴ...</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "**ᴀꜱꜱɪꜱᴛᴀɴᴛ ɴᴏᴡ ʀᴇᴀᴅʏ \n ᴛᴏ ᴘʟᴀʏ ᴍᴜꜱɪᴄ...**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>ᴀꜱꜱɪꜱᴛᴀɴᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ \n ᴊᴏɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ..."
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"**ᴀꜱꜱɪꜱᴛᴀɴᴛ ɴᴏᴛ ᴛᴏ ᴊᴏɪɴ \n ᴛʜɪꜱ ᴄʜᴀᴛ...**"
        )
        return

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**ᴘʟᴀʏ ᴍᴜꜱɪᴄ ʟᴇꜱꜱ \n ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🔥🥂𝐒𝐮𝐩𝐩𝐨𝐫𝐭🥂🔥",
                            url=f"https://t.me/oan_support")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🔥🥂𝐒𝐮𝐩𝐩𝐨𝐫𝐭🥂🔥",
                            url=f"https://t.me/oan_support")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/oan_support")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**ᴘʟᴀʏ ᴍᴜꜱɪᴄ ʟᴇꜱꜱ \n ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**ɢɪᴠᴇ ᴍᴜꜱɪᴄ ɴᴀᴍᴇ ᴛᴏ \n ᴘʟᴀʏ...**"
            )
        await lel.edit("😏")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**🔄𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐭𝐨 𝐀𝐭𝐭𝐢𝐭𝐮𝐝𝐞 𝐬𝐞𝐫𝐯𝐞𝐫.........**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**ᴍᴜꜱɪᴄ ɴᴏᴛ ꜰᴏᴜɴᴅ \n ᴛʀʏ ᴀɴᴏᴛʜᴇʀ...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/oan_support")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**ᴘʟᴀʏ ᴍᴜꜱɪᴄ ʟᴇꜱꜱ \n ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ \n ᴀᴅᴅᴇᴅ ꜱᴏɴɢ\n ᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ  » `{}` 🎶 ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
                message.chat.id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            ) 
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ\n ɴᴏᴡ ᴘʟᴀʏɪɴɢ ...**".format(),
        )

    os.remove("final.png")
    return await lel.delete()
    
    
    
@Client.on_message(commandpro(["/pause", "Pause", "Rukja"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg", 
                             caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ\n ɴᴏᴡ ▶️ ᴘᴀᴜꜱᴇᴅ ...**"
    )


@Client.on_message(commandpro(["/resume", "Resume", "Chalukar"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg", 
                             caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ\n ɴᴏᴡ ⏸ ᴘʟᴀʏɪɴɢ ...**"
    )



@Client.on_message(commandpro(["/skip", "/next", "Skip", "Next", "Changekar"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ \n ɴᴏᴛʜɪɴɢ ᴘʟᴀʏɪɴɢ ...**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
            
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                    InputStream(
                        InputAudioStream(
                            callsmusic.queues.get(chat_id)["file"],
                        ),
                    ),
                )

    await message.reply_photo(
                             photo="https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg", 
                             caption=f'**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ \n ɴᴏᴡ ⏩ꜱᴋɪᴘᴘᴇᴅ ...**'
   ) 


@Client.on_message(commandpro(["/end", "End", "/stop", "Stop", " Bandkar"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg", 
                             caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ\n ɴᴏᴡ ❌ ꜱᴛᴏᴘᴘᴇᴅ ...**"
    )


@Client.on_message(commandpro(["reload", "refresh", "Thikkar"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_photo(
                              photo="https://telegra.ph/file/6e2ab05382cf91185b4fe.jpg",
                              caption="**⚡𝗢𝗔𝗡 𝗠𝘂𝘀𝗶𝗰⚡ ᴍᴜꜱɪᴄ\n ɴᴏᴡ ʀᴇᴀʟᴏᴀᴅᴇᴅ ...**"
    )
