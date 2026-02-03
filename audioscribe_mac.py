#!/usr/bin/env python3
"""
AudioScribe - Local audio transcription with optional speaker identification.
macOS version

v1.250120
"""

import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

import gradio as gr
import torch
import whisperx

# Configuration
TOKEN_FILE = Path.home() / ".audioscribe_token.txt"
DOWNLOADS_DIR = Path.home() / "Downloads"

# Supported languages (21 languages as per README)
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Polish": "pl",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Korean": "ko",
    "Arabic": "ar",
    "Turkish": "tr",
    "Hindi": "hi",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Ukrainian": "uk",
    "Czech": "cs",
    "Auto-detect": None,
}

# Model options
MODELS = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]

# Supported audio formats
AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma"]


def get_device():
    """Determine the best available device for inference."""
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_compute_type(device):
    """Get appropriate compute type for the device."""
    if device == "cuda":
        return "float16"
    return "float32"


def load_token():
    """Load HuggingFace token from file."""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    return ""


def save_token(token):
    """Save HuggingFace token to file."""
    TOKEN_FILE.write_text(token.strip())
    return "Token saved successfully!"


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def transcribe(
    audio_file,
    language,
    model_size,
    enable_diarization,
    hf_token,
    progress=gr.Progress(),
):
    """Main transcription function."""
    if audio_file is None:
        return "Please upload an audio file.", ""

    # Validate file extension
    audio_path = Path(audio_file)
    if audio_path.suffix.lower() not in AUDIO_FORMATS:
        return f"Unsupported file format. Supported formats: {', '.join(AUDIO_FORMATS)}", ""

    device = get_device()
    compute_type = get_compute_type(device)

    print(f"\n{'='*60}")
    print(f"AudioScribe Transcription")
    print(f"{'='*60}")
    print(f"File: {audio_path.name}")
    print(f"Device: {device}")
    print(f"Model: {model_size}")
    print(f"Language: {language}")
    print(f"Speaker identification: {'Enabled' if enable_diarization else 'Disabled'}")
    print(f"{'='*60}\n")

    try:
        # Load model
        progress(0.1, desc="Loading model...")
        print("Loading Whisper model...")

        lang_code = LANGUAGES.get(language)
        model = whisperx.load_model(
            model_size,
            device,
            compute_type=compute_type,
            language=lang_code,
        )

        # Load audio
        progress(0.2, desc="Loading audio...")
        print("Loading audio file...")
        audio = whisperx.load_audio(str(audio_path))

        # Transcribe
        progress(0.3, desc="Transcribing...")
        print("Transcribing audio (this may take a while)...")
        result = model.transcribe(audio, batch_size=16)
        detected_language = result.get("language", lang_code or "en")
        print(f"Detected language: {detected_language}")

        # Align whisper output
        progress(0.6, desc="Aligning transcription...")
        print("Aligning transcription...")
        model_a, metadata = whisperx.load_align_model(
            language_code=detected_language, device=device
        )
        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            device,
            return_char_alignments=False,
        )

        # Speaker diarization (optional)
        if enable_diarization and hf_token:
            progress(0.7, desc="Identifying speakers...")
            print("Running speaker identification...")
            try:
                diarize_model = whisperx.DiarizationPipeline(
                    use_auth_token=hf_token, device=device
                )
                diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
                print("Speaker identification complete!")
            except Exception as e:
                print(f"Speaker identification failed: {e}")
                print("Continuing with basic transcription...")

        # Format output
        progress(0.9, desc="Formatting output...")
        print("Formatting transcript...")

        transcript_lines = []
        full_text_lines = []

        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()

            # Check for speaker label
            speaker = segment.get("speaker", "")
            if speaker:
                line = f"[{start_time} - {end_time}] [{speaker}]: {text}"
            else:
                line = f"[{start_time} - {end_time}]: {text}"

            transcript_lines.append(line)
            full_text_lines.append(text)

        transcript = "\n".join(transcript_lines)
        full_text = " ".join(full_text_lines)

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{audio_path.stem}_transcript_{timestamp}.txt"
        output_path = DOWNLOADS_DIR / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"AudioScribe Transcript\n")
            f.write(f"File: {audio_path.name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {model_size}\n")
            f.write(f"Language: {detected_language}\n")
            f.write(f"{'='*60}\n\n")
            f.write(transcript)
            f.write(f"\n\n{'='*60}\n")
            f.write("Full Text:\n\n")
            f.write(full_text)

        progress(1.0, desc="Complete!")
        print(f"\nTranscript saved to: {output_path}")
        print("Transcription complete!")

        return transcript, f"Saved to: {output_path}"

    except Exception as e:
        error_msg = f"Error during transcription: {str(e)}"
        print(error_msg)
        return error_msg, ""


def create_interface():
    """Create the Gradio web interface."""
    with gr.Blocks(
        title="AudioScribe",
        theme=gr.themes.Soft(),
    ) as app:
        gr.Markdown(
            """
            # AudioScribe
            **Local audio transcription with optional speaker identification**

            Upload an audio file, select your options, and click Transcribe.
            Your transcript will be saved to your Downloads folder.
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    label="Upload Audio File",
                    type="filepath",
                    sources=["upload"],
                )

                language = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="English",
                    label="Language",
                )

                model_size = gr.Dropdown(
                    choices=MODELS,
                    value="tiny",
                    label="Model Size",
                    info="Start with 'tiny' - it's fast and works on any computer",
                )

                with gr.Accordion("Speaker Identification", open=False):
                    gr.Markdown(
                        """
                        **Optional:** Identify who said what in your transcript.

                        Requires a free [Hugging Face](https://huggingface.co/join) account.
                        You must also accept the model terms:
                        - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
                        - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
                        """
                    )

                    enable_diarization = gr.Checkbox(
                        label="Enable speaker identification",
                        value=False,
                    )

                    hf_token = gr.Textbox(
                        label="Hugging Face Token",
                        type="password",
                        value=load_token(),
                        placeholder="hf_xxxxxxxxxxxxx",
                    )

                    save_btn = gr.Button("Save Token", size="sm")
                    token_status = gr.Textbox(label="", interactive=False, visible=False)

                    save_btn.click(
                        fn=save_token,
                        inputs=[hf_token],
                        outputs=[token_status],
                    ).then(
                        fn=lambda: gr.update(visible=True),
                        outputs=[token_status],
                    )

                transcribe_btn = gr.Button(
                    "Transcribe",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=2):
                output_text = gr.Textbox(
                    label="Transcript",
                    lines=25,
                    max_lines=50,
                    show_copy_button=True,
                )

                save_status = gr.Textbox(
                    label="Save Status",
                    interactive=False,
                )

        transcribe_btn.click(
            fn=transcribe,
            inputs=[
                audio_input,
                language,
                model_size,
                enable_diarization,
                hf_token,
            ],
            outputs=[output_text, save_status],
        )

        gr.Markdown(
            """
            ---
            **Tips:**
            - Start with the `tiny` model — it's fast and surprisingly accurate
            - Watch the terminal for progress updates
            - Transcripts are saved to your Downloads folder
            - Speaker identification works best on clear audio with distinct voices

            **Supported formats:** MP3, WAV, M4A, AAC, FLAC, OGG, WMA
            """
        )

    return app


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AudioScribe - Local Audio Transcription")
    print("="*60)
    print(f"Device: {get_device()}")
    print("Starting web interface...")
    print("="*60 + "\n")

    app = create_interface()
    app.launch(
        inbrowser=True,
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
    )
