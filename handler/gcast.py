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
        wtf = await message.reply("🛎️𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭...")
        if not message.reply_to_message:
            await wtf.edit("**❌𝐄𝐫𝐫𝐨𝐫\n\n📍𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭...**")
            return
        lmao = message.reply_to_message.text
        async for dialog in aditya.iter_dialogs():
            try:
                await aditya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"🔴𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭𝐢𝐧𝐠..... \n\n**🔴𝐒𝐞𝐧𝐭 𝐭𝐨 :** `{sent}` 𝐜𝐡𝐚𝐭𝐬 \n**🔴𝐅𝐚𝐢𝐥𝐞𝐝 𝐢𝐧:** {failed} 𝐜𝐡𝐚𝐭𝐬")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"🔴𝐆𝐜𝐚𝐬𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲📍\n\n**🔴𝐒𝐞𝐧𝐭 𝐭𝐨 :** `{sent}` 𝐜𝐡𝐚𝐭𝐬 \n**🔴𝐅𝐚𝐢𝐥𝐞𝐝 𝐢𝐧:** {failed} 𝐜𝐡𝐚𝐭𝐬")
