# Audio Scribe - Product Specification

**Repository:** `audioscribe`
**Filename:** `audioscribe-PRODUCT_SPEC.md`
**Last Updated:** 2026-02-26

---

## What This Is

**Audio Scribe** — Local audio transcription with speaker diarization. No data leaves your machine.

## Who It's For

**Primary Users:** Content creators, researchers, meeting facilitators, anyone who needs audio-to-text locally.

## Tech Stack

- **Language:** Python 3.11
- **Transcription:** WhisperX (ctranslate2 backend)
- **Speaker ID:** pyannote.audio 3.x (requires HuggingFace token)
- **UI:** Gradio 3.50.2 web interface (http://127.0.0.1:7860)
- **Audio:** ffmpeg (must be installed)
- **GPU:** CUDA on Windows, CPU fallback on Mac (MPS NOT supported by ctranslate2)

---

## Core Features

### Audio Transcription
- WhisperX-powered local transcription — no cloud, no data sharing
- Model sizes: tiny, base, small, medium, large-v2, large-v3
- 21 languages + auto-detect
- Timestamp alignment via WhisperX alignment models

### Batch File Upload
- Upload multiple audio files at once via the "Batch Upload" tab
- Files processed sequentially — queue up overnight jobs
- Per-file progress tracking in the UI progress bar
- Each file gets its own transcript saved to ~/Downloads/
- Combined output view with clear file-by-file headers
- Supports any audio format FFmpeg can decode (MP3, WAV, M4A, AAC, FLAC, OGG, WMA, WEBM, MP4, etc.)
- One bad file doesn't stop the batch — errors reported per-file

### Speaker Identification (Diarization)
- Identifies who said what using pyannote.audio
- Requires free HuggingFace account + token
- Version-aware patching: works with both pyannote 3.x and 4.x
- Direct pyannote.audio calls (bypasses whisperx wrapper for reliability)
- Token saved locally at ~/.audioscribe_token.txt

### User Interface
- Gradio web UI with Soft theme
- Tabbed input: Single File (with audio preview) and Batch Upload
- Language selection dropdown (21 languages + auto-detect)
- Model size selector with guidance
- Speaker ID toggle with collapsible token settings
- Progress bar with stage descriptions
- Transcript output with copy button (Mac)
- Auto-save to ~/Downloads/ with timestamps

### Performance & Reliability
- Model caching between transcriptions (reuses loaded model)
- CUDA GPU acceleration on Windows, CPU fallback on Mac
- torch.load patching for PyTorch 2.6+ compatibility
- torchaudio AudioMetaData/list_audio_backends shims for torchaudio 2.8+
- FFmpeg detection with helpful install messages
- Startup diagnostics (checks all dependencies)
- Comprehensive error handling with user-friendly messages

---

## Architecture & Design Decisions

- **Two platform files:** `audioscribe_windows.py` (comprehensive, with compat patches) and `audioscribe_mac.py` (simpler)
- **Windows launcher:** `AudioScribe_Windows.bat` for double-click desktop launch
- **Batch via reuse:** `transcribe_batch()` reuses `transcribe()` per-file via `_BatchProgress` wrapper — zero code duplication
- **Pyannote patching:** Runtime version detection + monkey-patching of 4 pyannote entry points for token parameter compatibility
- **No cloud dependency:** Everything runs locally. HF token only needed for speaker ID model download.

---

## Development History

Full session-by-session development history is maintained in `SESSION_NOTES.md`.

This specification is automatically updated alongside session notes to reflect:
- New features implemented
- Technical decisions made
- Architecture changes
- Integration updates

---

## Updating This Spec

At the end of each Claude Code session, this spec is updated automatically when you say:
> "Append session notes to SESSION_NOTES.md"

Claude will:
1. Update `SESSION_NOTES.md` with detailed session history
2. Update `audioscribe-PRODUCT_SPEC.md` with new features/decisions
3. Commit both files together

**Never manually edit this file** — it's maintained automatically from session notes.
