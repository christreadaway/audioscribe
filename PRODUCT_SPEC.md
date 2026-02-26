# AudioScribe — Product Specification

> **Version:** 2.1.0
> **Last Updated:** 2026-02-26
> **Repository:** `github.com/christreadaway/audioscribe`
> **Owner:** Chris Treadaway

---

## 1. Product Name & Problem Statement

**AudioScribe** is a local audio transcription app with speaker diarization (identifying who said what).

**Problem it solves:** Transcribing audio files — meetings, interviews, lectures, podcasts — is tedious and time-consuming. Cloud services like Otter.ai or Rev require uploading sensitive audio to third-party servers. AudioScribe runs 100% locally: no data leaves the user's machine, no subscriptions, no upload limits.

---

## 2. User Story

**Who:** A non-technical product builder (or anyone) who records meetings, interviews, or conversations and needs accurate written transcripts with speaker labels.

**What they're trying to accomplish:**
- Upload one or more audio files to a simple web UI
- Get an accurate transcript with timestamps and speaker labels
- Have transcripts auto-saved to their Downloads folder
- Do all of this locally, with no cloud dependency, on either Mac or Windows

**Key persona traits:**
- Not a coder — needs one-click launch (desktop shortcut / double-click)
- Often queues multiple files for overnight/unattended processing
- Needs clear feedback on progress and errors
- Values privacy — no audio should leave the machine

---

## 3. Core Functionality

### 3.1 Single-File Transcription
1. User opens browser to `http://127.0.0.1:7860`
2. On the **Single File** tab, user uploads one audio file via the audio widget (which shows a waveform preview)
3. User selects language (or Auto-detect), model size, and whether to identify speakers
4. User clicks **Transcribe**
5. Progress bar shows stages: Loading model → Transcribing → Aligning timestamps → Identifying speakers → Saving
6. Transcript appears in the right-hand panel with a copy button
7. Transcript is auto-saved to `~/Downloads/{filename}_{timestamp}.txt`

### 3.2 Batch File Upload
1. User switches to the **Batch Upload** tab
2. User uploads multiple audio files at once via file picker (multi-select)
3. User clicks **Transcribe All**
4. Files are processed sequentially — each file gets its own progress slice
5. Each file's transcript is saved individually to `~/Downloads/`
6. Combined output shows all transcripts with file-by-file headers
7. Summary line: "BATCH COMPLETE: X/Y files transcribed successfully"
8. One bad file does not stop the batch — errors are captured per-file

### 3.3 Speaker Identification (Diarization)
1. Requires a free Hugging Face token (stored locally at `~/.audioscribe_token.txt`)
2. User must accept model licenses on Hugging Face:
   - `pyannote/speaker-diarization-3.1`
   - `pyannote/segmentation-3.0`
3. When enabled, transcript output includes `[SPEAKER_00]`, `[SPEAKER_01]`, etc.
4. If token is missing or diarization fails, transcription continues without speaker labels (graceful degradation)

### 3.4 Model Selection
Six WhisperX model sizes available:
| Model | Speed | Accuracy | RAM/VRAM |
|-------|-------|----------|----------|
| tiny | Fastest | Good | ~1 GB |
| base | Fast | Better | ~1 GB |
| small | Moderate | Good | ~2 GB |
| medium | Slow | Very good | ~5 GB |
| large-v2 | Slowest | Excellent | ~10 GB |
| large-v3 | Slowest | Best | ~10 GB |

Default: **tiny** (works on any hardware).

### 3.5 Language Support
21 languages + Auto-detect:
English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Turkish, Polish, Swedish, Danish, Norwegian, Finnish, Greek, Czech

Default: **English**.

---

## 4. Inputs and Outputs

### Inputs
| Input | Type | Source | Notes |
|-------|------|--------|-------|
| Audio file(s) | File upload | User's local machine | Supported: mp3, wav, m4a, aac, flac, ogg, wma, webm, mp4 |
| Language | Dropdown | UI selection | 21 languages + Auto-detect |
| Model size | Dropdown | UI selection | tiny through large-v3 |
| Speaker ID toggle | Checkbox | UI selection | Default: enabled if token exists |
| HF token | Password text field | User input or `~/.audioscribe_token.txt` | Persisted locally, never committed to git |

