# AudioScribe - Project Status

> **Repository:** `github.com/christreadaway/audioscribe`
> **Category:** Product
> **Local Path:** `~/audioscribe/`

## Overall Progress: 90%

## What's Working
- Gradio web UI at http://127.0.0.1:7860
- Audio transcription via WhisperX (tiny through large-v3 models)
- **Batch file upload** — upload multiple files, process all sequentially (NEW)
- Tabbed UI: Single File + Batch Upload modes
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
- Batch upload — implemented, awaiting user testing on Windows

## Tech Stack
- Python 3.11, WhisperX, pyannote.audio 3.x, Gradio 3.50.2, ffmpeg
- CUDA on Windows, CPU on Mac
- See CLAUDE.md for full details

## Next Steps
1. User tests batch upload on Windows with real audio files
2. User tests speaker diarization on Windows with HF token
3. If working → merge branch to main
4. Pin pyannote.audio version in requirements.txt to prevent future breakage

## Blockers
- None — features are deployed, just need testing

## Last Session
- **Date:** 2026-02-26
- **Branch:** `claude/batch-file-upload-2gYSk`
- **Summary:** Added batch file upload feature to both Windows and Mac versions. Tabbed UI with Single File and Batch Upload modes. Each file processed sequentially with per-file progress tracking. All transcripts saved individually to ~/Downloads/.
