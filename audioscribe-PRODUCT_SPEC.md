# Audio Scribe - Product Specification

**Repository:** `audioscribe`  
**Filename:** `audioscribe-PRODUCT_SPEC.md`  
**Last Updated:** 2026-02-16 at 15:10 UTC

---

## What This Is

**Audio Scribe** - Audio transcription with speaker diarization

## Who It's For

**Primary Users:** Content creators, researchers, meeting facilitators

## Tech Stack

Python, audio processing, speaker identification

---

## Core Features

The following features have been implemented based on development sessions:

1. - Added comprehensive debug logging showing model, language, device, diarization status, HF token presence
2. - Added logs at each stage: "Speaker ID skipped", "Diarize segments: N found"
3. - Added monkey-patch in audioscribe_windows.py that re-creates missing AudioMetaData class and list_audio_backends function
4. - Added requirements.txt for one-command install
5. 10. Removed os, sys, time; added shutil for ffmpeg detection
6. 3. Added _get_model() with module-level cache - Same model/settings = instant reuse instead of reloading from disk
7. 4. Added gr.Progress() updates - Shows progress bar at each stage (Loading model â†’ Transcribing â†’ Aligning â†’ Identifying speakers â†’ Saving)
8. 5. Added check_ffmpeg() using shutil.which() - Clear install message if missing, startup warning in console
9. 7. Added DOWNLOADS.mkdir(exist_ok=True) before writing transcript
10. 9. Added explicit del align_model, del diarize_model after use
11. Added. Your CLAUDE.md now includes 5 new sections:
12. Added. Your global CLAUDE.md now includes:
13. Also my token should not be out there on the internet... it rebuilt with the token included.
14. Claude: Created global Claude code instructions file
15. Created PROJECT_STATUS.md - Documented project state and quick start
16. Created Python virtual environment (.venv/)
17. Created audioscribe_mac.py - Full transcription app with Gradio web UI
18. Created audioscribe_mac.py with all features from the README:
19. Done. Your global CLAUDE.md file is now created at /home/user/.claude/CLAUDE.md.
20. Fix: Added app.queue() before app.launch() - required for gr.Progress() in Gradio 3.50.2
21. Fixed Gradio queue error - Added .queue() for progress tracking support
22. Python 3.14 is too new - many packages (pillow, numpy) don't have pre-built wheels for it yet
23. The virtual environment was created in my sandbox environment, not on your Mac. Let me give you the commands to set it up on your machine:
24. Updated README.md - Added correct dependency versions and Python version notes
25. [Created AudioScribe_Windows.bat - double-click launcher]

---

## Technical Implementation

Key technical details from implementation:

- - Added monkey-patch in audioscribe_windows.py that re-creates missing AudioMetaData class and list_audio_backends function
- What happened: WhisperX uses ctranslate2 under the hood, which only supports CUDA (NVIDIA) and CPU. Apple's MPS GPU isn't supported yet. The fix falls back to CPU on Mac.
- Corrected MPS note (not supported, uses CPU)
- The whisperx API uses a different parameter name. Let me check and fix:
- Fixed. whisperx uses hf_token as the parameter name. Pull and try again:
- Speaker diarization: Uses hf_token=hf_token parameter
- Gradio: Uses .queue().launch() for progress tracking

---

## Architecture & Design Decisions

Key decisions made during development:

- All clean - PDF covers: what AudioScribe does, architecture, dependencies, all 3 known issues, correct setup steps (Python 3.11, venv, gradio==3.50.2, FFmpeg), and what to do next.


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

**Never manually edit this file** - it's maintained automatically from session notes.

