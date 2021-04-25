import asyncio

import requests
from telethon import functions

from . import ALIVE_NAME, CMD_LIST, SUDO_LIST
from .sql_helper.globals import addgvar, gvarstatus


@bot.on(admin_cmd(outgoing=True, pattern="help ?(.*)"))
async def cmd_list(event):
    if event.fwd_from:
        return
    if gvarstatus("HELPTYPE") and gvarstatus("HELPTYPE") == "false":
        HELPTYPE = False
    else:
        HELPTYPE = True
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = (
            "Total {count} commands found in {plugincount} plugins of catuserbot\n\n"
        )
        catcount = 0
        plugincount = 0
        for i in sorted(CMD_LIST):
            plugincount += 1
            string += f"{plugincount}) Commands found in Plugin " + i + " are \n"
            for iter_list in CMD_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"**All commands of the catuserbot can be seen [here]({url})**"
            await event.edit(reply_text)
            return
        await event.edit(string.format(count=catcount, plugincount=plugincount))
        return
    if input_str:
        if input_str in CMD_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in CMD_LIST[input_str]:
                string += f"  •  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.edit(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            await event.edit(input_str + " 𝐭𝐢𝐝𝐚𝐤 𝐚𝐝𝐚 𝐝𝐚𝐥𝐚𝐦 𝐩𝐥𝐮𝐠𝐢𝐧!")
            await asyncio.sleep(3)
            await event.delete()
    else:
        if HELPTYPE is True:
            help_string = f"𝐀𝐬𝐢𝐬𝐭𝐞𝐧 𝐔-𝐁𝐨𝐭. 𝐏𝐫𝐨𝐯𝐢𝐝𝐞𝐝 𝐛𝐲 {ALIVE_NAME} 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐥𝐚𝐤𝐮𝐤𝐚𝐧 𝐜𝐡𝐞𝐜𝐤 𝐤𝐞 𝐬𝐞𝐦𝐮𝐚 𝐩𝐥𝐮𝐠𝐢𝐧.\
                          \n𝐂𝐡𝐞𝐜𝐤 `.help plugin name` 𝐡𝐚𝐧𝐲𝐚 𝐮𝐧𝐭𝐮𝐤 𝐜𝐨𝐦𝐦𝐚𝐧𝐝, 𝐭𝐢𝐝𝐚𝐤 𝐭𝐞𝐫𝐦𝐚𝐬𝐮𝐤 𝐟𝐮𝐧𝐠𝐬𝐢.\
                          \n𝐂𝐡𝐞𝐜𝐤 `.info plugin name` 𝐮𝐧𝐭𝐮𝐤 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐛𝐞𝐬𝐞𝐫𝐭𝐚 𝐟𝐮𝐧𝐠𝐬𝐢 𝐩𝐥𝐮𝐠𝐢𝐧 𝐭𝐞𝐫𝐬𝐞𝐛𝐮𝐭"
            tgbotusername = Config.TG_BOT_USERNAME
            results = await event.client.inline_query(tgbotusername, help_string)
            await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
            await event.delete()
        else:
            string = "<b>𝐁𝐞𝐫𝐢 𝐬𝐩𝐞𝐬𝐢𝐟𝐢𝐤𝐚𝐬𝐢 𝐩𝐥𝐮𝐠𝐢𝐧 𝐦𝐚𝐧𝐚 𝐲𝐚𝐧𝐠 𝐢𝐧𝐠𝐢𝐧 𝐤𝐚𝐦𝐮 𝐡𝐞𝐥𝐩 !!\
                \n𝐉𝐮𝐦𝐥𝐚𝐡 𝐩𝐥𝐮𝐠𝐢𝐧 : </b><code>{count}</code>\
                \n<b>𝐅𝐮𝐧𝐠𝐬𝐢:</b> <code>.help 𝐧𝐚𝐦𝐚 𝐩𝐥𝐮𝐠𝐢𝐧</code> \n\n"
            catcount = 0
            for i in sorted(CMD_LIST):
                string += "╔" + f"<code>{str(i)}</code>"
                string += "╝"
                catcount += 1
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@bot.on(sudo_cmd(allow_sudo=True, pattern="help ?(.*)"))
async def info(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = "Total {count} commands found in {plugincount} sudo plugins of catuserbot\n\n"
        catcount = 0
        plugincount = 0
        for i in sorted(SUDO_LIST):
            plugincount += 1
            string += f"{plugincount}) Commands found in Plugin " + i + " are \n"
            for iter_list in SUDO_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"All commands of the catuserbot are [here]({url})"
            await event.reply(reply_text, link_preview=False)
            return
        await event.reply(
            string.format(count=catcount, plugincount=plugincount), link_preview=False
        )
        return
    if input_str:
        if input_str in SUDO_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in SUDO_LIST[input_str]:
                string += f"  •  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.reply(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            reply = await event.reply(input_str + " 𝐭𝐢𝐝𝐚𝐤 𝐚𝐝𝐚 𝐝𝐚𝐥𝐚𝐦 𝐩𝐥𝐮𝐠𝐢𝐧!")
            await asyncio.sleep(3)
            await event.delete()
            await reply.delete()
    else:
        string = "<b>𝐁𝐞𝐫𝐢 𝐬𝐩𝐞𝐬𝐢𝐟𝐢𝐤𝐚𝐬𝐢 𝐩𝐥𝐮𝐠𝐢𝐧 𝐦𝐚𝐧𝐚 𝐲𝐚𝐧𝐠 𝐢𝐧𝐠𝐢𝐧 𝐤𝐚𝐦𝐮 𝐡𝐞𝐥𝐩 !!\
            \n𝐉𝐮𝐦𝐥𝐚𝐡 𝐩𝐥𝐮𝐠𝐢𝐧 : </b><code>{count}</code>\
            \n<b>𝐅𝐮𝐧𝐠𝐬𝐢:</b> <code>.help 𝐧𝐚𝐦𝐚 𝐩𝐥𝐮𝐠𝐢𝐧</code>\n\n"
        catcount = 0
        for i in sorted(SUDO_LIST):
            string += "🔖" + f"<code>{str(i)}</code>"
            string += "🔖"
            catcount += 1
        await event.reply(string.format(count=catcount), parse_mode="HTML")


@bot.on(admin_cmd(outgoing=True, pattern="info ?(.*)"))
@bot.on(sudo_cmd(pattern="info ?(.*)", allow_sudo=True))
async def info(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            event = await edit_or_reply(event, "𝐏𝐥𝐮𝐠𝐢𝐧 𝐭𝐢𝐝𝐚𝐤 𝐚𝐝𝐚!!!")
            await asyncio.sleep(3)
            await event.delete()
    else:
        string = "<b>𝐁𝐞𝐫𝐢 𝐬𝐩𝐞𝐬𝐢𝐟𝐢𝐤𝐚𝐬𝐢 𝐩𝐥𝐮𝐠𝐢𝐧 𝐦𝐚𝐧𝐚 𝐲𝐚𝐧𝐠 𝐢𝐧𝐠𝐢𝐧 𝐤𝐚𝐦𝐮 𝐡𝐞𝐥𝐩 !!\
            \n𝐉𝐮𝐦𝐥𝐚𝐡 𝐩𝐥𝐮𝐠𝐢𝐧 : </b><code>{count}</code>\
            \n<b>𝐅𝐮𝐧𝐠𝐬𝐢 : </b><code>.info 𝐧𝐚𝐦𝐚 𝐩𝐥𝐮𝐠𝐢𝐧</code>\n\n"
        catcount = 0
        for i in sorted(CMD_HELP):
            string += "🔖" + f"<code>{str(i)}</code>"
            string += "🔖"
            catcount += 1
        if event.sender_id in Config.SUDO_USERS:
            await event.reply(string.format(count=catcount), parse_mode="HTML")
        else:
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@bot.on(admin_cmd(pattern="dc$"))
@bot.on(sudo_cmd(pattern="dc$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetNearestDcRequest())
    result = (
        _format.yaml_format(result)
        + "\n\n**List Of Telegram Data Centres:**\
                \nDC1 : Miami FL, USA\
                \nDC2 : Amsterdam, NL\
                \nDC3 : Miami FL, USA\
                \nDC4 : Amsterdam, NL\
                \nDC5 : Singapore, SG\
                "
    )
    await edit_or_reply(event, result)


@bot.on(admin_cmd(outgoing=True, pattern="setinline (true|false)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    h_type = input_str == "true"
    if gvarstatus("HELPTYPE") and gvarstatus("HELPTYPE") == "false":
        HELPTYPE = False
    else:
        HELPTYPE = True
    if HELPTYPE:
        if h_type:
            await event.edit("`𝐈𝐧𝐥𝐢𝐧𝐞 𝐦𝐨𝐝𝐞 𝐭𝐞𝐥𝐚𝐡 𝐡𝐢𝐝𝐮𝐩!!!`")
        else:
            addgvar("HELPTYPE", h_type)
            await event.edit("`𝐈𝐧𝐥𝐢𝐧𝐞 𝐦𝐨𝐝𝐞 𝐝𝐢𝐦𝐚𝐭𝐢𝐤𝐚𝐧!!!`")
    else:
        if h_type:
            addgvar("HELPTYPE", h_type)
            await event.edit("`𝐈𝐧𝐥𝐢𝐧𝐞 𝐦𝐨𝐝𝐞 𝐝𝐢𝐡𝐢𝐝𝐮𝐩𝐤𝐚𝐧!!!`")
        else:
            await event.edit("`𝐈𝐧𝐥𝐢𝐧𝐞 𝐦𝐨𝐝𝐞 𝐭𝐞𝐥𝐚𝐡 𝐦𝐚𝐭𝐢!!!`")


CMD_HELP.update(
    {
        "help": """**Plugin : **`help`

•  **Syntax : **`.help/.help plugin_name`
•  **Function : **__If you just type .help then shows you help menu, if plugin name is given then shows you only commands in thst plugin and if you use `.help text` then shows you all commands in your userbot__

•  **Syntax : **`.info/.info plugin_name`
•  **Function : **__To get details/information/usage of that plugin__

•  **Syntax : **`.dc`
•  **Function : **__Shows your dc id and dc ids list__

•  **Syntax : **`.setinline (true|false)`
•  **Function : **__Sets help menu either in inline or text format__"""
    }
)
