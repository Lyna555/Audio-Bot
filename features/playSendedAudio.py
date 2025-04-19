import os
import uuid

SAVE_FOLDER = "./audios"
os.makedirs(SAVE_FOLDER, exist_ok=True)

async def play_sended_audio(event, chat_id, pytgcalls):
    
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