### Outputs
| Output | Type | Destination | Notes |
|--------|------|-------------|-------|
| Transcript text | Text panel | Right column of UI | Copy button included |
| Saved transcript file | `.txt` file | `~/Downloads/{filename}_{timestamp}.txt` | One file per audio input |
| Progress bar | Visual indicator | UI | Shows current stage |
| Terminal diagnostics | Console text | Command prompt window | Model loading, segment counts, errors |

### Transcript Format (Windows version)
```
[SPEAKER_00]
Hello, welcome to the meeting.

[SPEAKER_01]
Thanks for having me.
```

### Transcript Format (Mac version)
```
[00:00 - 00:05] [SPEAKER_00]: Hello, welcome to the meeting.
[00:05 - 00:12] [SPEAKER_01]: Thanks for having me.
```

---

## 5. Business Rules and Logic

### Token Management
- IF `~/.audioscribe_token.txt` exists at startup → pre-fill token field, auto-enable speaker ID checkbox
- IF user clicks "Save Token" → write to `~/.audioscribe_token.txt`
- IF speaker ID is enabled but no token → show warning, continue transcription without speaker labels
- Token is NEVER committed to git or logged in full

### Model Caching
- IF same model size + device + language is requested → reuse cached model (no reload)
- IF different model requested → free previous model from memory, load new one
- IF GPU → clear CUDA cache between model swaps

### Error Handling
- IF FFmpeg not installed → show clear install instructions in transcript area
- IF audio file is corrupted → show error with suggestions
- IF GPU out of memory → suggest smaller model
- IF diarization fails → show warning banner, continue with plain transcript
- IF one file in batch fails → log error for that file, continue processing remaining files

### Compatibility Patches (applied at startup)
- `torch.load` patched to `weights_only=False` for PyTorch 2.6+ compatibility
- `torchaudio.AudioMetaData` shimmed if missing (torchaudio 2.8+)
- `torchaudio.list_audio_backends` shimmed if missing
- pyannote.audio token parameter normalized: `token=` vs `use_auth_token=` depending on pyannote version (3.x vs 4.x)
- Stale server on port 7860 auto-killed before launch (Windows)

### Platform-Specific Rules
| Rule | Windows | Mac |
|------|---------|-----|
| GPU | CUDA (NVIDIA) | CPU only (MPS not supported by ctranslate2) |
| torch version | 2.5.1 | 2.2.0 |
| torchaudio version | 2.5.1 | 2.2.0 |
| Compute type (GPU) | float16 | N/A |
| Compute type (CPU) | int8 | float32 |
| Batch size | 16 (GPU) / 4 (CPU) | 16 |
| Script | `audioscribe_windows.py` | `audioscribe_mac.py` |
| Launcher | `AudioScribe_Windows.bat` (desktop shortcut) | `python audioscribe_mac.py` |

---

## 6. Data Requirements

### Stored Locally
| Data | Location | Persistence |
|------|----------|-------------|
| HF token | `~/.audioscribe_token.txt` | Permanent until user deletes |
| Transcripts | `~/Downloads/{name}_{timestamp}.txt` | Permanent |
| WhisperX models | `~/.cache/huggingface/` (auto-downloaded) | Cached by HuggingFace hub |
| pyannote models | `~/.cache/huggingface/` (auto-downloaded) | Cached, requires HF token + license acceptance |

### Not Stored
- Audio files are processed in-place from temp uploads — not copied or retained
- No analytics, telemetry, or cloud calls (except HuggingFace model downloads on first use)
- No database

---

## 7. Integrations and Dependencies

### Runtime Dependencies
| Dependency | Purpose | Version Constraint |
|------------|---------|-------------------|
| Python | Runtime | 3.11 |
| WhisperX | Transcription engine (ctranslate2 backend) | Latest via pip |
| pyannote.audio | Speaker diarization | 3.x (version-aware patches handle 3.x vs 4.x) |
| Gradio | Web UI framework | 3.50.2 (pinned) |
| torch | ML framework | 2.5.1 (Windows) / 2.2.0 (Mac) |
| torchaudio | Audio loading | 2.5.1 (Windows) / 2.2.0 (Mac) |
| FFmpeg | Audio decoding (system install) | Any recent version |

### External Services
| Service | Purpose | Required? |
|---------|---------|-----------|
| Hugging Face Hub | Model downloads (first use only) | Yes (for models) |
| Hugging Face Token | Speaker diarization model access | Only for speaker ID |

