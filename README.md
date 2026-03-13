# 🎙️ Bilibili 视频语音提取器

基于 Python 构建的本地自动化全栈工具。整合 `yt-dlp` 与 OpenAI 的 `faster-whisper` 模型，只需输入 B 站视频分享链接，即可一键将视频语音自动提取、识别并导出为带时间轴的标准字幕文件和纯文本。

## ✨ 核心功能

* **🔗 智能链接解析**：支持直接粘贴 B 站 App 复制的长段落分享文本，自动利用正则提取有效 URL。
* **📥 高效音频提取**：底层调用 `yt-dlp` 与 `FFmpeg`，跳过视频画面，直取最高音质音频流，节省时间和带宽。
* **🧠 本地 AI 识别**：接入 `faster-whisper` 本地大模型，无需联网调用 API，保护隐私且免费。通过 Prompt 锚定，强制精准输出简体中文。
* **📝 双轨格式输出**：前端界面同时展示“带时间轴文本”与“纯文本”，满足对位和阅读的双重需求。
* **💾 一键文件导出**：支持将识别结果直接下载为标准 `.srt` 字幕文件（可无缝导入 PR、剪映等专业软件）和 `.txt` 文本文件。
* **⏳ 实时进度追踪**：优化的 Gradio 交互界面，提供从下载到识别的全阶段动态进度条展示，告别长视频等待焦虑。

## 🛠️ 技术栈

* **后端逻辑**: Python 3.11
* **音视频处理**: FFmpeg, yt-dlp
* **AI 语音识别**: faster-whisper (Base 模型)
* **前端 Web UI**: Gradio

## 🚀 快速开始

### 1. 环境准备
* 确保你的电脑已安装 **Python 3.10+**。
* **必须安装 FFmpeg** 并已将其配置到系统的环境变量中（用于底层的音视频格式转换）。

### 2. 克隆项目与安装依赖
在终端中运行以下命令克隆本项目并安装核心依赖：

```bash
git clone [https://github.com/Listenerrr/BiliAudioToText.git](https://github.com/你的GitHub用户名/BiliAudioToText.git)
cd BiliAudioToText

# 建议在虚拟环境中运行
pip install yt-dlp faster-whisper gradio
3. 运行程序
在项目根目录运行主程序：

Bash
python app.py
终端出现 Running on local URL:  http://127.0.0.1:7860 后，点击链接即可在浏览器中打开可视化界面使用。

💡 使用提示
初次运行程序时，faster-whisper 会自动从外网下载 AI 模型文件（几十 MB），请保持网络畅通并耐心等待。

程序运行时会在本地生成 temp_audio.mp3 作为临时处理文件，每次执行新任务时会自动覆盖，不会占用过多磁盘空间。