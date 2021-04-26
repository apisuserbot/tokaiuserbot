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
    await typew.edit(f"**𝗟𝘂 𝗞𝗼𝗻𝘁𝗼𝗹!!!**")
    sleep(3)
    await typew.edit("`𝗞𝗼𝗻𝘁𝗼𝗹 𝗞𝗼𝗻𝘁𝗼𝗹 𝗞𝗼𝗻𝘁𝗼𝗹!!!`")
    sleep(3)
    await typew.edit("`𝗗𝗮𝘀𝗮𝗿 𝗞𝗲𝗽𝗮𝗹𝗮 𝗞𝗼𝗻𝘁𝗼𝗹!!!`")


@register(outgoing=True, pattern='^G(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝗘𝗺𝗺... 𝗯𝗲𝗻𝘁𝗮𝗿 𝗴𝘂𝗮 𝗽𝗶𝗸𝗶𝗿 𝗱𝘂𝗹𝘂...**")
    sleep(3)
    await typew.edit("`𝗚𝗮 𝗱𝘂𝗹𝘂 𝗱𝗲𝗵..`")


@register(outgoing=True, pattern='^P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"**𝗛𝗮𝗹𝗼𝗼𝗼.... 𝗞𝗲𝗻𝗮𝗹𝗶𝗻 𝗡𝗮𝗺𝗮 𝗚𝘂𝗮 {DEFAULTUSER}**")
    sleep(2)
    await typew.edit("`𝗦𝗮𝗹𝗮𝗺 𝗞𝗲𝗻𝗮𝗹....`")


@register(outgoing=True, pattern='^L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`𝗘𝗵𝗵 𝗔𝗱𝗮 𝗬𝗮𝗻𝗴 𝗦𝗮𝗹𝗮𝗺...`")
    sleep(1)
    await typew.edit("`𝗪𝗮'𝗮𝗹𝗮𝗶𝗸𝘂𝗺𝘀𝗮𝗹𝗮𝗺...`")


CMD_HELP.update({
    "salam":
    "`P`\
\nUsage: Untuk Memberi Hujatan.\
\n\n`L`\
\nUsage: Untuk Menjawab Salam.\
\n\n`G`\
\nUsage: Untuk Menolak.\
\n\n`kntl`\
\nUsage: Toxic Abis."
})
