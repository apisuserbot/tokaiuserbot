# Userbot module to help you manage a group

# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights, MessageMediaPhoto

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, LOGS, get_user_from_event
from .sql_helper.mute_sql import is_muted, mute, unmute

# =================== CONSTANT ===================

PP_TOO_SMOL = "`𝐆𝐚𝐦𝐛𝐚𝐫 𝐭𝐞𝐫𝐥𝐚𝐥𝐮 𝐤𝐞𝐜𝐢𝐥 𝐛𝐨𝐬𝐬!!!`"
PP_ERROR = "`𝐆𝐚𝐠𝐚𝐥 𝐦𝐞𝐦𝐩𝐫𝐨𝐬𝐞𝐬 𝐠𝐚𝐦𝐛𝐚𝐫!!!`"
NO_ADMIN = "`𝐁𝐨𝐬 𝐛𝐮𝐤𝐚𝐧 𝐚𝐝𝐦𝐢𝐧!!!`"
NO_PERM = "`𝐁𝐨𝐬 𝐭𝐢𝐝𝐚𝐤 𝐩𝐮𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐥𝐞𝐧𝐠𝐤𝐚𝐩!! 𝐌𝐞𝐧𝐲𝐞𝐝𝐢𝐡𝐤𝐚𝐧 𝐬𝐞𝐤𝐚𝐥𝐢`"
CHAT_PP_CHANGED = "`𝐂𝐡𝐚𝐭 𝐩𝐢𝐜𝐭𝐮𝐫𝐞 𝐝𝐢𝐠𝐚𝐧𝐭𝐢!!!`"
INVALID_MEDIA = "`𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐞𝐱𝐭𝐞𝐧𝐬𝐢𝐨𝐧!!!`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ================================================


