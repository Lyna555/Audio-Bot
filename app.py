import asyncio
import os
import uuid
import yt_dlp
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from pytgcalls import PyTgCalls
from dotenv import load_dotenv
from pytube import Playlist

load_dotenv()

# Telegram app information
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

#with TelegramClient(StringSession(), API_ID, API_HASH) as client:
#    print("Your session string:", client.session.save())

# Telegram userbot information
SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

pytgcalls = PyTgCalls(client)

uploaded_files = {}

SAVE_FOLDER = "./audios"
os.makedirs(SAVE_FOLDER, exist_ok=True)

active_groups = set()

# verify if the command sender is an admin
async def is_admin(event):
    if not event.is_group:
        return True
    
    chat_id = event.chat_id
    sender_id = event.sender_id

    # get all admins
    admins = await client.get_participants(chat_id, filter=ChannelParticipantsAdmins)
    
    return any(admin.id == sender_id for admin in admins)

# get youtube playlist videos
async def get_playlist_videos(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls
        return video_urls
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []

# get youtube video urlz
def get_audio_stream_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict['url']

# start the bot
@client.on(events.NewMessage(pattern="/ابدا"))
async def start_bot(event):
    
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    chat_id = event.chat_id
    active_groups.add(chat_id)

    await event.reply("""✅ البوت مفعل الآن ويمكنك استخدام الأوامر!

    🔹 **كيف يعمل البوت؟**
    1️⃣ **تفعيل البوت**: عند إرسال `/ابدا`، يتم تفعيل البوت ويصبح جاهزًا للاستجابة للأوامر.
    2️⃣ **من يمكنه استخدام البوت؟**: المشرفون ومالك القناة فقط من يمكنهم تفعيل البوت واستخدامه.
    3️⃣ **تشغيل الصوت في المحادثة الصوتية**: قم بالرد على الملف الصوتي الذي أرسلته وأرسل `/شغل` لتشغيله.
    4️⃣ **التحكم في التشغيل**:
    - ⏸ `/توقف` لإيقاف التشغيل مؤقتًا.
    - ▶ `/اكمل` لاستئناف التشغيل.
    - ⛔ `/اغلق` لإيقاف البوت والخروج من المحادثة الصوتية.
    5️⃣ **تعليمات إضافية**:
    - `/قرآن` لتشغيل القرآن كاملا.
    - `/البقرة` لتشغيل سورة البقرة.
    - `/يوسف` لتشغيل سورة يوسف.
    - `/الكهف` لتشغيل سورة الكهف.
    - `/الملك` لتشغيل سورة الملك.
    - `/دعاء` لتشغيل دعاء من الكتاب والسنة.
    - `/مستجاب` لتشغيل دعاء مستجاب.
    - `/اذكار`  لتشغيل دعاء الصباح والمساء.""")


VIDEO_URLS = {
    "/البقرة": "https://www.youtube.com/watch?v=k9NDKEw5slo",
    "/يوسف": "https://www.youtube.com/watch?v=pENMnDp_XLc",
    "/الكهف": "https://www.youtube.com/watch?v=DrTaNX51xF0",
    "/الملك": "https://www.youtube.com/watch?v=1SOzkCdDrz0",
    "/دعاء": "https://www.youtube.com/watch?v=2hEntR9k5pE",
    "/مستجاب": "https://www.youtube.com/watch?v=MHHkxeOJxQE",
    "/اذكار": "https://www.youtube.com/watch?v=xrZALrmabb0",
}

# playing existed videos
@client.on(events.NewMessage(pattern=r"/(دعاء|الملك|البقرة|مستجاب|يوسف|اذكار|الكهف)"))
async def play_specific_video(event):
    
    chat_id = event.chat_id
    
    # get command
    command = event.text.strip()
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    video_url = VIDEO_URLS.get(command)
    
    # check if the video exists
    if not video_url:
        await event.reply("❌ لم يتم العثور على الفيديو")
        return

    try:
        youtube_url = get_audio_stream_url(video_url)
    except Exception as e:
        await event.reply("⚠️ خطأ في تحميل الصوت من يوتيوب")
        print(f"yt-dlp error: {e}")
        return

    await event.reply(f"🔄 جاري تشغيل {video_url}...")
    
    try:
        try:
            await pytgcalls.start()
            await pytgcalls.play(chat_id, youtube_url)
        except:
            await pytgcalls.play(chat_id, youtube_url)
            
        await event.reply("🎥 تم تشغيل الفيديو بنجاح")
        
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن الغرفة مفتوحة")
        print(f"Error: {e}")
        return

# playing quran by Yassin El-Djazairi 
@client.on(events.NewMessage(pattern="/قرآن"))
async def play_youtube_playlist(event):
    
    chat_id = event.chat_id
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return

    playlist_url = "https://www.youtube.com/watch?v=oj1dIsucvaU&list=PLBmYhnNemtrxMMJKZ8q6HZYXKMNlfmq_y"

    # Fetch video URLs from the playlist
    video_urls = await get_playlist_videos(playlist_url)
    
    if not video_urls:
        await event.reply("❌ لم يتم العثور على أي فيديوهات في قائمة التشغيل!")
        return

    await event.reply(f"🔄 جاري تشغيل قائمة التشغيل ({len(video_urls)} فيديوهات)...")

    # Play each video in the playlist
    for video_url in video_urls:
        await event.reply(f"🎶 تشغيل: {video_url}")

        # Extract audio URL using yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'extract_audio': True,
            'no_warnings': True,
            'noplaylist': True,
            'quiet': True
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info.get('url', None)
            
        # playing video
        if audio_url:
            try:
                try:
                    await pytgcalls.start()
                    await pytgcalls.play(chat_id, audio_url)
                except:
                    await pytgcalls.play(chat_id, audio_url)
                    
                await asyncio.sleep(info.get('duration', 5))
            except Exception as e:
                await event.reply(f"⚠️ يرجى التأكد من أن الغرفة مفتوحة")
                print(f"ERROR:{e}")
                return

# join the chat voice and play the replied audio file
@client.on(events.NewMessage(pattern="/شغل"))
async def play_voice_chat(event):
    chat_id = event.chat_id

    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return

    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return

    # Check if the sender is replying to a message
    if not event.reply_to_msg_id:
        await event.reply("⚠️ يرجى الرد على الملف الصوتي الذي تريد تشغيله باستخدام /شغل")
        return

    # Get the replied message
    reply_msg = await event.get_reply_message()

    # Check if the replied message contains an audio file
    if not reply_msg.file or not reply_msg.file.ext not in ("mp4", "mp3", "ogg"):
        await event.reply("⚠️ يجب الرد على ملف صوتي فقط!")
        return

    # Extract filename if available; otherwise, generate a unique one
    filename = reply_msg.file.name if reply_msg.file.name else f"voice_{uuid.uuid4().hex}.ogg"
    file_path = os.path.join(SAVE_FOLDER, filename)

    # Download the audio file
    await event.reply("🔄 جارٍ تحميل الملف الصوتي ...")
    await reply_msg.download_media(file_path)

    # Playing the audio file
    try:
        await event.reply(f"🔊 جارٍ تشغيل: `{filename}`")

        try:
            await pytgcalls.start()
            await pytgcalls.play(chat_id, file_path)
        except:
            await pytgcalls.play(chat_id, file_path)

        await event.reply("🎶 تم تشغيل الملف الصوتي")
    
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن الغرفة مفتوحة")
        print(f"Error: {e}")
        return

# pause the audio file
@client.on(events.NewMessage(pattern="/توقف"))
async def pause_voice_chat(event):
    
    chat_id = event.chat_id
     
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return

    # stoping the audio
    try:
        if event.is_group:
            await event.reply("⏸ توقف")
            await pytgcalls.pause(chat_id)
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن البوت في الغرفة ")
        print(f"Error: {e}")
        return

# resume the audio file
@client.on(events.NewMessage(pattern="/اكمل"))
async def resume_voice_chat(event):
    
    chat_id = event.chat_id
    
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return

    # resuming the audio
    try:
        if event.is_group:
            await event.reply("▶ أكمل")
            await pytgcalls.resume(chat_id)
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن البوت في الغرفة ")
        print(f"Error: {e}")
        return

# stop the bot
@client.on(events.NewMessage(pattern="/اغلق"))
async def stop_bot(event):
    
    chat_id = event.chat_id
    
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    # stopping the bot and leaving the chat voice
    if chat_id in active_groups:
        active_groups.remove(chat_id)
        await pytgcalls.leave_call(chat_id)
        
    await event.reply("⛔ البوت متوقف الآن!")
    return


async def main():
    await client.connect()
    
    # running the bot
    print("User bot is running...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
