"""
✘ Commands Available -
• `{i}tempmail`
   Generates Temporary Mail
"""

from . import *
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio


@bot.on(admin_cmd(outgoing=True, pattern="tempmail$"))
async def demn(ult):
    chat = "@TempMailBot"
    msg = await eor(ult, f"Membuat Temporary Email...")
    async with ultroid_bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True,
                from_users=220112646
            )
            )
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("Generate New")
            response = await response
            link = ((response).reply_markup.rows[2].buttons[0].url)
            await ultroid_bot.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Boss! Tolong Unblock @TempMailBot ")
            return
        await eor(ult, f"TEMPMAIL ~ `{response.message.message}`\n\n[CLICK UNTUK BUKA INBOX]({link})")



HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
