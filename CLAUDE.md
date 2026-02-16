# Claude Code Instructions - AudioScribe

## About This Project
Audio transcription tool with speaker diarization using Whisper AI. Processes audio files to generate accurate transcripts with speaker identification. Includes both Mac and Windows versions with Gradio UI for progress tracking.

## About Me (Chris Treadaway)
Product builder, not a coder. I bring requirements and vision — you handle implementation.

**Working with me:**
- Bias toward action - just do it, don't argue
- Make terminal commands dummy-proof (always start with `cd ~/audioscribe`)
- Minimize questions - make judgment calls and tell me what you chose
- I get interrupted frequently - always end sessions with a handoff note

## Tech Stack
- **Language:** Python 3.10+
- **AI Model:** OpenAI Whisper + WhisperX for diarization
- **UI:** Gradio for web interface
- **Key Libraries:**
  - whisperx (speaker diarization)
  - gradio (progress tracking UI)
  - torch (model inference)
  - HuggingFace transformers

## File Paths
- **Always use:** `~/audioscribe/path/to/file`
- **Never use:** `/Users/christreadaway/...`
- **Always start commands with:** `cd ~/audioscribe`

## PII Rules (CRITICAL)
❌ NEVER include:
- Real names from transcripts → use [Speaker Name]
- File paths with /Users/christreadaway → use ~/
- API keys/tokens in code

✅ ALWAYS use placeholders

## Key Features
- Audio file upload and processing
- Whisper AI transcription
- Speaker diarization (who said what)
- Progress tracking with Gradio queue
- Output: Timestamped transcripts with speaker labels
- Supports: Mac and Windows versions

## Platform-Specific Files
- **Mac:** `audioscribe_mac.py`
- **Windows:** `audioscribe_windows.py` (if exists)
- Both use same core logic, different paths/dependencies

## Common Issues

### HuggingFace Token Parameter Names
WhisperX library changed parameter names across versions:
- Old: `use_auth_token`
- Current: `token` or `hf_token`

Always use the current parameter name for the installed version.

### Gradio Queue Requirement
For progress tracking to work:
```python
interface.queue().launch()
```
Not just `.launch()` - the `.queue()` is critical.

### Python Version
Requires Python 3.10+ for type hints like `dict | None`

### CUDA/GPU Support
- Mac: Uses MPS (Metal Performance Shaders)
- Windows: Can use CUDA if available
- CPU fallback works but is slower

## Session End Routine
Before ending EVERY session, Claude will automatically create/update SESSION_NOTES.md:

```markdown
## [Date] [Time] - [Brief Description]

### What We Built
- [Feature 1]: [files modified]
- [Feature 2]: [what was implemented]

### Technical Details
Files changed:
- path/to/file.ext (what changed)
- path/to/file2.ext (what changed)

Code patterns used:
- [Pattern or approach used]
- [Libraries or techniques applied]

### Current Status
✅ Working: [what's tested and works]
❌ Broken: [known issues]
🚧 In Progress: [incomplete features]

### Branch Info
Branch: [branch-name]
Commits: [X files changed, Y insertions, Z deletions]
Ready to merge: [Yes/No - why or why not]

### Decisions Made
- [Decision 1 and rationale]
- [Decision 2 and rationale]

### Next Steps
1. [Priority 1 with specific action]
2. [Priority 2 with specific action]
3. [Priority 3 with specific action]

### Questions/Blockers
- [Open question or blocker]
- [Uncertainty that needs resolution]
```

**To execute:** Say "Append session notes to SESSION_NOTES.md" and Claude will:
1. Create/update SESSION_NOTES.md in repo root
2. Add new session at the TOP (most recent first)
3. Commit the file to current branch
4. Confirm completion

SESSION_NOTES.md is committed to the repo and tracks all session progress over time.

## Git Branch Strategy
- Claude Code creates new branch per session
- Merge to main when tested
- Delete merged branches

## Testing Approach
- Test with sample audio file
- Verify speaker diarization accuracy
- Check progress UI updates correctly
- Test on both Mac and Windows if possible

## Setup/Installation

### Mac
```bash
cd ~/audioscribe
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python audioscribe_mac.py
```

### Windows
```powershell
cd C:\Users\chris-treadaway\audioscribe
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python audioscribe_windows.py
```

## Environment Variables
```bash
# HuggingFace token for model access
HUGGINGFACE_TOKEN=hf_...
```

## Current Status
Working on Mac. Windows setup in progress. Debug/simplify session on Feb 13, 2026.

---
Last Updated: February 16, 2026


## Session Management

### Reading Past Work
- `SESSION_NOTES.md` contains complete session history with detailed conversations
- Read this file at session start if you need context on recent work
- Sessions are ordered newest-first with full technical details

### Ending Sessions
At the end of each session, say:
> "Append session notes to SESSION_NOTES.md"

Claude will automatically:
1. Generate a detailed session entry with conversation highlights
2. Add it to the top of SESSION_NOTES.md (newest first)
3. Include all technical work, files changed, commands used
4. Commit the updated file

### What Gets Logged
- Conversation highlights (substantial exchanges)
- Technical work and implementation details
- Files modified/created
- Commands executed
- URLs and documentation referenced
- Problem-solving context and decisions made