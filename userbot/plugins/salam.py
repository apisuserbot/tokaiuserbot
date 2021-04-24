from time import sleep
from platform import uname
from userbot import CMD_HELP
from userbot.plugins import ALIVE_NAME
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern='^kntl(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐋𝐔 𝐊𝐎𝐍𝐓𝐎𝐋!!!**")
    sleep(3)
    await typew.edit("`𝐊𝐎𝐍𝐓𝐎𝐋 𝐊𝐎𝐍𝐓𝐎𝐋 𝐊𝐎𝐍𝐓𝐎𝐋!!!`")
    sleep(3)
    await typew.edit("`𝐃𝐀𝐒𝐀𝐑 𝐊𝐄𝐏𝐀𝐋𝐀 𝐊𝐎𝐍𝐓𝐎𝐋!!!`")


@register(outgoing=True, pattern='^G(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐄𝐦𝐦... 𝐛𝐞𝐧𝐭𝐚𝐫 𝐠𝐮𝐚 𝐩𝐢𝐤𝐢𝐫 𝐝𝐮𝐥𝐮...**")
    sleep(3)
    await typew.edit("`𝐆𝐚 𝐝𝐮𝐥𝐮 𝐝𝐞𝐡.`")


@register(outgoing=True, pattern='^P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐇𝐚𝐥𝐨𝐨𝐨, 𝐤𝐞𝐧𝐚𝐥𝐢𝐧 𝐠𝐮𝐚 {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("`𝐒𝐚𝐥𝐚𝐦 𝐊𝐞𝐧𝐚𝐥.....`")


@register(outgoing=True, pattern='^L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`𝐉𝐚𝐰𝐚𝐛 𝐬𝐚𝐥𝐚𝐦 𝐝𝐮𝐥𝐮 𝐚𝐡𝐡...`")
    sleep(1)
    await typew.edit("`𝐖𝐚𝐚𝐥𝐚𝐢𝐤𝐮𝐦𝐬𝐚𝐥𝐚𝐦......`")


CMD_HELP.update({
    "salam":
    "`P`\
\nUsage: Untuk Memberi Hujatan.\
\n\n`L`\
\nUsage: Untuk Menjawab Salam."
})
