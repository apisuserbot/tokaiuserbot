from time import sleep
from platform import uname
from userbot import CMD_HELP
from userbot.plugins import ALIVE_NAME
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern='^Kntl(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"`Kontol`")
    sleep(3)
    await typew.edit("`Tau kontol!?`")
    sleep(3)
    await typew.edit("`Mukalo kaya kontol!!!`")


@register(outgoing=True, pattern='^G(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"`Emm, bentar gua pikir dulu...`")
    sleep(3)
    await typew.edit("`Ga dulu deh...`")


@register(outgoing=True, pattern='^Salken(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit(f"`Halo, kenalin gua {DEFAULTUSER}`")
    sleep(2)
    await typew.edit("`Salam kenal...`")


@register(outgoing=True, pattern='^L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`وَالسَّلاَمُعَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ`")


@register(outgoing=True, pattern='^P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ`")


CMD_HELP.update({
    "salam":
    "`kntl`\
\nUsage: Untuk Memberi Hujatan.\
\n\n`L`\
\nUsage: Untuk Menjawab Salam.\
\n\n`G`\
\nUsage: Untuk Menolak.\
\n\n`P`\
\nUsage: Untuk memberi salam dan perkenalan."
})