### System Requirements
- **Windows:** NVIDIA GPU with CUDA recommended (CPU fallback available)
- **Mac:** Any Mac with Python 3.11 (CPU only — MPS not supported)
- **Both:** FFmpeg installed and on PATH
- **Disk:** ~1-10 GB for models depending on size chosen

---

## 8. Out of Scope (Not Building Now)

- Cloud deployment or hosted version
- Real-time / streaming transcription (live microphone input)
- Speaker name assignment (labels are SPEAKER_00, SPEAKER_01, etc. — no name mapping)
- Voice signature training / custom speaker profiles
- Audio editing or playback controls
- Translation (transcribes in original language only)
- Mobile app
- Multi-user / authentication
- Custom vocabulary or domain-specific fine-tuning
- Automatic language detection per-speaker in multilingual meetings
- Export formats beyond plain text (no SRT, VTT, DOCX, PDF)
- Electron or native desktop wrapper (runs as local web server + browser)

---

## 9. Open Design Questions

1. **Pin pyannote.audio version?** The 3.x → 4.x breaking change caused significant debugging. Should `requirements.txt` pin a specific pyannote version to prevent future breakage?

2. **Mac version parity:** The Mac version (`audioscribe_mac.py`) lacks several Windows-version improvements:
   - No model caching (reloads model every transcription)
   - No stale-server kill
   - No dark mode / version display
   - No pyannote version-aware patching
   - No torch.load / torchaudio compatibility shims
   - Should these be backported?

3. **Speaker name mapping:** Users currently see SPEAKER_00, SPEAKER_01. Should there be a UI to map these to real names post-transcription?

4. **Export formats:** Should we support SRT/VTT (subtitles), DOCX, or PDF export in addition to plain text?

5. **Concurrent batch processing:** Currently files are processed sequentially. On a machine with enough VRAM, could we process 2+ files in parallel?

6. **Auto-update mechanism:** Currently requires `git pull` to update. Should there be an in-app update check?

---

## 10. Success Criteria

### Must-Have (MVP — Complete)
- [x] User can upload a single audio file and get a transcript
- [x] User can upload multiple files and get all transcripts (batch mode)
- [x] Transcripts auto-saved to ~/Downloads with timestamps
- [x] Speaker labels appear when diarization is enabled and token is valid
- [x] Works on Windows with CUDA GPU
- [x] Works on Mac with CPU
- [x] One-click launch on Windows (desktop shortcut → .bat file)
- [x] Progress feedback during transcription
- [x] Graceful error messages (not raw Python tracebacks)

### Quality Bar
- [ ] Batch upload tested with 3+ real audio files on Windows
- [ ] Speaker diarization tested end-to-end on Windows with HF token
- [ ] No stale server issues — clean launch every time
- [ ] App starts in under 10 seconds (before model loading)

### Nice-to-Have (Future)
- [ ] Mac version has feature parity with Windows
- [ ] SRT/VTT subtitle export
- [ ] Speaker name mapping UI
- [ ] In-app model download progress indicator

---

## File Inventory

| File | Purpose |
|------|---------|
| `audioscribe_windows.py` | Main app — Windows version (v2.1.0) |
| `audioscribe_mac.py` | Main app — Mac version |
| `AudioScribe_Windows.bat` | Windows launcher (activates venv, starts app) |
| `requirements.txt` | Python dependencies |
| `CLAUDE.md` | Claude Code instructions (tech spec, session rules) |
| `PROJECT_STATUS.md` | Current project snapshot (overwritten each session) |
| `SESSION_NOTES.md` | Session history log (appended each session) |
| `PRODUCT_SPEC.md` | This file — full product specification |
| `.gitignore` | Excludes `__pycache__/`, `.venv/` |

---

## How to Rebuild From This Spec

A developer (or Claude in a future session) should be able to recreate AudioScribe from this spec plus `CLAUDE.md` by:

1. Reading this spec for requirements and business rules
2. Reading `CLAUDE.md` for technical constraints and development rules
3. Using `requirements.txt` for exact dependency versions
4. Following the platform-specific rules in Section 5
5. Implementing the UI layout described in Section 3
6. Applying the compatibility patches described in Section 5 (Business Rules)
7. Testing against the success criteria in Section 10
