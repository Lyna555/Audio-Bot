import os
import asyncio
import dropbox
from dotenv import load_dotenv

load_dotenv()

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
FOLDER_PATH = "/quran"


def list_files_in_folder():
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    result = dbx.files_list_folder(FOLDER_PATH)

    links = []
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(entry.path_lower)
            raw_url = shared_link_metadata.url.replace("?dl=0", "?raw=1")
            links.append(raw_url)

    return links


async def play_quran(event, chat_id, pytgcalls):
    # Fetch audio URLs from the Dropbox folder
    audio_urls = list_files_in_folder()

    if not audio_urls:
        await event.reply("❌ لم يتم العثور على أي ملفات صوتية!")
        return

    await event.reply(f"🔄 جاري تشغيل قائمة التشغيل ({len(audio_urls)} ملفات)...")

    # Play each audio file
    for audio_url in audio_urls:
        await event.reply(f"🎶 تشغيل: {audio_url}")

        try:
            try:
                await pytgcalls.start()
                await pytgcalls.play(chat_id, audio_url)
            except:
                await pytgcalls.play(chat_id, audio_url)

            # Wait for the file to finish (you can replace with fixed sleep or duration check)
            await asyncio.sleep(10)  # You may want to calculate duration dynamically
        except Exception as e:
            await event.reply("⚠️ يرجى التأكد من أن الغرفة مفتوحة")
            print(f"ERROR: {e}")
            return