@bot.on(admin_cmd(pattern="setgpic$"))
@bot.on(sudo_cmd(pattern="setgpic$", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    if gpic.fwd_from:
        return
    if not gpic.is_group:
        await edit_or_reply(gpic, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    replymsg = await gpic.get_reply_message()
    await gpic.get_chat()
    photo = None
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await edit_or_reply(gpic, INVALID_MEDIA)
    sandy = None
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await edit_or_reply(gpic, CHAT_PP_CHANGED)
            sandy = True
        except PhotoCropSizeSmallError:
            await edit_or_reply(gpic, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await edit_or_reply(gpic, PP_ERROR)
        except Exception as e:
            await edit_or_reply(gpic, f"**𝐆𝐚𝐠𝐚𝐥 : **`{str(e)}`")
        if BOTLOG and sandy:
            await gpic.client.send_message(
                BOTLOG_CHATID,
                "#GROUPPIC\n"
                f"Group profile pic changed "
                f"CHAT: {gpic.chat.title}(`{gpic.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="promote(?: |$)(.*)", command="promote"))
@bot.on(sudo_cmd(pattern="promote(?: |$)(.*)", command="promote", allow_sudo=True))
@errors_handler
async def promote(promt):
    if promt.fwd_from:
        return
    if not promt.is_group:
        await edit_or_reply(promt, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    catevent = await edit_or_reply(promt, "`𝐏𝐫𝐨𝐦𝐨𝐭𝐢𝐧𝐠...`")
    user, rank = await get_user_from_event(promt, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await catevent.edit("`𝐏𝐫𝐨𝐦𝐨𝐭𝐞𝐝 𝐬𝐮𝐤𝐬𝐞𝐬!!! 𝐂𝐢𝐞𝐞 𝐚𝐝𝐦𝐢𝐧 𝐛𝐚𝐫𝐮...`")
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="demote(?: |$)(.*)", command="demote"))
@bot.on(sudo_cmd(pattern="demote(?: |$)(.*)", command="demote", allow_sudo=True))
@errors_handler
async def demote(dmod):
    if dmod.fwd_from:
        return
    if not dmod.is_group:
        await edit_or_reply(dmod, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(dmod, NO_ADMIN)
        return
    catevent = await edit_or_reply(dmod, "`𝐃𝐞𝐦𝐨𝐭𝐢𝐧𝐠...`")
    rank = "admeme"
    user = await get_user_from_event(dmod, catevent)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    await catevent.edit("`𝐃𝐞𝐦𝐨𝐭𝐞𝐝 𝐬𝐮𝐤𝐬𝐞𝐬!!! 𝐌𝐞𝐧𝐠𝐬𝐞𝐝𝐢𝐡𝐤𝐚𝐧...`")
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="ban(?: |$)(.*)", command="ban"))
@bot.on(sudo_cmd(pattern="ban(?: |$)(.*)", command="ban", allow_sudo=True))
@errors_handler
async def ban(bon):
    if bon.fwd_from:
        return
    if not bon.is_group:
        await edit_or_reply(bon, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(bon, NO_ADMIN)
        return
    catevent = await edit_or_reply(bon, "`𝐒𝐞𝐥𝐚𝐦𝐚𝐭 𝐭𝐢𝐧𝐠𝐠𝐚𝐥...`")
    user, reason = await get_user_from_event(bon, catevent)
    if not user:
        return
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catevent.edit(
            "`𝐀𝐤𝐮 𝐭𝐢𝐝𝐚𝐤 𝐩𝐮𝐧𝐲𝐚 𝐚𝐥𝐚𝐬𝐚𝐧... 𝐓𝐚𝐩𝐢 𝐝𝐢𝐚 𝐭𝐞𝐭𝐚𝐩 𝐭𝐞𝐫𝐛𝐚𝐧𝐧𝐞𝐝!!`"
        )
        return
    if reason:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)}` 𝐓𝐞𝐥𝐚𝐡 𝐝𝐢𝐛𝐚𝐧𝐧𝐞𝐝!!`\n**𝐊𝐚𝐫𝐞𝐧𝐚 : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `𝐓𝐞𝐥𝐚𝐡 𝐝𝐢𝐛𝐚𝐧𝐧𝐞𝐝!!`"
        )
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
        )


@bot.on(admin_cmd(pattern="unban(?: |$)(.*)", command="unban"))
@bot.on(sudo_cmd(pattern="unban(?: |$)(.*)", command="unban", allow_sudo=True))
@errors_handler
async def nothanos(unbon):
    if unbon.fwd_from:
        return
    if not unbon.is_group:
        await edit_or_reply(unbon, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(unbon, NO_ADMIN)
        return
    catevent = await edit_or_reply(unbon, "`𝐔𝐧𝐛𝐚𝐧𝐧𝐢𝐧𝐠...`")
    user = await get_user_from_event(unbon, catevent)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `𝐔𝐧𝐛𝐚𝐧𝐞𝐝 𝐬𝐮𝐤𝐬𝐞𝐬!!! 𝐉𝐚𝐧𝐠𝐚𝐧 𝐧𝐚𝐤𝐚𝐥 𝐥𝐚𝐠𝐢 𝐲𝐚...`"
        )
        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("`𝐁𝐨𝐬!! 𝐔𝐧𝐛𝐚𝐧 𝐥𝐨𝐠𝐢𝐜 𝐞𝐫𝐫𝐨𝐫...`")


@bot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="mute(?: |$)(.*)", command="mute"))
@bot.on(sudo_cmd(pattern="mute(?: |$)(.*)", command="mute", allow_sudo=True))
async def startmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("`𝐒𝐢𝐬𝐭𝐞𝐦 𝐞𝐫𝐫𝐨𝐫!!! 𝐌𝐚𝐢𝐧 𝐩𝐫𝐨𝐛𝐥𝐞𝐦 𝐭𝐚𝐤 𝐝𝐢𝐤𝐞𝐭𝐚𝐡𝐮𝐢...`")
        await sleep(2)
        await event.get_reply_message()
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if is_muted(userid, chat_id):
            return await event.edit(
                "`𝐁𝐨𝐬, 𝐮𝐬𝐞𝐫 𝐢𝐧𝐢 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞!!! 𝐆𝐢𝐦𝐚𝐧𝐚 𝐬𝐢𝐡 𝐛𝐨𝐬...`"
            )
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.edit(f"**𝐆𝐚𝐠𝐚𝐥 **\n`{str(e)}`")
        else:
            await event.edit("`𝐔𝐬𝐞𝐫 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"**User :** [{replied_user.user.first_name}](tg://user?id={userid})\n",
            )
    else:
        chat = await event.get_chat()
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "`𝐌𝐚𝐚𝐟, 𝐚𝐤𝐮 𝐭𝐢𝐝𝐚𝐤 𝐛𝐢𝐬𝐚 𝐦𝐮𝐭𝐞 𝐛𝐨𝐬𝐤𝐮 𝐬𝐞𝐧𝐝𝐢𝐫𝐢!!!`")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "`𝐁𝐨𝐬, 𝐮𝐬𝐞𝐫 𝐢𝐧𝐢 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞!!! 𝐆𝐢𝐦𝐚𝐧𝐚 𝐬𝐢𝐡 𝐛𝐨𝐬...`"
            )
        try:
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                await edit_or_reply(
                    event, "`𝐁𝐨𝐬 𝐭𝐢𝐝𝐚𝐤 𝐩𝐮𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐥𝐞𝐧𝐠𝐤𝐚𝐩!! 𝐌𝐞𝐧𝐲𝐞𝐝𝐢𝐡𝐤𝐚𝐧 𝐬𝐞𝐤𝐚𝐥𝐢.` ಥ﹏ಥ  "
                )
                return
            result = await event.client(
                functions.channels.GetParticipantRequest(
                    channel=event.chat_id, user_id=user.id
                )
            )
            try:
                if result.participant.banned_rights.send_messages:
                    return await edit_or_reply(
                        event,
                        "`𝐁𝐨𝐬, 𝐮𝐬𝐞𝐫 𝐢𝐧𝐢 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞!!! 𝐆𝐢𝐦𝐚𝐧𝐚 𝐬𝐢𝐡 𝐛𝐨𝐬...`",
                    )
            except Exception as e:
                LOGS.info(str(e))
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "`𝐁𝐨𝐬 𝐭𝐢𝐝𝐚𝐤 𝐩𝐮𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐥𝐞𝐧𝐠𝐤𝐚𝐩!! 𝐌𝐞𝐧𝐲𝐞𝐝𝐢𝐡𝐤𝐚𝐧 𝐬𝐞𝐤𝐚𝐥𝐢. ಥ﹏ಥ`",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "`𝐁𝐨𝐬 𝐭𝐢𝐝𝐚𝐤 𝐩𝐮𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐥𝐞𝐧𝐠𝐤𝐚𝐩!! 𝐌𝐞𝐧𝐲𝐞𝐝𝐢𝐡𝐤𝐚𝐧 𝐬𝐞𝐤𝐚𝐥𝐢.` ಥ﹏ಥ  "
                )
            try:
                mute(user.id, event.chat_id)
            except Exception as e:
                return await edit_or_reply(event, f"**𝐆𝐚𝐠𝐚𝐥 **\n`{str(e)}`")
        except Exception as e:
            return await edit_or_reply(event, f"**𝐆𝐚𝐠𝐚𝐥 : **`{str(e)}`")
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `𝐔𝐬𝐞𝐫 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞 𝐝𝐢 {event.chat.title}`\n"
                f"`𝐊𝐚𝐫𝐞𝐧𝐚:`{reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `𝐔𝐬𝐞𝐫 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞 𝐝𝐢 {event.chat.title}`\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {event.chat.title}(`{event.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="unmute(?: |$)(.*)", command="unmute"))
