"""
AudioScribe - Local Audio Transcription with Speaker Identification
Windows version

Transcribe audio files locally using WhisperX with an optional
speaker diarization pipeline from pyannote.audio. No data leaves
your machine.

Usage:
    python audioscribe_windows.py

Then open http://127.0.0.1:7860 in your browser.
"""

import shutil
import pathlib
import datetime
import warnings

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# PyTorch 2.6+ changed torch.load to default weights_only=True which breaks
# loading pyannote VAD models used by WhisperX.  Patch it back to the old
# behaviour since all models are from trusted sources.
# ---------------------------------------------------------------------------
import torch
import torch.serialization
import torchaudio

# ---------------------------------------------------------------------------
# torchaudio 2.8+ removed AudioMetaData and list_audio_backends which
# pyannote.audio (used by WhisperX) still references.  Patch them back so
# the diarization pipeline can load without errors.
# ---------------------------------------------------------------------------
if not hasattr(torchaudio, "AudioMetaData"):
    from dataclasses import dataclass

    @dataclass
    class _AudioMetaData:
        sample_rate: int = 0
        num_frames: int = 0
        num_channels: int = 0
        bits_per_sample: int = 0
        encoding: str = ""

    torchaudio.AudioMetaData = _AudioMetaData

if not hasattr(torchaudio, "list_audio_backends"):
    torchaudio.list_audio_backends = lambda: ["ffmpeg"]

_original_torch_load = (
    torch.serialization.load.__wrapped__
    if hasattr(torch.serialization.load, "__wrapped__")
    else torch.serialization.load
)


def _patched_torch_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)


torch.load = _patched_torch_load
torch.serialization.load = _patched_torch_load

import gradio as gr

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HOME = pathlib.Path.home()
DOWNLOADS = HOME / "Downloads"
TOKEN_FILE = HOME / ".audioscribe_token.txt"

# ---------------------------------------------------------------------------
# Supported languages (WhisperX language codes)
# ---------------------------------------------------------------------------
LANGUAGES = [
    "English", "Spanish", "French", "German", "Italian", "Portuguese",
    "Dutch", "Russian", "Chinese", "Japanese", "Korean", "Arabic",
    "Hindi", "Turkish", "Polish", "Swedish", "Danish", "Norwegian",
    "Finnish", "Greek", "Czech",
]

LANG_CODES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Italian": "it", "Portuguese": "pt", "Dutch": "nl", "Russian": "ru",
    "Chinese": "zh", "Japanese": "ja", "Korean": "ko", "Arabic": "ar",
    "Hindi": "hi", "Turkish": "tr", "Polish": "pl", "Swedish": "sv",
    "Danish": "da", "Norwegian": "no", "Finnish": "fi", "Greek": "el",
    "Czech": "cs",
}

MODELS = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]

# ---------------------------------------------------------------------------
# Model cache — avoids reloading the same model between transcriptions
# ---------------------------------------------------------------------------
_model_cache = {"key": None, "model": None}

# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------

def load_token() -> str:
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    return ""


def save_token(token: str) -> str:
    token = token.strip()
    if not token:
        return "No token provided."
    TOKEN_FILE.write_text(token)
    return f"Token saved to {TOKEN_FILE}"


# ---------------------------------------------------------------------------
# Detect compute device
# ---------------------------------------------------------------------------

def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_compute_type(device: str) -> str:
    return "float16" if device == "cuda" else "int8"


# ---------------------------------------------------------------------------
# FFmpeg check
# ---------------------------------------------------------------------------

def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


# ---------------------------------------------------------------------------
# Model loading with cache
# ---------------------------------------------------------------------------

