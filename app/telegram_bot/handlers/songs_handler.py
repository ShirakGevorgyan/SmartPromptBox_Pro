from aiogram import Router
from aiogram.types import Message

router = Router()
user_links = {}

@router.message(lambda msg: msg.text == "🎵 Ուղարկված երգեր")
async def show_sent_songs(message: Message):
    user_id = message.from_user.id
    links = user_links.get(user_id, [])

    if not links:
        await message.answer("📭 Դու դեռ ոչ մի երգի հղում չես ուղարկել։")
    else:
        await message.answer("📄 Ահա քո ուղարկած YouTube հղումները՝\n\n" + "\n".join(links))

def save_user_link(user_id: int, link: str):
    if user_id not in user_links:
        user_links[user_id] = []
    if link not in user_links[user_id]:
        user_links[user_id].append(link)
