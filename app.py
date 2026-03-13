import gradio as gr
import yt_dlp
import os
import re  # 💡 新增：引入正则表达式库，用来提取隐藏在文字中的链接
from faster_whisper import WhisperModel

print("🤖 正在初始化 AI 模型，请稍候...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("✅ 模型准备就绪！")


def extract_url(text):
    """💡 新增辅助函数：用正则表达式从杂乱的文本中提取网址"""
    # 查找以 http:// 或 https:// 开头，直到遇到空格或换行符为止的字符串
    match = re.search(r'(https?://[^\s]+)', text)
    if match:
        return match.group(1)
    return text  # 如果没找到，就原样返回，交由后面的代码去报错


def process_video(raw_input):
    if not raw_input:
        return "请先输入一个有效的视频链接哦！", ""

    # 💡 优化点 2：清洗输入，提取纯净的 URL
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
        print(f"📥 正在下载音频...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"❌ 下载失败，可能是链接不正确。错误信息: {e}", ""

    if not os.path.exists(temp_audio):
        return "❌ 找不到音频文件，提取失败了。", ""

    print("🧠 正在进行 AI 语音识别...")
    try:
        # 💡 增加 initial_prompt，用一段简体中文文本作为“引子”，强制模型输出简体字
        segments, info = model.transcribe(
            temp_audio,
            beam_size=5,
            initial_prompt="以下是一段简体中文的普通话句子。"
        )

        # 💡 优化点 1：准备两个不同的字符串变量来分别存储结果
        text_with_timestamps = f"识别语言: {info.language}\n" + "=" * 30 + "\n"
        pure_text = ""

        for segment in segments:
            # 拼接带时间轴的版本
            text_with_timestamps += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            # 拼接纯文本版本
            pure_text += segment.text

        # 注意：这里我们 return 了两个值，对应 Gradio 界面的两个输出框
        return text_with_timestamps, pure_text

    except Exception as e:
        return f"❌ 识别失败，错误信息: {e}", ""


# --- 搭建网页前端界面 ---
demo = gr.Interface(
    fn=process_video,
    inputs=gr.Textbox(label="输入B站视频分享内容 (支持直接粘贴App里的长段落)", lines=3),
    # 💡 优化界面：将 outputs 改成一个列表，包含两个文本框
    outputs=[
        gr.Textbox(label="带时间轴的提取结果 (方便对位)", lines=12),
        gr.Textbox(label="纯文本提取结果 (方便直接阅读和复制)", lines=12)
    ],
    title="🎙️ B站视频语音提取器 Pro",
    description="只需粘贴分享链接（自带多余文字也不怕），AI 自动为你提取双版本文本。"
)

if __name__ == "__main__":
    demo.launch()