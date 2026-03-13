from faster_whisper import WhisperModel


def audio_to_text(audio_file_path):
    print("🤖 正在加载 AI 语音大模型，请稍候...")
    print("   (注意：第一次运行会自动从外网下载模型文件，大概几十到几百MB，请耐心等待)")

    # 核心指令 1：初始化大模型。
    # 我们先使用 "base" 基础模型测试，它体积小、速度快。
    # device="cpu" 保证在任何电脑上都能运行。compute_type="int8" 可以降低内存占用。
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print(f"\n🎧 模型加载完毕！开始倾听并识别音频：{audio_file_path}")

    # 核心指令 2：让模型开始听写
    segments, info = model.transcribe(audio_file_path, beam_size=5)

    print(f"💡 检测到音频语言为: {info.language} (准确率: {info.language_probability:.2f})")
    print("-" * 40)

    # 核心指令 3：逐句输出识别到的文字
    full_text = ""
    for segment in segments:
        # segment.start 和 end 代表这句话在视频里的开始和结束时间
        line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
        print(line)
        full_text += segment.text + "\n"

    print("-" * 40)
    print("✅ 识别全部完成！")
    return full_text


# ---------- 下面是测试运行区域 ----------
if __name__ == "__main__":
    # ⚠️ 重要提示：请把下面双引号里的内容，替换成你刚才实际下载的 mp3 文件的名字！
    # 如果文件和代码在同一个目录下，直接写文件名；如果在 downloads 文件夹里，就写 "downloads/你的文件名.mp3"
    test_audio = "【官方 MV】Never Gonna Give You Up - Rick Astley.mp3"

    audio_to_text(test_audio)