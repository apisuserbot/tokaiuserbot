# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

from datetime import datetime

from speedtest import Speedtest
from . import CMD_HELP, StartTime, ALIVE_NAME
from userbot.events import register
import time

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern="^.fping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit(".                       /¯ )")
    await pong.edit(".                       /¯ )\n                      /¯  /")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ ")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (")
    await pong.edit(".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  ")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**✠ 𝐏𝐢𝐧𝐠** "
                    f"\n  ➠ `%sms` \n"
                    f"**✠ 𝐎𝐰𝐧𝐞𝐫** "
                    f"\n  ➠ `{ALIVE_NAME}` \n" % (duration))


@register(outgoing=True, pattern="^.lping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("🔞")
    await pong.edit("__**𝐓𝐎𝐊𝐀𝐈🔞**__")
    await pong.edit("__**𝐓𝐎𝐊🔞𝐀𝐈**__")
    await pong.edit("__**𝐓𝐎🔞𝐊𝐀𝐈**__")
    await pong.edit("__**𝐓🔞𝐎𝐊𝐀𝐈**__")
    await pong.edit("__**🔞𝐓𝐎𝐊𝐀𝐈🔞**__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**🔞𝐓𝐎𝐊𝐀𝐈 𝐏𝐈𝐍𝐆🔞**\n"
                    f"🔞 **𝐏𝐈𝐍𝐆:** "
                    f"`%sms` \n"
                    f"🔞 **𝐎𝐍𝐋𝐈𝐍𝐄:** "
                    f"`{uptime}` \n" % (duration))


@register(outgoing=True, pattern="^.xping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Ping..............`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**🏓𝐏𝐨𝐧𝐠!!**\n"
                    f"➠ __𝐏𝐢𝐧𝐠:__ "
                    f"`%sms` \n"
                    f"➠ __𝐔𝐩𝐭𝐢𝐦𝐞:__ "
                    f"`{uptime}` \n" % (duration))


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("**✎**")
    await pong.edit("**✎✎**")
    await pong.edit("**✎✎✎**")
    await pong.edit("**🏓𝐏𝐨𝐧𝐠!!**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**✠ 𝐓𝐨𝐤𝐚𝐢 𝐏𝐢𝐧𝐠 ✠**\n"
                    f"➠ **𝐏𝐢𝐧𝐠:** "
                    f"`%sms` \n"
                    f"➠ **𝐔𝐩𝐭𝐢𝐦𝐞:** "
                    f"`{uptime}` \n"
                    f"**➠ 𝐎𝐰𝐧𝐞𝐫:** `{ALIVE_NAME}`" % (duration))


@register(outgoing=True, pattern="^.sinyal$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`𝐏𝐢𝐧𝐠𝐢𝐧𝐠 𝐒𝐞𝐫𝐯𝐞𝐫....`")
    await pong.edit("**0% ▒▒▒▒▒▒▒▒▒▒**")
    await pong.edit("**20% ██▒▒▒▒▒▒▒▒**")
    await pong.edit("**40% ████▒▒▒▒▒▒**")
    await pong.edit("**60% ██████▒▒▒▒**")
    await pong.edit("**80% ████████▒▒**")
    await pong.edit("**100% ██████████**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"- 𝐓𝐎𝐊𝐀𝐈 -\n"
                    f"**• 𝐏𝐢𝐧𝐠  :** "
                    f"`%sms` \n"
                    f"**• 𝐔𝐩𝐭𝐢𝐦𝐞  :** "
                    f"`{uptime}` \n"
                    f"**• 𝐎𝐰𝐧𝐞𝐫  :** `{ALIVE_NAME}`" % (duration))


@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    await spd.edit("`𝐒𝐞𝐝𝐚𝐧𝐠 𝐭𝐞𝐬𝐭𝐢𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐡𝐢𝐠𝐡 𝐬𝐩𝐞𝐞𝐝...📡`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    await spd.edit("**𝐓𝐞𝐬𝐭 𝐑𝐞𝐬𝐮𝐥𝐭:\n**"
                   "✎ **𝐃𝐢𝐦𝐮𝐥𝐚𝐢 𝐏𝐚𝐝𝐚:** "
                   f"`{result['timestamp']}` \n"
                   f" **━━━━━━━━━━━━━━━━━**\n\n"
                   "✎ **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝:** "
                   f"`{speed_convert(result['download'])}` \n"
                   "✎ **𝐔𝐩𝐥𝐨𝐚𝐝:** "
                   f"`{speed_convert(result['upload'])}` \n"
                   "✎ **𝐏𝐢𝐧𝐠:** "
                   f"`{result['ping']}` \n"
                   "❃ **𝐈𝐒𝐏:** "
                   f"`{result['client']['isp']}` \n"
                   "❃ **𝐁𝐎𝐓:** `𝐓𝐨𝐤𝐚𝐢 𝐔-𝐁𝐨𝐭`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.pong$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`𝐏𝐨𝐧𝐠.....🏓`")
    await pong.edit("`𝐏𝐨𝐧𝐠....🏓.`")
    await pong.edit("`𝐏𝐨𝐧𝐠...🏓..`")
    await pong.edit("`𝐏𝐨𝐧𝐠..🏓...`")
    await pong.edit("`𝐏𝐨𝐧𝐠.🏓....`")
    await pong.edit("`𝐏𝐨𝐧𝐠🏓.....`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("➠ **𝐏𝐢𝐧𝐠!!**\n`%sms`" % (duration))

CMD_HELP.update(
    {"ping": "`.ping` ; `.lping` ; `.xping` ; `.fping`\
    \nPenjelasan: Untuk menunjukkan ping bot.\
    \n\n`.speed`\
    \nPenjelasan: Untuk menunjukkan kecepatan.\
    \n\n`.pong`\
    \nPenjelasan: sama kaya perintah ping."
     })
CMD_HELP.update(
    {"sinyal": "**Modules:** `Sinyal`\
    \n\n**• Perintah :** `.sinyal`\
    \n  ➥ **Penjelasan :** __Untuk melihat sinyal bot__"})
