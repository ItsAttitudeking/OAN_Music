# Copyright (C) 2021 By @itsattitudeking

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from modules.callsmusic.callsmusic import client as aditya
from modules.config import SUDO_USERS

@Client.on_message(filters.command(["gcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("šļøšš­šš«š­š¢š§š  šš«šØššššš¬š­...")
        if not message.reply_to_message:
            await wtf.edit("**āšš«š«šØš«\n\nššš„ššš¬š š«šš©š„š² š­šØ š š¦šš¬š¬šš š š­šØ š¬š­šš«š­ šš«šØššššš¬š­...**")
            return
        lmao = message.reply_to_message.text
        async for dialog in aditya.iter_dialogs():
            try:
                await aditya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"š“šš«šØššššš¬š­š¢š§š ..... \n\n**š“ššš§š­ š­šØ :** `{sent}` šš”šš­š¬ \n**š“ššš¢š„šš š¢š§:** {failed} šš”šš­š¬")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"š“šššš¬š­ šš®šššš¬š¬šš®š„š„š²š\n\n**š“ššš§š­ š­šØ :** `{sent}` šš”šš­š¬ \n**š“ššš¢š„šš š¢š§:** {failed} šš”šš­š¬")