def _get_model(model_size, device, compute_type, lang_code):
    """Load a WhisperX model, reusing the cached one if settings match."""
    import whisperx

    global _model_cache
    key = (model_size, device, compute_type, lang_code)

    if _model_cache["key"] == key and _model_cache["model"] is not None:
        print("       Using cached model")
        return _model_cache["model"]

    # Free previous model
    if _model_cache["model"] is not None:
        del _model_cache["model"]
        _model_cache = {"key": None, "model": None}
        if device == "cuda":
            torch.cuda.empty_cache()

    model = whisperx.load_model(
        model_size, device, compute_type=compute_type, language=lang_code,
    )
    _model_cache = {"key": key, "model": model}
    return model


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def transcribe(audio_path, language, model_size, enable_diarization, hf_token,
               progress=gr.Progress()):
    """Transcribe an audio file and return the text."""
    if audio_path is None:
        return "Please upload an audio file."

    if not check_ffmpeg():
        return (
            "FFmpeg is not installed.\n\n"
            "FFmpeg is required to decode audio files. Install it:\n"
            "  Windows:  winget install FFmpeg\n"
            "  macOS:    brew install ffmpeg\n\n"
            "Then restart AudioScribe."
        )

    import whisperx

    device = get_device()
    compute_type = get_compute_type(device)
    lang_code = LANG_CODES.get(language)
    if language == "Auto-detect":
        lang_code = None

    token = (hf_token or "").strip() or load_token()

    print(f"\n{'=' * 60}")
    print(f"AudioScribe — Transcribing")
    print(f"  Model       : {model_size}")
    print(f"  Language    : {language}")
    print(f"  Device      : {device} ({compute_type})")
    print(f"  Diarization : {enable_diarization}")
    print(f"  HF token    : {'present' if token else 'MISSING'}")
    print(f"{'=' * 60}\n")

    try:
        # ---- Load model (cached between runs) ----
        progress(0.05, desc="Loading model...")
        print("[1/4] Loading model...")
        model = _get_model(model_size, device, compute_type, lang_code)

        # ---- Transcribe ----
        progress(0.2, desc="Transcribing audio...")
        print("[2/4] Transcribing audio...")
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=16 if device == "cuda" else 4)
        detected_lang = result.get("language", lang_code or "unknown")
        print(f"       Detected language: {detected_lang}")

        # ---- Align timestamps ----
        progress(0.55, desc="Aligning timestamps...")
        print("[3/4] Aligning timestamps...")
        try:
            align_model, metadata = whisperx.load_align_model(
                language_code=detected_lang, device=device,
            )
            result = whisperx.align(
                result["segments"], align_model, metadata, audio, device,
                return_char_alignments=False,
            )
            del align_model, metadata
        except Exception as e:
            print(f"       Alignment skipped: {e}")

        # ---- Speaker diarization (optional) ----
        if enable_diarization:
            if not token:
                print("[4/4] Speaker ID skipped — no Hugging Face token.")
            else:
                progress(0.75, desc="Identifying speakers...")
                print("[4/4] Identifying speakers...")
                try:
                    diarize_model = whisperx.DiarizationPipeline(
                        use_auth_token=token, device=device,
                    )
                    diarize_segments = diarize_model(audio)
                    print(f"       Diarize segments: {len(diarize_segments)} found")
                    result = whisperx.assign_word_speakers(diarize_segments, result)
                    del diarize_model, diarize_segments
                    print("       Speaker identification complete.")
                except Exception as e:
                    print(f"       Speaker ID failed: {e}")
        else:
            print("[4/4] Speaker diarization disabled — skipping.")

        # ---- Build transcript ----
        progress(0.9, desc="Saving transcript...")
        lines = []
        current_speaker = None
        for seg in result.get("segments", []):
            speaker = seg.get("speaker")
            text = seg.get("text", "").strip()
            if not text:
                continue
            if enable_diarization and speaker and speaker != current_speaker:
                current_speaker = speaker
                lines.append(f"\n[{speaker}]")
            lines.append(text)

        transcript = "\n".join(lines).strip()
        if not transcript:
            return "No speech detected in the audio file."

        # ---- Save to Downloads ----
        DOWNLOADS.mkdir(exist_ok=True)
        audio_name = pathlib.Path(audio_path).stem
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = DOWNLOADS / f"{audio_name}_{timestamp}.txt"
        out_file.write_text(transcript, encoding="utf-8")
        print(f"\nTranscript saved to: {out_file}\n")

        if device == "cuda":
            torch.cuda.empty_cache()

        progress(1.0, desc="Done!")
        return transcript

    except Exception as e:
        if device == "cuda":
            torch.cuda.empty_cache()
        msg = str(e)
        if "out of memory" in msg.lower():
            return (
                "Out of GPU memory.\n\n"
                "Try a smaller model:\n"
                "  tiny  — fastest, works on any hardware\n"
                "  base  — good balance of speed and accuracy\n"
                "  small — better accuracy, needs more memory\n\n"
                "Or close other GPU-intensive applications."
            )
        hints = [
            "Try a smaller model (e.g. 'tiny')",
            "Ensure the audio file is not corrupted",
        ]
        if "ffmpeg" in msg.lower() or "FileNotFoundError" in msg:
            hints.insert(0, "Install FFmpeg:  winget install FFmpeg")
        return (
            f"Transcription failed: {msg}\n\n"
            "Suggestions:\n" + "\n".join(f"  - {h}" for h in hints)
        )


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def build_ui():
    with gr.Blocks(title="AudioScribe", theme=gr.themes.Soft()) as app:
        gr.Markdown(
            "# AudioScribe\n"
            "Local audio transcription with optional speaker identification."
        )

        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    label="Upload Audio",
                    type="filepath",
                    source="upload",
                )
                language = gr.Dropdown(
                    choices=["Auto-detect"] + LANGUAGES,
                    value="English",
                    label="Language",
                )
                model_size = gr.Dropdown(
                    choices=MODELS,
                    value="tiny",
                    label="Model Size",
                )
                enable_diarization = gr.Checkbox(
                    label="Identify speakers",
                    value=True,
                )

                with gr.Accordion("Hugging Face Token (for speaker ID)", open=False):
                    gr.Markdown(
                        "Required only for speaker identification. "
                        "Get a free token at "
                        "[huggingface.co](https://huggingface.co/settings/tokens)."
                    )
                    hf_token = gr.Textbox(
                        label="Token",
                        placeholder="hf_...",
                        type="password",
                        value=load_token(),
                    )
                    save_btn = gr.Button("Save Token")
                    token_status = gr.Textbox(label="Status", interactive=False)
                    save_btn.click(fn=save_token, inputs=hf_token, outputs=token_status)

                transcribe_btn = gr.Button("Transcribe", variant="primary")

            with gr.Column(scale=2):
                output = gr.Textbox(
                    label="Transcript",
                    lines=25,
                    show_copy_button=True,
                )

        transcribe_btn.click(
            fn=transcribe,
            inputs=[audio_input, language, model_size, enable_diarization, hf_token],
            outputs=output,
        )

        gr.Markdown(
            "---\n"
            "Transcripts are saved to your **Downloads** folder.  \n"
            "Start with the **tiny** model — it's fast and works on any hardware."
        )

    return app


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("  AudioScribe — Local Audio Transcription")
    print("  Open your browser to http://127.0.0.1:7860")
    print("=" * 60 + "\n")

    if not check_ffmpeg():
        print("WARNING: FFmpeg is not found on PATH.")
        print("  Install: winget install FFmpeg (Windows)")
        print("           brew install ffmpeg (macOS)\n")

    app = build_ui()
    app.queue()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        share=False,
    )


if __name__ == "__main__":
    main()
