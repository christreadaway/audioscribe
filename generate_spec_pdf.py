"""Generate AudioScribe Windows Setup Spec PDF."""
from fpdf import FPDF

class SpecPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "AudioScribe - Windows Setup Product Spec", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.ln(4)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(60, 60, 60)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + 5)
        self.multi_cell(180, 5, text, fill=True)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + 5)
        if bold_prefix:
            self.cell(3, 5.5, "- ")
            self.set_font("Helvetica", "B", 10)
            self.write(5.5, bold_prefix + " ")
            self.set_font("Helvetica", "", 10)
            self.multi_cell(0, 5.5, text)
        else:
            self.multi_cell(175, 5.5, "-  " + text)
        self.ln(0.5)

    def table_row(self, cols, widths, bold=False):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 9)
        h = 6
        for i, col in enumerate(cols):
            self.cell(widths[i], h, col, border=1, align="L")
        self.ln(h)


pdf = SpecPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 22)
pdf.set_text_color(20, 20, 20)
pdf.cell(0, 15, "AudioScribe", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Windows Setup Product Spec", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)

pdf.body_text(
    "Repo: https://github.com/christreadaway/audioscribe\n"
    "Branch: claude/setup-audioscribe-windows-DreIB\n"
    "Primary file: audioscribe_windows.py (283 lines)\n"
    "Launcher: AudioScribe_Windows.bat"
)

# ---- What AudioScribe Does ----
pdf.section_title("What AudioScribe Does")
pdf.body_text(
    "A local-only audio transcription app with a browser-based UI. The user uploads an audio file, "
    "it transcribes using WhisperX (an OpenAI Whisper variant), optionally identifies speakers via "
    "pyannote.audio, and saves a .txt transcript to ~/Downloads. No data leaves the machine. "
    "Runs a Gradio web app at http://127.0.0.1:7860."
)

# ---- Architecture ----
pdf.section_title("Architecture (single file: audioscribe_windows.py)")

w = [45, 20, 125]
pdf.table_row(["Section", "Lines", "What it does"], w, bold=True)
pdf.table_row(["torch.load patch", "29-36", "Patches PyTorch 2.6+ to allow weights_only=False for pyannote"], w)
pdf.table_row(["Config/constants", "38-64", "Paths, 21 supported languages, 6 Whisper model sizes"], w)
pdf.table_row(["load/save_token", "70-81", "Read/write HuggingFace token from ~/.audioscribe_token.txt"], w)
pdf.table_row(["get_device", "87-97", "Detects CUDA vs CPU, sets float16 vs int8"], w)
pdf.table_row(["transcribe()", "103-196", "Core: load model, transcribe, align, diarize, save .txt"], w)
pdf.table_row(["build_ui()", "202-261", "Gradio Blocks UI with all inputs and transcript output"], w)
pdf.table_row(["main()", "267-283", "Prints banner, launches Gradio on 127.0.0.1:7860"], w)

# ---- Dependencies ----
pdf.section_title("Dependencies")

w2 = [50, 140]
pdf.table_row(["Package", "Purpose"], w2, bold=True)
pdf.table_row(["torch, torchaudio", "ML framework, audio processing"], w2)
pdf.table_row(["whisperx", "Transcription engine (wraps faster-whisper + ctranslate2)"], w2)
pdf.table_row(["gradio==3.50.2", "Web UI (must be this version - see Known Issues)"], w2)
pdf.table_row(["ffmpeg", "Audio decoding (system install, not pip)"], w2)
pdf.table_row(["pyannote.audio", "Speaker diarization (pulled in by whisperx)"], w2)

# ---- Known Issues ----
pdf.section_title("Known Issues (Current State of the Branch)")

pdf.sub_title("Issue 1: Gradio API mismatch on the branch")
pdf.body_text(
    "The branch currently has code written for NEW Gradio (5.x/6.x) API, but the project "
    "should use gradio==3.50.2 (as documented in README and .bat file). WhisperX was built "
    "against old Gradio. Two lines need to be reverted on the branch:"
)
pdf.bullet("Line 213: change sources=[\"upload\"] back to source=\"upload\"")
pdf.bullet("Line 245: change buttons=[\"copy\"] back to show_copy_button=True")

pdf.sub_title("Issue 2: Python version requirement")
pdf.body_text(
    "WhisperX depends on ctranslate2==4.4.0 which requires Python <3.14. "
    "Python 3.11 is the recommended version. Python 3.12 also works. "
    "Python 3.13 and 3.14 do NOT work. If pip install whisperx fails with "
    "\"No matching distribution found for ctranslate2\", this is the cause."
)

pdf.sub_title("Issue 3: Virtual environment required")
pdf.body_text(
    "The .bat launcher expects a .venv folder. System-wide pip installs on a wrong "
    "Python version will not work. A venv created with py -3.11 is required."
)

# ---- Correct Setup Steps ----
pdf.section_title("Correct Setup Steps (Windows)")

pdf.sub_title("Step 1: Install Python 3.11")
pdf.body_text(
    "Download from https://www.python.org/downloads/release/python-3119/\n"
    "Check \"Add Python to PATH\" during installation.\n"
    "Verify: py -3.11 --version"
)

pdf.sub_title("Step 2: Install FFmpeg")
pdf.code_block("winget install FFmpeg")

pdf.sub_title("Step 3: Clone the repo")
pdf.code_block(
    "git clone https://github.com/christreadaway/audioscribe.git\n"
    "cd audioscribe"
)

pdf.sub_title("Step 4: Create virtual environment")
pdf.code_block(
    "py -3.11 -m venv .venv\n"
    ".venv\\Scripts\\Activate.ps1"
)
pdf.body_text(
    "If you get an execution policy error, run this first:\n"
    "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned"
)

pdf.sub_title("Step 5: Install dependencies")
pdf.body_text("For NVIDIA GPU (faster):")
pdf.code_block(
    "pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118\n"
    "pip install whisperx gradio==3.50.2"
)
pdf.body_text("For CPU only:")
pdf.code_block("pip install torch torchaudio whisperx gradio==3.50.2")

pdf.sub_title("Step 6: Run")
pdf.code_block("python audioscribe_windows.py")
pdf.body_text("Or double-click AudioScribe_Windows.bat.")

# ---- Files in Repo ----
pdf.section_title("Files in Repo")

w3 = [60, 130]
pdf.table_row(["File", "Purpose"], w3, bold=True)
pdf.table_row(["audioscribe_windows.py", "Main application (283 lines)"], w3)
pdf.table_row(["AudioScribe_Windows.bat", "Double-click launcher (expects .venv to exist)"], w3)
pdf.table_row(["README.md", "Full user-facing docs (219 lines)"], w3)
pdf.table_row(["LICENSE", "MIT license"], w3)

# ---- What to Do Next ----
pdf.section_title("What to Do Next")

pdf.bullet(
    "Revert the two Gradio API changes on the branch so the code matches gradio==3.50.2: "
    "line 213 (sources -> source) and line 245 (buttons -> show_copy_button)."
)
pdf.bullet(
    "Install Python 3.11, create the .venv, install deps with gradio==3.50.2, and test end-to-end."
)
pdf.bullet(
    "Verify transcription works with a short audio file using the \"tiny\" model."
)
pdf.bullet(
    "Optionally test speaker diarization with a Hugging Face token."
)

# ---- Save ----
pdf.output("/home/user/audioscribe/AudioScribe_Windows_Setup_Spec.pdf")
print("PDF generated.")
