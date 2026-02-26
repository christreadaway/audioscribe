# AudioScribe - Project Status

> **Repository:** `github.com/christreadaway/audioscribe`
> **Category:** Product
> **Local Path:** `~/audioscribe/`

## Overall Progress: 90%

## What's Working
- Gradio web UI at http://127.0.0.1:7860
- Audio transcription via WhisperX (tiny through large-v3 models)
- **Batch file upload** — upload multiple files, process all sequentially
- Tabbed UI: Single File + Batch Upload modes
- Dark mode default (via JS injection)
- Version number displayed in header (v2.1.0)
- Stale-server auto-kill on startup (Windows)
- 21 languages + auto-detect
- Timestamp alignment
- Model caching between transcriptions (works across batch files too)
- HF token save/load from `~/.audioscribe_token.txt`
- Transcript auto-save to ~/Downloads/ (per-file in batch mode)
- Progress bar feedback (per-file progress in batch mode)
- FFmpeg detection with helpful error messages
- torch.load patching for PyTorch 2.6+ compatibility
- torchaudio AudioMetaData/list_audio_backends shims
- Startup diagnostics

## What's Broken
- Nothing confirmed broken

## What's In Progress
- Speaker diarization — comprehensive fix deployed, awaiting Windows testing
- Batch upload — implemented, **user seeing old cached page in browser** — needs hard refresh (Ctrl+Shift+R) after relaunch

## Tech Stack
- Python 3.11, WhisperX, pyannote.audio 3.x, Gradio 3.50.2, ffmpeg
- CUDA on Windows, CPU on Mac
- See CLAUDE.md for full details

## Next Steps
1. User double-clicks desktop icon, then hard-refreshes browser (Ctrl+Shift+R) to see v2.1.0 UI with tabs
2. User tests batch upload on Windows with real audio files
3. User tests speaker diarization on Windows with HF token
4. If working → merge branch to main

## Blockers
- Browser cache was serving old page — hard refresh required after relaunch

## Last Session
- **Date:** 2026-02-26
- **Branch:** `claude/batch-file-upload-2gYSk`
- **Summary:** Debugged why user wasn't seeing batch upload UI. Root cause: old Gradio server process was holding port 7860 (or browser cache). Added stale-server auto-kill, dark mode, version display. Confirmed code on disk is correct (v2.1.0 with tabs). User needs to relaunch app and hard-refresh browser.
