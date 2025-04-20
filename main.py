import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from features.utilities import client, pytgcalls
from features.playMostUsedAudios import play_most_used_audios
from features.playQuran import play_quran
from features.playSendedAudio import play_sended_audio
from features.pauseSendedVideo import pause_sended_video
from features.resumeSendedVideo import resume_sended_videos

active_groups = set()

# Verify if the command sender is an admin
async def is_admin(event):
    if not event.is_group:
        return True
    
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Get all admins
    admins = await client.get_participants(chat_id, filter=ChannelParticipantsAdmins)
    
    return any(admin.id == sender_id for admin in admins)

# Start the bot
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
    
# Playing existed videos
@client.on(events.NewMessage(pattern=r"/(دعاء|الملك|البقرة|مستجاب|يوسف|اذكار|الكهف)"))
async def play_most_used_audios_handler(event):
    
    chat_id = event.chat_id
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    await play_most_used_audios(event, chat_id, pytgcalls)
    

# Playing quran by Yassin El-Djazairi 
@client.on(events.NewMessage(pattern="/قرآن"))
async def play_quran_handler(event):
    
    chat_id = event.chat_id
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    await play_quran(event, chat_id, pytgcalls)
    
# Join the chat voice and play the replied audio file
@client.on(events.NewMessage(pattern="/شغل"))
async def play_sended_audio_handler(event):
    chat_id = event.chat_id

    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    await play_sended_audio(event, chat_id, pytgcalls)
    

# Pause the audio file
@client.on(events.NewMessage(pattern="/توقف"))
async def pause_sended_audio_handler(event):
    
    chat_id = event.chat_id
     
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    await pause_sended_video(event, chat_id, pytgcalls)
    
# Resume the audio file
@client.on(events.NewMessage(pattern="/اكمل"))
async def resume_sended_video_handler(event):
    
    chat_id = event.chat_id
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    await resume_sended_videos(event, chat_id, pytgcalls)
    
# Stop the bot
@client.on(events.NewMessage(pattern="/اغلق"))
async def stop_bot(event):
    
    chat_id = event.chat_id
    
    # Check if the user bot is active in this group
    if chat_id not in active_groups:
        await event.reply("⚠️ البوت غير مفعل في هذه المجموعة! استخدم `/ابدا` أولًا.")
        return
    
    # Check if the user is an admin
    if not await is_admin(event):
        await event.reply("🚫 فقط المشرفين يمكنهم استخدام هذا الأمر!")
        return
    
    # Stopping the bot and leaving the chat voice
    if chat_id in active_groups:
        active_groups.remove(chat_id)
        await pytgcalls.leave_call(chat_id)
        
    await event.reply("⛔ البوت متوقف الآن!")
    return

async def main():   
    await client.connect()
     
    # Running the bot
    print("User bot is running...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())