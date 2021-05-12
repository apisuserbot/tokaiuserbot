import time
from platform import python_version
from time import sleep
from telethon import version

from . import ALIVE_NAME, StartTime, catversion, get_readable_time, mention, reply_id

DEFAULTUSER = ALIVE_NAME or "cat"
CAT_IMG = Config.ALIVE_PIC
CUSTOM_ALIVE_TEXT = Config.CUSTOM_ALIVE_TEXT or "Tokai U-Bot"
EMOJI = Config.CUSTOM_ALIVE_EMOJI or "┃➠ "


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if CAT_IMG:
        await alive.edit("`Activating system.....`")
        sleep(2)
        await alive.edit("`Activating...0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...8%\n███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...20%\n██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...36%\n██████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...52%\n██████████████▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...84%\n█████████████████████▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...100%\n█████████████████████████`")
        await alive.edit("⚡")
        sleep(3)
        cat_caption = f"**••━━━━━━ ✘ {CUSTOM_ALIVE_TEXT} ✘ ━━━━━━••**\n"
        cat_caption += f"**╭━━✠━━━━━━━ ◈◈ ━━━━━━━✠━━╮**\n"
        cat_caption += f"**{EMOJI}** **Data :** `{check_sgnirts}`\n"
        cat_caption += f"**{EMOJI}** **Telethon :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI}** **Bot Ver :** `{catversion}`\n"
        cat_caption += f"**{EMOJI}** **Phyton :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI}** **Uptime :** `{uptime}\n`"
        cat_caption += f"**{EMOJI}** **Owner :** {mention}\n"
        cat_caption += f"**╰━━✠━━━━━━━ ◈◈ ━━━━━━━✠━━╯**\n"
        await alive.client.send_file(
            alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id
        )
        await alive.delete()
    else:
        await alive.edit("`Activating system.....`")
        sleep(2)
        await alive.edit("`Activating...0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...8%\n███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...20%\n██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...36%\n██████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...52%\n██████████████▒▒▒▒▒▒▒▒▒▒▒`")
        await alive.edit("`Activating...84%\n█████████████████████▒▒▒▒`")
        sleep(1)
        await alive.edit("`Activating...100%\n█████████████████████████`")
        await alive.edit("⚡")
        sleep(3)
        await edit_or_reply(
            alive,
            f"**••━━━━━ ✘ {CUSTOM_ALIVE_TEXT} ✘ ━━━━━••**\n"
            f"**╭━━✠━━━━━━ ◈◈ ━━━━━━✠━━╮**\n"
            f"**{EMOJI}** **Data :** `{check_sgnirts}`\n"
            f"**{EMOJI}** **Telethon :** `{version.__version__}\n`"
            f"**{EMOJI}** **Bot Ver :** `{catversion}`\n"
            f"**{EMOJI}** **Python :** `{python_version()}\n`"
            f"**{EMOJI}** **Uptime :** `{uptime}\n`"
            f"**{EMOJI}** **Owner :** {mention}\n"
            f"**╰━━✠━━━━━━ ◈◈ ━━━━━━✠━━╯**\n",
        )


# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "No Database is set"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "Berfungsi Normal"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update(
    {
        "alive": "**Plugin :** `alive`\
      \n\n  •  **Syntax : **`.alive` \
      \n  •  **Function : **__status of bot will be showed__\
      \nSet `ALIVE_PIC` var for media in alive message"
    }
)
