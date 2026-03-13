import gradio as gr
import yt_dlp
import os
from faster_whisper import WhisperModel

# 1. 全局加载 AI 模型（放在最外面，这样每次转换就不用重新加载模型了，速度更快）
print("🤖 正在初始化 AI 模型，请稍候...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("✅ 模型准备就绪！")


def process_video(url):
    """这是处理视频的核心流水线函数"""
    if not url:
        return "请先输入一个有效的视频链接哦！"

    # 固定一个临时文件名，每次处理新视频时覆盖旧的，防止硬盘塞满
    temp_audio = "temp_audio.mp3"
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    # --- 第一步：下载音频 ---
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True  # 隐藏下载时满屏的代码输出，让后台干净一点
    }

    try:
        print(f"📥 正在下载音频: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"❌ 下载失败，可能是链接不正确或触发了反爬机制。错误信息: {e}"

    # --- 第二步：语音转文字 ---
    if not os.path.exists(temp_audio):
        return "❌ 找不到音频文件，提取失败了。"

    print("🧠 正在进行 AI 语音识别...")
    try:
        segments, info = model.transcribe(temp_audio, beam_size=5)

        result_text = f"识别语言: {info.language}\n" + "=" * 30 + "\n"
        for segment in segments:
            result_text += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"

        return result_text
    except Exception as e:
        return f"❌ 识别失败，错误信息: {e}"


# --- 第三步：搭建网页前端界面 ---
# 这里利用 Gradio 快速生成 UI，完全不需要写 HTML
demo = gr.Interface(
    fn=process_video,  # 绑定我们上面写的流水线函数
    inputs=gr.Textbox(label="输入B站视频链接 (例如: https://www.bilibili.com/video/BV...)", lines=2),
    outputs=gr.Textbox(label="提取的文字结果", lines=15),
    title="🎙️ B站视频语音提取器",
    description="只需粘贴链接，AI 自动为你提取并生成带时间轴的文本。",
)

if __name__ == "__main__":
    # 启动网页服务
    demo.launch()