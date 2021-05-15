import asyncio
import os
import sys

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

if Config.UPSTREAM_REPO == "tokaibot":
    UPSTREAM_REPO_URL = "https://github.com/Tokai-Robo/tokaiuserbot"
elif Config.UPSTREAM_REPO == "badcat":
    UPSTREAM_REPO_URL = "https://github.com/Jisan09/catuserbot"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "heroku aplikasi tidak terdeteksi, hmm? "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting aplikasi heroku"
IS_SELECTED_DIFFERENT_BRANCH = (
    "terlihat seperti custom branch {branch_name} "
    "sedang digunakan:\n"
    "dalam hal itu, Updater tidak dapat mengidentifikasi branch mana yang relevant."
    "tolong cek/gunakan official branch, dan re-start updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**UPDATE Baru tersedia untuk [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog terlalu besar, buka file untuk melihatnya.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "`Successfully Updated!\n" "Bot restarting.. Mohon tunggu!`"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    os.execle(sys.executable, *args, os.environ)
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"update(| now)$"))
@bot.on(sudo_cmd(pattern="update(| now)$", allow_sudo=True))
async def upstream(event):
    "Untuk .update command, check jika bot telah up to date, update dengan spesifikasi"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`Mengecek update,mohon tunggu...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "`Set vars yang dibutuhkan dahulu untuk mengupdate bot`"
        )
    try:
        txt = "`Oops.. Updater tidak dapat dilnjutkan karena "
        txt += "beberapa masalah terdeteksi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} tidak terdeteksi`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Gagal! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Sayangnya, directory telah {error} "
                "sepertinya itu bukan git repository.\n"
                "Proses update masih bisa dilakukan dengan mengetik "
                ".update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Sepertinya kamu menggunakan custom branch ({ac_br}). "
            "dalam hal itu, Updater tidak dapat mengidentifikasi "
            "branch mana yang palin relevant. "
            "Tolong cek/gunakan official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "\n`Tokai-Userbot telah`  **up-to-date**  `dengan`  "
            f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond("`Ketik .update now untuk update Tokai-Ubot\n"
                                   "Ketik .update deploy untuk update dengan metode deploy ulang Tokai-Ubot`")

    if force_update:
        await event.edit(
            "`Force-Syncing pada system inti, mohon tunggu...`"
        )
    if conf == "now":
        await event.edit("`Update dalam proses, mohon tunggu...`")
        await update(event, repo, ups_rem, ac_br)
    return


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`Tolong set up` **HEROKU_APP_NAME** `Var`"
                " agar dapat mengupdate userbot...`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Invalid Heroku credentials for deploying userbot dyno.`"
            )
            return repo.__del__()
        await event.edit(
            "`Userbot dyno build dalam proses, mohon tunggu hingga proses selesai. Proses biasanya memakan waktu 4-5 menit.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`Here is the error log:\n{error}`")
            return repo.__del__()
        build_status = app.builds(order_by="created_at", sort="desc")[0]
        if build_status.status == "failed":
            await event.edit(
                "`Build gagal!\n" "Tertunda atau error pada system...`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit("`Deploy telah sukses!\n" "Restarting, mohon tunggu...`")
    else:
        await event.edit("`Tolong set up`  **HEROKU_API_KEY**  ` Var...`")
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"update deploy$"))
@bot.on(sudo_cmd(pattern="update deploy$", allow_sudo=True))
async def upstream(event):
    event = await edit_or_reply(event, "`Pulling Tokai-Ubot repo, mohon tunggu....`")
    off_repo = "https://github.com/Mr-confused/catpack"
    os.chdir("/app")
    catcmd = f"rm -rf .git"
    try:
        await _catutils.runcmd(catcmd)
    except BaseException:
        pass
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("`Deploying userbot, mohon tunggu....`")
    await deploy(event, repo, ups_rem, ac_br, txt)


@bot.on(admin_cmd(pattern=r"badcat$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"badcat$", allow_sudo=True))
async def variable(var):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            var,
            "Set the required var in heroku to function this normally `HEROKU_API_KEY`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            var,
            "Set the required var in heroku to function this normally `HEROKU_APP_NAME`.",
        )
    heroku_var = app.config()
    await edit_or_reply(var, f"`Changing goodcat to badcat wait for 2-3 minutes.`")
    heroku_var["UPSTREAM_REPO"] = "https://github.com/Jisan09/catuserbot"


CMD_HELP.update(
    {
        "updater": "**Plugin : **`updater`"
        "\n\n•  **Syntax : **`.update`"
        "\n•  **Function :** Checks if the main userbot repository has any updates "
        "and shows a changelog if so."
        "\n\n•  **Syntax : **`.update now`"
        "\n•  **Function :** Update your userbot, "
        "if there are any updates in your userbot repository.if you restart these goes back to last time when you deployed"
        "\n\n•  **Syntax : **`.update deploy`"
        "\n•  **Function :** Deploy your userbot.So even you restart it doesnt go back to previous version"
        "\nThis will triggered deploy always, even no updates."
        "\n\n•  **Syntax : **`.badcat`"
        "\n•  **Function :** Shifts from official cat repo to jisan's repo(for gali commands)"
    }
)