@bot.on(sudo_cmd(pattern="unmute(?: |$)(.*)", command="unmute", allow_sudo=True))
async def endmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("`𝐒𝐢𝐬𝐭𝐞𝐦 𝐞𝐫𝐫𝐨𝐫!!! 𝐌𝐚𝐢𝐧 𝐩𝐫𝐨𝐛𝐥𝐞𝐦 𝐭𝐚𝐤 𝐝𝐢𝐤𝐞𝐭𝐚𝐡𝐮𝐢...`")
        await sleep(1)
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if not is_muted(userid, chat_id):
            return await event.edit(
                "`__𝐔𝐬𝐞𝐫 𝐢𝐧𝐢 𝐭𝐢𝐝𝐚𝐤 𝐝𝐢𝐦𝐮𝐭𝐞 𝐝𝐢𝐜𝐡𝐚𝐭 𝐢𝐧𝐢__\n（ ^_^）o自自o（^_^ ）`"
            )
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.edit(f"**𝐆𝐚𝐠𝐚𝐥 **\n`{str(e)}`")
        else:
            await event.edit(
                "`𝐔𝐬𝐞𝐫 𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐦𝐮𝐭𝐞!!!\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"**User :** [{replied_user.user.first_name}](tg://user?id={userid})\n",
            )
    else:
        user = await get_user_from_event(event)
        user = user[0]
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client(
                    functions.channels.GetParticipantRequest(
                        channel=event.chat_id, user_id=user.id
                    )
                )
                try:
                    if result.participant.banned_rights.send_messages:
                        await event.client(
                            EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                        )
                except Exception:
                    return await edit_or_reply(
                        event,
                        "`𝐔𝐬𝐞𝐫 𝐢𝐧𝐢 𝐭𝐢𝐝𝐚𝐤 𝐝𝐢𝐛𝐢𝐬𝐮𝐤𝐚𝐧 𝐥𝐚𝐠𝐢, 𝐬𝐞𝐥𝐚𝐦𝐚𝐭 𝐛𝐞𝐫𝐛𝐢𝐜𝐚𝐫𝐚...`",
                    )
        except Exception as e:
            return await edit_or_reply(event, f"**𝐆𝐚𝐠𝐚𝐥 : **`{str(e)}`")
        await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `𝐭𝐞𝐥𝐚𝐡 𝐝𝐢𝐮𝐧𝐦𝐮𝐭𝐞 𝐝𝐢 {event.chat.title}\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {event.chat.title}(`{event.chat_id}`)",
            )


@bot.on(admin_cmd(pattern="kick(?: |$)(.*)", command="kick"))
@bot.on(sudo_cmd(pattern="kick(?: |$)(.*)", command="kick", allow_sudo=True))
@errors_handler
async def kick(usr):
    if usr.fwd_from:
        return
    if not usr.is_group:
        await edit_or_reply(usr, "`𝐌𝐚𝐚𝐟 𝐛𝐨𝐬, 𝐢𝐧𝐢 𝐛𝐮𝐤𝐚𝐧 𝐠𝐫𝐮𝐩!!!`")
        return
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        return
    catevent = await edit_or_reply(usr, "`𝐌𝐞𝐧𝐞𝐧𝐝𝐚𝐧𝐠...`")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await catevent.edit(NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await catevent.edit(
            f"`𝐃𝐢𝐭𝐞𝐧𝐝𝐚𝐧𝐠` [{user.first_name}](tg://user?id={user.id})`!`\n𝐊𝐚𝐫𝐞𝐧𝐚: {reason}"
        )
    else:
        await catevent.edit(f"`𝐃𝐢𝐭𝐞𝐧𝐝𝐚𝐧𝐠!!!` [{user.first_name}](tg://user?id={user.id})`!`")
    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@bot.on(admin_cmd(pattern="pin($| (.*))", command="pin"))
@bot.on(sudo_cmd(pattern="pin($| (.*))", command="pin", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    if not msg.is_private:
        await msg.get_chat()
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        return await edit_delete(msg, "`Reply to a message to pin it.`", 5)
    options = msg.pattern_match.group(1)
    is_silent = False
    if options == "loud":
        is_silent = True
    try:
        await msg.client.pin_message(msg.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(msg, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(msg, f"`{str(e)}`", 5)
    await edit_delete(msg, "`Pinned Successfully!`", 3)
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG and not msg.is_private:
        try:
            await msg.client.send_message(
                BOTLOG_CHATID,
                "#PIN\n"
                f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
                f"LOUD: {is_silent}",
            )
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="unpin($| (.*))", command="unpin"))
@bot.on(sudo_cmd(pattern="unpin($| (.*))", command="unpin", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    if not msg.is_private:
        await msg.get_chat()
    to_unpin = msg.reply_to_msg_id
    options = (msg.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        await edit_delete(msg, "`Reply to a message to unpin it or use .unpin all`", 5)
        return
    if to_unpin and not options:
        try:
            await msg.client.unpin_message(msg.chat_id, to_unpin)
        except BadRequestError:
            return await edit_delete(msg, NO_PERM, 5)
        except Exception as e:
            return await edit_delete(msg, f"`{str(e)}`", 5)
    elif options == "all":
        try:
            await msg.client.unpin_message(msg.chat_id)
        except BadRequestError:
            return await edit_delete(msg, NO_PERM, 5)
        except Exception as e:
            return await edit_delete(msg, f"`{str(e)}`", 5)
    else:
        return await edit_delete(
            msg, "`Reply to a message to unpin it or use .unpin all`", 5
        )
    await edit_delete(msg, "`Unpinned Successfully!`", 3)
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG and not msg.is_private:
        try:
            await msg.client.send_message(
                BOTLOG_CHATID,
                "#UNPIN\n"
                f"**Admin : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat : **{msg.chat.title}(`{msg.chat_id}`)\n",
            )
        except Exception as e:
            LOGS.info(str(e))


@bot.on(admin_cmd(pattern="iundlt$", command="iundlt"))
@bot.on(sudo_cmd(pattern="iundlt$", command="iundlt", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await edit_or_reply(event, "`I don't think this is a group.`")
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=5, edit=False, delete=True
        )
        deleted_msg = "Deleted message in this group:"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await edit_or_reply(event, deleted_msg)
    else:
        await edit_or_reply(
            event, "`You need administrative permissions in order to do this command`"
        )
        await sleep(3)
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CMD_HELP.update(
    {
        "admin": "**Plugin : **`admin`\
        \n\n  •  **Syntax : **`.setgpic` <reply to image>\
        \n  •  **Usage : **Changes the group's display picture\
        \n\n  •  **Syntax : **`.promote` <username/reply> <custom rank (optional)>\
        \n  •  **Usage : **Provides admin rights to the person in the chat.\
        \n\n  •  **Syntax : **`.demote `<username/reply>\
        \n  •  **Usage : **Revokes the person's admin permissions in the chat.\
        \n\n  •  **Syntax : **`.ban` <username/reply> <reason (optional)>\
        \n  •  **Usage : **Bans the person off your chat.\
        \n\n  •  **Syntax : **`.unban` <username/reply>\
        \n  •  **Usage : **Removes the ban from the person in the chat.\
        \n\n  •  **Syntax : **`.mute` <username/reply> <reason (optional)>\
        \n  •  **Usage : **Mutes the person in the chat, works on admins too.\
        \n\n  •  **Syntax : **`.unmute` <username/reply>\
        \n  •  **Usage : **Removes the person from the muted list.\
        \n\n  •  **Syntax : **`.pin `<reply> or `.pin loud`\
        \n  •  **Usage : **Pins the replied message in Group\
        \n\n  •  **Syntax : **`.unpin `<reply> or `.unpin all`\
        \n  •  **Usage : **Unpins the replied message in Group\
        \n\n  •  **Syntax : **`.kick `<username/reply> \
        \n  •  **Usage : **kick the person off your chat.\
        \n\n  •  **Syntax : **`.iundlt`\
        \n  •  **Usage : **display last 5 deleted messages in group."
    }
)
