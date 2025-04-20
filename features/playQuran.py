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

    # ✅ Sort files by name (e.g. 001.mp3, 002.mp3, etc.)
    result.entries.sort(key=lambda f: f.name if isinstance(f, dropbox.files.FileMetadata) else '')

    links = []

    for entry in result.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            try:
                shared_link = dbx.sharing_create_shared_link_with_settings(entry.path_lower)
            except dropbox.exceptions.ApiError as e:
                if (isinstance(e.error, dropbox.sharing.CreateSharedLinkWithSettingsError)
                        and e.error.is_shared_link_already_exists()):
                    existing_links = dbx.sharing_list_shared_links(path=entry.path_lower, direct_only=True)
                    shared_link = existing_links.links[0] if existing_links.links else None
                else:
                    raise

            if shared_link:
                raw_url = shared_link.url.replace("?dl=0", "?raw=1")
                links.append(raw_url)

    return links


async def play_quran(event, chat_id, pytgcalls):
    audio_urls = list_files_in_folder()

    if not audio_urls:
        await event.reply("❌ لم يتم العثور على أي ملفات صوتية!")
        return

    await event.reply(f"🔄 جاري تشغيل القرآن الكريم ({len(audio_urls)} ملفات)...")

    for url in audio_urls:
        await event.reply(f"🎶 يتم الآن تشغيل: {url}")

        try:
            try:
                await pytgcalls.start()
                await pytgcalls.play(chat_id, url)
            except:
                await pytgcalls.play(chat_id, url)

            await asyncio.sleep(10)  # ⏱️ Replace with real duration if needed
        except Exception as e:
            await event.reply("⚠️ يرجى التأكد من أن الغرفة الصوتية مفتوحة")
            print(f"❌ خطأ أثناء التشغيل: {e}")
            return
