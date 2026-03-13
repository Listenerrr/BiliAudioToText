import gradio as gr
import yt_dlp
import os
import re
from faster_whisper import WhisperModel

print("🤖 正在初始化 AI 模型，请稍候...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("✅ 模型准备就绪！")


def extract_url(text):
    match = re.search(r'(https?://[^\s]+)', text)
    if match:
        return match.group(1)
    return text


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"


# 💡 新增：在参数里加上 progress=gr.Progress()，激活 Gradio 的进度条功能
def process_video(raw_input, progress=gr.Progress()):
    if not raw_input:
        return "请先输入一个有效的视频链接哦！", "", None, None

    # 💡 进度条：10%
    progress(0.1, desc="🔍 正在解析并清洗链接...")
    url = extract_url(raw_input)
    print(f"🔗 实际解析到的链接为: {url}")

    temp_audio = "temp_audio.mp3"
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }

    try:
        # 💡 进度条：30%
        progress(0.3, desc="📥 正在从 B 站提取最高音质音频...")
        print(f"📥 正在下载音频...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"❌ 下载失败，可能是链接不正确。错误信息: {e}", "", None, None

    if not os.path.exists(temp_audio):
        return "❌ 找不到音频文件，提取失败了。", "", None, None

    print("🧠 正在进行 AI 语音识别...")
    try:
        # 💡 进度条：60%
        progress(0.6, desc="🧠 音频下载完成！AI 正在努力听写中（这步最耗时）...")
        segments, info = model.transcribe(
            temp_audio,
            beam_size=5,
            initial_prompt="以下是一段简体中文的普通话句子。"
        )

        # 💡 进度条：90%
        progress(0.9, desc="📝 听写完成！正在排版并生成字幕文件...")
        text_with_timestamps = f"识别语言: {info.language}\n" + "=" * 30 + "\n"
        pure_text = ""
        srt_content = ""
        segment_index = 1

        for segment in segments:
            text_with_timestamps += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            pure_text += segment.text

            start_time = format_time(segment.start)
            end_time = format_time(segment.end)
            srt_content += f"{segment_index}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{segment.text.strip()}\n\n"
            segment_index += 1

        srt_filename = "提取结果_字幕.srt"
        txt_filename = "提取结果_纯文本.txt"

        with open(srt_filename, "w", encoding="utf-8") as f:
            f.write(srt_content)

        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(pure_text)

        # 💡 进度条：100%
        progress(1.0, desc="✅ 全部处理完毕！")
        return text_with_timestamps, pure_text, srt_filename, txt_filename

    except Exception as e:
        return f"❌ 识别失败，错误信息: {e}", "", None, None


# --- 搭建网页前端界面 ---
demo = gr.Interface(
    fn=process_video,
    inputs=gr.Textbox(label="输入B站视频分享内容 (支持直接粘贴App里的长段落)", lines=3),
    outputs=[
        gr.Textbox(label="带时间轴的提取结果 (方便对位)", lines=12),
        gr.Textbox(label="纯文本提取结果 (方便直接阅读和复制)", lines=12),
        gr.File(label="📥 下载 SRT 字幕文件 (可直接导入剪映/PR等剪辑软件)"),
        gr.File(label="📥 下载 TXT 纯文本文件")
    ],
    title="🎙️ B站视频语音提取器 Pro Max",
    description="只需粘贴分享链接，AI 自动为你提取双版本文本，并支持一键下载标准字幕文件！"
)

if __name__ == "__main__":
    demo.launch()