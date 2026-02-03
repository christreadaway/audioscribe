# AudioScribe - Project Status

## Overview
Local audio transcription application with optional speaker identification. Runs entirely on your computer with no cloud dependencies.

## Current Status: **Working**

The macOS version is fully functional and tested on Apple Silicon (M-series) Macs.

## Completed Features
- [x] WhisperX-based transcription engine
- [x] Gradio web interface (http://127.0.0.1:7860)
- [x] 21 language support with auto-detection
- [x] Multiple model sizes (tiny, base, small, medium, large-v2, large-v3)
- [x] Optional speaker diarization via pyannote.audio
- [x] Transcripts saved to Downloads folder
- [x] HuggingFace token management for speaker identification

## Files
| File | Description |
|------|-------------|
| `audioscribe_mac.py` | Main application for macOS |
| `README.md` | User documentation and setup instructions |
| `PROJECT_STATUS.md` | This file - project status tracker |
| `.gitignore` | Git ignore patterns for Python projects |
| `LICENSE` | MIT License |

## Dependencies
- Python 3.11 (recommended; 3.9-3.12 supported)
- torch==2.2.0
- torchaudio==2.2.0
- whisperx
- gradio==3.50.2

## Known Issues / Notes
- **MPS (Apple GPU) not supported** - ctranslate2/whisperx doesn't support Apple's Metal GPU yet; runs on CPU
- Python 3.13+ not yet supported (dependency compatibility issues)
- Latest torch/torchaudio versions have breaking changes with pyannote.audio; pinned to 2.2.0
- Large models (medium, large-v2/v3) are slower on CPU but still work

## Fixes Applied (2026-02-03)
| Issue | Fix |
|-------|-----|
| MPS device error | Fall back to CPU (ctranslate2 doesn't support MPS) |
| Gradio progress tracking error | Added `.queue()` before `.launch()` |
| Speaker diarization auth error | Changed `use_auth_token` to `token` for newer huggingface_hub |

## Quick Start (macOS)
```bash
cd ~/audioscribe
git pull origin claude/setup-audioscribe-mac-26c4P
python3.11 -m venv .venv
source .venv/bin/activate
pip install torch==2.2.0 torchaudio==2.2.0
pip install whisperx gradio==3.50.2
python audioscribe_mac.py
```

## Repository
https://github.com/christreadaway/audioscribe

Branch: `claude/setup-audioscribe-mac-26c4P`

## Last Updated
2026-02-03
