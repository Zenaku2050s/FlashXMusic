from logging import getLogger

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont
from pyrogram import enums, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup

from FlashXMusic import app

random_photo = [
    "https://telegra.ph/file/c1e44824e6b8d41def80c.jpg",
    "https://telegra.ph/file/18e61e800e05062b61b83.jpg",
    "https://telegra.ph/file/0968f0f08b94cc21c2689.jpg",
    "https://telegra.ph/file/9e56aec423cd7c5daabf9.jpg",
    "https://telegra.ph/file/0b98dc047825876744a2e.jpg",
]
# --------------------------------------------------------------------------------- #


LOGGER = getLogger(__name__)


class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}  # Default state is "on"

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]


wlcm = WelDatabase()


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None


def circle(pfp, size=(700, 700)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chatname, id, uname):
    background = Image.open("FlashXMusic/assets/FlashXMusicl2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((1157, 1158))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('FlashXMusic/assets/font.ttf', size=110)
    welcome_font = ImageFont.truetype('FlashXMusic/assets/font.ttf', size=60)
    draw.text((1800, 700), f'NAME: {user}', fill=(255, 255, 255), font=font)
    draw.text((1800, 830), f'ID: {id}', fill=(255, 255, 255), font=font)
    draw.text((1800, 965), f"USERNAME : {uname}", fill=(255, 255, 255), font=font)
    pfp_position = (391, 336)
    background.paste(pfp, pfp_position, pfp)
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(
                    f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ** {message.chat.title}"
                )
        elif state == "on":
            if not A:
                await message.reply_text("**ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ.**")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(
                    f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ ** {message.chat.title}"
                )
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ!**")


@app.on_chat_member_updated(filters.group, group=-8)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)
    if A:
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    # Add the modified condition here
    if member.new_chat_member and not member.old_chat_member:

        try:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except AttributeError:
            pic = "FlashXMusic/assets/upic.png"
        if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
            except Exception as e:
                LOGGER.error(e)
        try:
            welcomeimg = welcomepic(
                pic, user.first_name, member.chat.title, user.id, user.username
            )
            button_text = "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏"
            add_button_text = "๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏"
            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link = f"https://t.me/{app.username}?startgroup=true"
            temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
                member.chat.id,
                photo=welcomeimg,
                caption=f"""
**ʜᴇʏ {user.mention} ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ {member.chat.title} ! 
✧ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ✧**
━━━━━━━━━━━━━━━━━━━━━
**✧ ɴᴀᴍᴇ ๏** {user.mention}
**✧ ɪᴅ ๏** `{user.id}`
**✧ ᴜ_ɴᴀᴍᴇ ๏** @{user.username}
**✧ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ๏** {count}
━━━━━━━━━━━━━━━━━━━━━
""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(button_text, url=deep_link)],
                        [InlineKeyboardButton(text=add_button_text, url=add_link)],
                    ]
                ),
            )
        except Exception as e:
            return


__MODULE__ = "Welcome"
__HELP__ = """
## Welcome Module

This module handles welcome messages for new members joining a group.

### Commands:
- `/welcome [on|off]`: Enable or disable welcome notifications in the group.

### Features:
- Automatically sends a welcome message when a new member joins the group.
- Allows admins to enable or disable welcome notifications.

"""
