# AudioScribe - Project Status

> **Repository:** `github.com/christreadaway/audioscribe`
> **Category:** Product
> **Local Path:** `~/audioscribe/`

## Overall Progress: 85%

## What's Working
- Gradio web UI at http://127.0.0.1:7860
- Audio transcription via WhisperX (tiny through large-v3 models)
- 21 languages + auto-detect
- Timestamp alignment
- Model caching between transcriptions
- HF token save/load from `~/.audioscribe_token.txt`
- Transcript auto-save to ~/Downloads/
- Progress bar feedback
- FFmpeg detection with helpful error messages
- torch.load patching for PyTorch 2.6+ compatibility
- torchaudio AudioMetaData/list_audio_backends shims
- Startup diagnostics

## What's Broken
- Nothing confirmed broken — previous token mismatch errors should be resolved

## What's In Progress
- Speaker diarization (pyannote.audio) — comprehensive version-aware fix deployed, awaiting user testing on Windows
- Branch: `claude/debug-speaker-identification-S0sic`

## Tech Stack
- Python 3.11, WhisperX, pyannote.audio 3.x, Gradio, ffmpeg
- CUDA on Windows, CPU on Mac
- See CLAUDE.md for full details

## Next Steps
1. User tests speaker diarization on Windows with real audio + HF token
2. If working → merge branch to main
3. Pin pyannote.audio version in requirements.txt to prevent future breakage

## Blockers
- None — fix is deployed, just needs testing

## Last Session
- **Date:** 2026-02-17
- **Branch:** `claude/debug-speaker-identification-S0sic`
- **Summary:** Comprehensive fix for pyannote/whisperx token parameter mismatch. Researched full API surface, patched all 4 pyannote entry points, replaced whisperx diarization wrapper with direct pyannote calls using version-aware token parameters.
