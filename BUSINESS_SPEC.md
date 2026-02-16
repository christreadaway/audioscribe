# AudioScribe — Business Product Spec
**Version:** 2.0 | **Date:** 2026-02-16 | **Repo:** github.com/christreadaway/audioscribe

---

## 1. Problem Statement
Audio transcription services are either expensive (Otter.ai, Rev), require internet connectivity, or don't identify individual speakers. Professionals who record meetings, interviews, and classes need accurate transcripts with speaker labels ("Speaker 1 said X, Speaker 2 said Y") to create usable meeting notes. Existing free tools produce wall-of-text transcripts without speaker distinction, making them unusable for multi-person conversations.

## 2. Solution
A local-first audio transcription application using WhisperX for speech-to-text and pyannote for speaker diarization. Runs entirely on the user's computer — no cloud dependency, no subscription, no data leaving the machine. Provides a simple Gradio web interface where users upload audio, select options, and download labeled transcripts.

## 3. Target Users
- **Meeting Facilitators** — Transcribe team meetings with speaker attribution
- **Teachers / Professors** — Transcribe class recordings with student identification
- **Journalists / Researchers** — Interview transcription with speaker labels
- **Content Creators** — Podcast and video transcription
- **Anyone recording conversations** — Local, private, free alternative to cloud transcription services

## 4. Core Features

### Transcription Engine
- **WhisperX** — OpenAI Whisper variant optimized for word-level timestamps
- **21 Languages** — English, Spanish, French, German, Chinese, Japanese, and 15 more, plus auto-detect
- **Model Sizes** — tiny, base, small, medium, large-v3 (trade speed vs. accuracy)
- **Word-Level Alignment** — Precise timestamps for each word

### Speaker Diarization
- **pyannote 3.1** — State-of-the-art speaker identification
- **Automatic Speaker Count** — Detects number of speakers without manual input
- **Speaker Labels** — Transcript segments tagged with "Speaker 1", "Speaker 2", etc.
- **Voice Signatures** — Stores speaker voice profiles for cross-session identification
- **HuggingFace Token Required** — Free account needed; must accept pyannote model terms

### User Interface (Gradio)
- **File Upload** — Drag-and-drop audio files (MP3, WAV, M4A, etc.)
- **Speaker ID Toggle** — Checkbox to enable/disable diarization (ON by default)
- **Model Selection** — Dropdown for model size
- **Language Selection** — Dropdown with auto-detect option
- **Progress Bar** — Real-time stage updates (Loading model → Transcribing → Aligning → Identifying speakers → Saving)
- **Token Input** — Collapsible accordion for HuggingFace token entry

### Performance Optimizations
- **Model Caching** — Same model/settings reuse cached instance (no reload on repeat transcriptions)
- **GPU Support** — CUDA acceleration when available; graceful fallback to CPU
- **MPS Handling** — Apple Silicon MPS detected but falls back to CPU (not fully supported by WhisperX)

### Output
- **Transcript Files** — Saved to ~/Downloads/ with timestamps
- **Speaker-Labeled Format** — Each segment shows speaker, timestamp, and text
- **Debug Logging** — Console shows model, language, device, diarization status, HF token presence

## 5. Tech Stack
- **Language:** Python 3.10+
- **Transcription:** WhisperX (OpenAI Whisper variant)
- **Diarization:** pyannote.audio 3.1 via HuggingFace
- **UI:** Gradio 3.50+
- **ML Framework:** PyTorch 2.5.1 + torchaudio 2.5.1 (pinned for compatibility)
- **Audio:** ffmpeg (required system dependency)
- **Platforms:** Windows (primary), macOS (CPU mode)

## 6. Data & Privacy
- **100% Local** — No audio data ever leaves the user's machine
- **No Cloud Dependency** — Models downloaded once, run offline thereafter
- **No Account Required** — Only HuggingFace token for diarization (free)
- **Transcripts stored locally** — ~/Downloads/ folder

## 7. Current Status
- **Working:** Transcription on Windows with GPU acceleration
- **Working:** Speaker diarization with pyannote 3.1
- **Working:** Gradio web interface with progress tracking
- **Working:** Model caching for repeat transcriptions
- **Fixed:** HuggingFace auth parameter (use_auth_token → token → hf_token)
- **Fixed:** torchaudio compatibility (pinned to 2.5.1, monkey-patch for AudioMetaData)
- **Fixed:** Gradio queue requirement for progress bars
- **Platform Files:** audioscribe_windows.py (primary), audioscribe_mac.py (secondary)
- **Desktop Shortcut:** Windows batch file (AudioScribe_Windows.bat) created

## 8. Business Model
- **Free / Open Source** — Core transcription tool
- **Patreon Support** — Voluntary donations for continued development
- **Launch Sequence:** 2 Patreon posts (done), one-time donation option, then push to GitHub public

## 9. Success Metrics
- Successful transcriptions with speaker identification
- Patreon supporters
- GitHub stars and community contributions
- Accuracy of speaker diarization across different audio qualities

## 10. Open Questions / Next Steps
- Voice signature persistence across sessions (currently per-session)
- Batch transcription mode (process multiple files)
- Real-time transcription (live microphone input)
- Integration with ParentPoint (transcribe parent-teacher conferences)
- macOS Apple Silicon native support (currently CPU-only fallback)
- Cloud-hosted option for users who can't run locally
