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

import os
import sys
import time
import pathlib
import datetime
import warnings

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# PyTorch 2.6+ changed torch.load to default weights_only=True which breaks
# loading pyannote VAD models used by WhisperX. Patch it back to the old
# behaviour since all models are from trusted sources.
# ---------------------------------------------------------------------------
import torch
import torch.serialization
_original_torch_load = torch.serialization.load.__wrapped__ if hasattr(torch.serialization.load, '__wrapped__') else torch.serialization.load
def _patched_torch_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_torch_load
torch.serialization.load = _patched_torch_load

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

def get_device():
    import torch
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_compute_type(device: str) -> str:
    if device == "cuda":
        return "float16"
    return "int8"

# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def transcribe(audio_path, language, model_size, enable_diarization, hf_token, progress=None):
    if audio_path is None:
        return "Please upload an audio file."

    import whisperx
    import torch

    device = get_device()
    compute_type = get_compute_type(device)

    lang_code = LANG_CODES.get(language)
    if language == "Auto-detect":
        lang_code = None

    # ---- Step 1: Load model and transcribe ----
    print(f"\n{'='*60}")
    print(f"AudioScribe — Transcribing")
    print(f"  Model   : {model_size}")
    print(f"  Language : {language}")
    print(f"  Device   : {device} ({compute_type})")
    print(f"{'='*60}\n")

    print("[1/3] Loading model...")
    model = whisperx.load_model(model_size, device, compute_type=compute_type,
                                language=lang_code)

    print("[2/3] Transcribing audio...")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=16 if device == "cuda" else 4)

    detected_lang = result.get("language", lang_code or "unknown")
    print(f"       Detected language: {detected_lang}")

    # ---- Step 2: Align timestamps ----
    print("[3/3] Aligning timestamps...")
    try:
        align_model, metadata = whisperx.load_align_model(
            language_code=detected_lang, device=device
        )
        result = whisperx.align(
            result["segments"], align_model, metadata, audio, device,
            return_char_alignments=False,
        )
    except Exception as e:
        print(f"       Alignment skipped: {e}")

    # ---- Step 3 (optional): Speaker diarization ----
    if enable_diarization:
        token = (hf_token or "").strip() or load_token()
        if not token:
            print("       Speaker ID skipped — no Hugging Face token provided.")
        else:
            print("       Running speaker identification (this may take a while)...")
            try:
                diarize_model = whisperx.DiarizationPipeline(
                    use_auth_token=token, device=device
                )
                diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
                print("       Speaker identification complete.")
            except Exception as e:
                print(f"       Speaker ID failed: {e}")

    # ---- Build transcript text ----
    lines = []
    current_speaker = None
    for seg in result.get("segments", []):
        speaker = seg.get("speaker", None)
        text = seg.get("text", "").strip()
        if not text:
            continue
        if enable_diarization and speaker:
            if speaker != current_speaker:
                current_speaker = speaker
                lines.append(f"\n[{speaker}]")
            lines.append(text)
        else:
            lines.append(text)

    transcript = "\n".join(lines).strip()

    # ---- Save to Downloads ----
    audio_name = pathlib.Path(audio_path).stem
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = DOWNLOADS / f"{audio_name}_{timestamp}.txt"
    out_file.write_text(transcript, encoding="utf-8")
    print(f"\nTranscript saved to: {out_file}\n")

    # Free GPU memory
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    return transcript

# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

def build_ui():
    import gradio as gr

    with gr.Blocks(title="AudioScribe", theme=gr.themes.Soft()) as app:
        gr.Markdown("# AudioScribe\nLocal audio transcription with optional speaker identification.")

        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    label="Upload Audio",
                    type="filepath",
                    sources=["upload"],
                )
                language = gr.Dropdown(
                    choices=["Auto-detect"] + LANGUAGES,
                    value="English",
                    label="Language",
                )
                model_size = gr.Dropdown(
                    choices=MODELS,
                    value="tiny",
                    label="Model (start with tiny)",
                )
                enable_diarization = gr.Checkbox(
                    label="Enable speaker identification",
                    value=False,
                )
                hf_token = gr.Textbox(
                    label="Hugging Face Token (optional)",
                    placeholder="hf_...",
                    type="password",
                    value=load_token(),
                )
                save_btn = gr.Button("Save Token")
                token_status = gr.Textbox(label="Token Status", interactive=False)
                save_btn.click(fn=save_token, inputs=hf_token, outputs=token_status)

                transcribe_btn = gr.Button("Transcribe", variant="primary")

            with gr.Column(scale=2):
                output = gr.Textbox(
                    label="Transcript",
                    lines=25,
                    buttons=["copy"],
                )

        transcribe_btn.click(
            fn=transcribe,
            inputs=[audio_input, language, model_size, enable_diarization, hf_token],
            outputs=output,
        )

        gr.Markdown(
            "---\n"
            "Transcripts are saved to your **Downloads** folder.  \n"
            "Speaker identification requires a free "
            "[Hugging Face](https://huggingface.co/join) account."
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

    app = build_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        share=False,
    )


if __name__ == "__main__":
    main()
