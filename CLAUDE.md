# Claude Code Instructions - AudioScribe

## About This Project
Local audio transcription app with speaker diarization (identifying who said what). Uses WhisperX for transcription and pyannote.audio for speaker identification. Gradio web UI. Runs on Mac (CPU) and Windows (CUDA GPU). Saves transcripts to ~/Downloads/.

## About Me (Chris Treadaway)
Product builder, not a coder. I bring requirements and vision — you handle implementation.

**Working with me:**
- Bias toward action — just do it, don't argue
- Make terminal commands dummy-proof (always start with `cd ~/audioscribe`)
- Minimize questions — make judgment calls and tell me what you chose
- I get interrupted frequently — always end sessions with clear handoff

## Tech Stack
- **Language:** Python 3.11
- **Transcription:** WhisperX (ctranslate2 backend)
- **Speaker ID:** pyannote.audio 3.x (requires HuggingFace token)
- **UI:** Gradio web interface (http://127.0.0.1:7860)
- **Audio:** ffmpeg (must be installed)
- **GPU:** CUDA on Windows, CPU fallback on Mac (MPS NOT supported by ctranslate2)

## File Paths
- **Always use:** `~/audioscribe/`
- **Never use:** `/Users/christreadaway/...`
- **Always start commands with:** `cd ~/audioscribe`
- **Transcripts saved to:** `~/Downloads/`

## PII Rules
❌ NEVER include: HuggingFace tokens, API keys, real speaker names in code, file paths with /Users/christreadaway → use ~/
✅ Token stored locally at `~/.audioscribe_token.txt` — never committed

## Critical Technical Notes
- **torch versions MUST be pinned:** torch==2.5.1, torchaudio==2.5.1 on Windows; torch==2.2.0, torchaudio==2.2.0 on Mac
- **MPS (Apple GPU) is NOT supported** — always fall back to CPU on Mac
- **Speaker diarization parameter:** Use `hf_token=` (not `use_auth_token=` or `token=`)
- **Gradio requires:** `app.queue().launch()` for progress tracking
- **Model caching:** Use module-level cache to avoid reloading on every transcription
- **Windows has separate script:** audioscribe_windows.py with torchaudio monkey-patch

## Key Features
- 21 languages supported + auto-detect
- Model sizes: tiny → large-v3
- Speaker identification with voice signatures
- Progress bar feedback during transcription
- Collapsible HuggingFace token input
- Transcripts auto-saved to Downloads with timestamps

## Git Branch Strategy
- Claude Code creates new branch per session
- Merge to main when stable
- Delete merged branches immediately

## Session End Routine

At the end of EVERY session — or when I say "end session" — do ALL of the following:

### A. Update SESSION_NOTES.md
Append a detailed entry at the TOP of SESSION_NOTES.md (most recent first) with: What We Built, Technical Details, Current Status (✅/❌/🚧), Branch Info, Decisions Made, Next Steps, Questions/Blockers.

### B. Update PROJECT_STATUS.md
Overwrite PROJECT_STATUS.md with the CURRENT state of the project — progress %, what's working, what's broken, what's in progress, next steps, last session date/summary. This is a snapshot, not a log.

### C. Commit Both Files
```
git add SESSION_NOTES.md PROJECT_STATUS.md
git commit -m "Session end: [brief description of what was done]"
git push
```

### D. Tell the User
- What branch you're on
- Whether it's ready to merge to main (and if not, why)
- Top 3 next steps for the next session

---
Last Updated: February 16, 2026
