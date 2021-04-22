import json

import requests

from userbot import CMD_HELP
from userbot.events import register

PLACE = ""


@register(pattern=r"^\.adzan(?: |$)(.*)")
async def get_adzan(adzan):
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("𝐓𝐨𝐥𝐨𝐧𝐠 𝐛𝐞𝐫𝐢𝐤𝐚𝐧 𝐧𝐚𝐦𝐚 𝐤𝐨𝐭𝐚 𝐚𝐭𝐚𝐮 𝐝𝐚𝐞𝐫𝐚𝐡.")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

    # url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"𝐓𝐢𝐝𝐚𝐤 𝐝𝐚𝐩𝐚𝐭 𝐦𝐞𝐧𝐞𝐦𝐮𝐤𝐚𝐧 𝐝𝐚𝐞𝐫𝐚𝐡 𝐭𝐞𝐫𝐬𝐞𝐛𝐮𝐭 `{LOCATION}`")

    parsed = json.loads(request.text)

    city = parsed["results"]["location"]["city"]
    country = parsed["results"]["location"]["country"]
    timezone = parsed["results"]["location"]["timezone"]
    date = parsed["results"]["datetime"][0]["date"]["gregorian"]

    imsak = parsed["results"]["datetime"][0]["times"]["Imsak"]
    subuh = parsed["results"]["datetime"][0]["times"]["Fajr"]
    zuhur = parsed["results"]["datetime"][0]["times"]["Dhuhr"]
    ashar = parsed["results"]["datetime"][0]["times"]["Asr"]
    maghrib = parsed["results"]["datetime"][0]["times"]["Maghrib"]
    isya = parsed["results"]["datetime"][0]["times"]["Isha"]

    result = (
        f"**Jadwal Sholat**:\n"
        f"📅 `{date} | {timezone}`\n"
        f"🌏 `{city} | {country}`\n\n"
        f"**𝐈𝐦𝐬𝐚𝐤 :** `{imsak}`\n"
        f"**𝐒𝐮𝐛𝐮𝐡 :** `{subuh}`\n"
        f"**𝐃𝐳𝐮𝐡𝐮𝐫 :** `{zuhur}`\n"
        f"**𝐀𝐬𝐡𝐚𝐫 :** `{ashar}`\n"
        f"**𝐌𝐚𝐠𝐡𝐫𝐢𝐛 :** `{maghrib}`\n"
        f"**𝐈𝐬𝐲𝐚 :** `{isya}`\n"
    )

    await adzan.edit(result)


CMD_HELP.update({"adzan": "\n\n`>.adzan <city>`"
                 "\nUsage: Gets the prayer time for moslem."})
