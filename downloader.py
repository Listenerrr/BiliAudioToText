import yt_dlp


def download_bilibili_audio(video_url):
    print(f"正在准备下载，目标链接: {video_url}")

    # 这里是给“搬运工” yt-dlp 下达的具体指令
    ydl_opts = {
        'format': 'bestaudio/best',  # 指令1：只要最好的音频，不要画面，省时间省流量
        'outtmpl': '%(title)s.%(ext)s',  # 指令2：下载下来的文件，自动用“视频原本的标题”来命名
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # 指令3：呼叫底层的 FFmpeg 来处理格式
            'preferredcodec': 'mp3',  # 指令4：统一转换成通用的 mp3 格式
            'preferredquality': '192',  # 指令5：设置一下音质
        }],
    }

    try:
        # 开始执行下载任务
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("\n🎉 太棒了！音频下载并转换成功，快去左侧目录看看吧！")
    except Exception as e:
        print(f"\n❌ 哎呀，下载遇到了问题，错误信息是: {e}")


# ---------- 下面是测试运行区域 ----------
if __name__ == "__main__":
    # 这里我随便放了一个 B 站经典的视频链接作为测试（你可以换成任意你想测的 B 站视频）
    test_url = "https://www.bilibili.com/video/BV1GJ411x7h7"

    # 调用上面写好的函数
    download_bilibili_audio(test_url)