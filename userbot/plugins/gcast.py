# frm Ultroid
# port by Koala @manusiarakitann
# @LordUserbot_Group
# Alvin Ganteng

from userbot.events import register
from userbot import CMD_HELP, bot
# Alvin Ganteng


@register(outgoing=True, pattern="^.gcast (.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`𝐁𝐨𝐬, 𝐭𝐨𝐥𝐨𝐧𝐠 𝐛𝐞𝐫𝐢 𝐚𝐤𝐮 𝐩𝐞𝐬𝐚𝐧!!`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`𝐆𝐥𝐨𝐛𝐚𝐥 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐬𝐞𝐝𝐚𝐧𝐠 𝐛𝐞𝐫𝐥𝐚𝐧𝐠𝐬𝐮𝐧𝐠...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**𝐆𝐜𝐚𝐬𝐭𝐢𝐧𝐠 𝐬𝐮𝐤𝐬𝐞𝐬 𝐝𝐢𝐥𝐮𝐧𝐜𝐮𝐫𝐤𝐚𝐧 𝐤𝐞** `{done}` **𝐠𝐫𝐮𝐩,𝐆𝐚𝐠𝐚𝐥 𝐦𝐞𝐧𝐠𝐢𝐫𝐢𝐦 𝐩𝐞𝐬𝐚𝐧 𝐤𝐞** `{er}` **𝐠𝐫𝐮𝐩**")

# Alvin Ganteng
CMD_HELP.update(
    {
        "gcast": "`.gcast <pesan>`\
    \nPenjelasan: Global Broadcast mengirim pesan ke Seluruh Grup yang Bos Masuki."
    })
