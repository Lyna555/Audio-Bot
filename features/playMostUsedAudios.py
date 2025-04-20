import aiohttp
import aiofiles
import os

AUDIO_FOLDER = "audios"

# Create the audios folder if it doesn't exist
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

VIDEO_URLS = {
    "/البقرة": "https://www.dropbox.com/scl/fi/mqxmah0lteljq7t9jo3fd/bakara.mp3?rlkey=owk93u0vayy22pfq6wf1tr37u&st=gqiw2q7n&dl=0",
    "/يوسف": "https://www.dropbox.com/scl/fi/r261wx0ceo1ctouq4j2ts/youssef.mp3?rlkey=u4crt1cfuaxoteb4qojwd49nx&st=hvygnyun&dl=0",
    "/الكهف": "https://www.dropbox.com/scl/fi/iqbk93kzy5jd39cvy9kjs/kahf.mp3?rlkey=3e7nz4v095ep974tnsnxc090f&st=y4sdm69p&dl=0",
    "/الملك": "https://www.dropbox.com/scl/fi/ntiubyr7wza95ovciq3by/mulk.mp3?rlkey=4wms180vooa2ypdry5763hn36&st=yo5m7nma&dl=0",
    "/دعاء": "https://www.dropbox.com/scl/fi/boda0c196v4uwdw7wwdzx/kitab.mp3?rlkey=vidx8wtj493gpjfb34xmpqw1c&st=z50rm526&dl=0",
    "/مستجاب": "https://www.dropbox.com/scl/fi/9xmqeo5vp482gtp79w9jx/mustadjab.mp3?rlkey=vh4d5v2vov8c4rgzvh2afi6bg&st=nw9clwlt&dl=0",
    "/اذكار": "https://www.dropbox.com/scl/fi/flejra23x4kj5kkifebuh/adhkar.mp3?rlkey=2bsrm88i5r6vt8qgyu6rzogd1&st=xxt6oyq8&dl=0",
}

async def download_to_audios(dropbox_url, name):
    if "dl=0" in dropbox_url:
        dropbox_url = dropbox_url.replace("dl=0", "raw=1")
    elif "dl=1" in dropbox_url:
        dropbox_url = dropbox_url.replace("dl=1", "raw=1")

    file_path = os.path.join(AUDIO_FOLDER, f"{name}.mp3")
    
    if os.path.exists(file_path):
        return file_path  # Already downloaded

    async with aiohttp.ClientSession() as session:
        async with session.get(dropbox_url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(await resp.read())
                return file_path
            else:
                return None

async def play_most_used_audios(event, chat_id, pytgcalls):
    command = event.text.strip()
    dropbox_url = VIDEO_URLS.get(command)

    if not dropbox_url:
        await event.reply("❌ لم يتم العثور على الفيديو")
        return

    name = command.replace("/", "")  # e.g. "البقرة"
    await event.reply("🔄 جاري التحميل والتشغيل...")

    audio_file = await download_to_audios(dropbox_url, name)

    if not audio_file:
        await event.reply("⚠️ فشل في تحميل الملف")
        return

    try:
        await pytgcalls.start()
        await pytgcalls.play(chat_id, audio_file)
        await event.reply("🎧 تم تشغيل الصوت بنجاح")
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن الغرفة مفتوحة")
        print(f"Error: {e}")
