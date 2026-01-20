# AudioScribe

**Local audio transcription with optional speaker identification.**

Transcribe meetings, interviews, and voice memos entirely on your computer — no cloud services, no subscriptions, no data leaving your machine.

---

## Why AudioScribe?

| Problem | AudioScribe Solution |
|---------|---------------------|
| Cloud transcription services cost money | **Free and open source** |
| Privacy concerns with uploading audio | **Runs 100% locally** — nothing leaves your computer |
| Command-line tools are intimidating | **Simple web interface** — just upload and click |
| Hard to tell who said what | **Optional speaker identification** labels each speaker |

---

## Features

- **21 languages supported** — English, Spanish, French, German, Japanese, and more
- **Speaker identification** — Labels who said what (e.g., `[SPEAKER_00]: Hello...`)
- **Multiple transcription models** — Trade off speed vs. accuracy based on your hardware
- **Works offline** — No internet required after initial setup
- **Cross-platform** — macOS and Windows supported

---

## Quick Start

### macOS

**Requirements:** macOS 10.15+, Python 3.9+ (pre-installed on most Macs)

**Step 1: Create project folder and virtual environment**
```bash
mkdir ~/audioscribe
cd ~/audioscribe
python3 -m venv .venv
source .venv/bin/activate
```

**Step 2: Install dependencies**
```bash
pip install whisperx gradio==3.50.2
```

**Step 3: Download AudioScribe**

Download `audioscribe_mac.py` from this repository and save it to `~/audioscribe/`

**Step 4: Run**
```bash
cd ~/audioscribe && source .venv/bin/activate && python audioscribe_mac.py
```

Your browser will open to `http://127.0.0.1:7860` with the AudioScribe interface.

---

### Windows

**Requirements:** Windows 10/11, Python 3.11, FFmpeg

**Step 1: Install Python**
1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation

**Step 2: Install FFmpeg**
```cmd
winget install FFmpeg
```

**Step 3: Create project folder and virtual environment**
```cmd
mkdir %USERPROFILE%\audioscribe
cd %USERPROFILE%\audioscribe
py -3.11 -m venv .venv
.venv\Scripts\activate
```

**Step 4: Install dependencies**

*With NVIDIA GPU:*
```cmd
pip install torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118
pip install whisperx gradio==3.50.2
```

*Without NVIDIA GPU (CPU only):*
```cmd
pip install torch==2.5.1 torchaudio==2.5.1
pip install whisperx gradio==3.50.2
```

**Step 5: Download AudioScribe**

Download `audioscribe_windows.py` and `AudioScribe_Windows.bat` from this repository and save them to your `audioscribe` folder.

**Step 6: Run**

Double-click `AudioScribe_Windows.bat` or run:
```cmd
cd %USERPROFILE%\audioscribe
.venv\Scripts\activate
python audioscribe_windows.py
```

See [README_WINDOWS.md](README_WINDOWS.md) for detailed Windows instructions and troubleshooting.

---

## Usage

1. **Upload an audio file** — Supports .mp3, .wav, .m4a, .aac, .flac, .ogg, .wma
2. **Select language** — English is default, or choose auto-detect
3. **Choose a model** — Start with "tiny" (fastest and most reliable)
4. **Enable speaker identification** (optional) — Requires one-time Hugging Face setup
5. **Click Transcribe** — Watch the terminal for progress
6. **Find your transcript** — Saved to your Downloads folder as a .txt file

### Model Selection Guide

| Model | Speed | Accuracy | Hardware Needed |
|-------|-------|----------|-----------------|
| tiny | Fastest | Good | Any computer |
| base | Fast | Better | Any computer |
| small | Slower | Good | GPU recommended |
| medium | Slow | Great | GPU required |
| large-v2/v3 | Very slow | Best | GPU required |

**Recommendation:** Start with `tiny`. It works on any hardware and is surprisingly accurate for clear audio.

---

## Speaker Identification Setup

Speaker identification labels who said what in your transcript. It requires a free Hugging Face account and accepting the model terms.

**One-time setup:**

1. Create a free account at [huggingface.co/join](https://huggingface.co/join)
2. Create an access token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (select "Read" access)
3. Accept the model terms (while logged in):
   - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
   - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
4. Paste your token in AudioScribe and click Save

Your token is stored locally at `~/.audioscribe_token.txt` and never sent anywhere except Hugging Face for model authentication.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python: command not found` | Open a new terminal window, or reinstall Python with "Add to PATH" checked |
| `No module named whisperx` | Activate the virtual environment first: `source .venv/bin/activate` (Mac) or `.venv\Scripts\activate` (Windows) |
| Transcription freezes | Use the `tiny` or `base` model — larger models require a GPU |
| `ffmpeg: command not found` | Install FFmpeg: `winget install FFmpeg` (Windows) or `brew install ffmpeg` (Mac) |
| Speaker identification hangs | This can happen on long files. The basic transcript is already saved — you can Ctrl+C safely |

---

## File Locations

| What | macOS | Windows |
|------|-------|---------|
| Application | `~/audioscribe/` | `C:\Users\YourName\audioscribe\` |
| Transcripts | `~/Downloads/` | `C:\Users\YourName\Downloads\` |
| Saved token | `~/.audioscribe_token.txt` | `C:\Users\YourName\.audioscribe_token.txt` |
| Model cache | `~/.cache/huggingface/` | `C:\Users\YourName\.cache\huggingface\` |

---

## Third-Party Licenses

AudioScribe is built on these excellent open-source projects:

| Library | License | Link |
|---------|---------|------|
| WhisperX | BSD-4-Clause | [github.com/m-bain/whisperX](https://github.com/m-bain/whisperX) |
| OpenAI Whisper | MIT | [github.com/openai/whisper](https://github.com/openai/whisper) |
| pyannote.audio | MIT | [github.com/pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) |
| Gradio | Apache 2.0 | [github.com/gradio-app/gradio](https://github.com/gradio-app/gradio) |
| PyTorch | BSD | [pytorch.org](https://pytorch.org) |

Speaker identification requires accepting additional terms:
- [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)

---

## Support

If AudioScribe is useful to you, consider supporting development:

☕ [**Support on Patreon**](https://www.patreon.com/cw/christreadaway)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**v1.250120** · Made by [Chris Treadaway](https://www.patreon.com/cw/christreadaway)
