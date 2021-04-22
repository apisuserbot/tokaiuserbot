from platform import uname
from userbot import ALIVE_NAME, CMD_HELP, CMD_LIST
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern='^kntl(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐋𝐔 𝐊𝐎𝐍𝐓𝐎𝐋**")
    sleep(3)
    await typew.edit("`𝐊𝐎𝐍𝐓𝐎𝐋 𝐊𝐎𝐍𝐓𝐎𝐋 𝐊𝐎𝐍𝐓𝐎𝐋!!!`")
    sleep(3)
    await typew.edit("`𝐃𝐀𝐒𝐀𝐑 𝐊𝐄𝐏𝐀𝐋𝐀 𝐊𝐎𝐍𝐓𝐎𝐋!!!`")


@register(outgoing=True, pattern='^G(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐉𝐀𝐊𝐀 𝐒𝐄𝐌𝐁𝐔𝐍𝐆 𝐁𝐀𝐖𝐀 𝐆𝐎𝐋𝐎𝐊**")
    sleep(3)
    await typew.edit("`𝐍𝐈𝐌𝐁𝐑𝐔𝐍𝐆 𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊!!!`")


@register(outgoing=True, pattern='^.g(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐉𝐀𝐊𝐀 𝐒𝐄𝐌𝐁𝐔𝐍𝐆 𝐁𝐀𝐖𝐀 𝐆𝐎𝐋𝐎𝐊**")
    sleep(3)
    await typew.edit("`𝐍𝐈𝐌𝐁𝐑𝐔𝐍𝐆 𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊!!!`")


@register(outgoing=True, pattern='^P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐇𝐚𝐥𝐨𝐨𝐨, 𝐤𝐞𝐧𝐚𝐥𝐢𝐧 𝐠𝐮𝐚 {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("`𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋.....`")


@register(outgoing=True, pattern='^p(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝐇𝐚𝐥𝐨𝐨𝐨, 𝐤𝐞𝐧𝐚𝐥𝐢𝐧 𝐠𝐮𝐚 {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("`𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋.....`")


@register(outgoing=True, pattern='^L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`𝐀𝐬𝐭𝐚𝐠𝐟𝐢𝐫𝐮𝐥𝐨𝐡 𝐤𝐚𝐦𝐮 𝐢𝐧𝐢 𝐛𝐞𝐫𝐝𝐨𝐬𝐚 𝐬𝐞𝐤𝐚𝐥𝐢...`")
    sleep(1)
    await typew.edit("`𝐖𝐚𝐚𝐥𝐚𝐢𝐤𝐮𝐦𝐬𝐚𝐥𝐚𝐦 𝐬𝐚𝐲𝐚𝐧𝐠......`")


@register(outgoing=True, pattern='^l(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`𝐀𝐬𝐭𝐚𝐠𝐟𝐢𝐫𝐮𝐥𝐨𝐡 𝐤𝐚𝐦𝐮 𝐢𝐧𝐢 𝐛𝐞𝐫𝐝𝐨𝐬𝐚 𝐬𝐞𝐤𝐚𝐥𝐢...`")
    sleep(1)
    await typew.edit("`𝐖𝐚𝐚𝐥𝐚𝐢𝐤𝐮𝐦𝐬𝐚𝐥𝐚𝐦 𝐬𝐚𝐲𝐚𝐧𝐠.....`")


CMD_HELP.update({
    "salam":
    "`P`\
\nUsage: Untuk Memberi Hujatan.\
\n\n`L`\
\nUsage: Untuk Menjawab Salam."
})
