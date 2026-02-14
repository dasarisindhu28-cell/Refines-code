import gradio as gr

# =========================
# Language Extensions
# =========================
EXTENSIONS = {
    "Python": ".py",
    "C": ".c",
    "C++": ".cpp",
    "Java": ".java",
    "JavaScript": ".js"
}

# =========================
# Modern UI CSS
# =========================
custom_css = """
body { background: #0f172a !important; font-family: Inter, sans-serif; }
.gradio-container { max-width: 1100px !important; margin: auto !important; }

.block {
    background: #1e293b;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    cursor: pointer;
    transition: 0.2s;
    font-size: 20px;
    font-weight: bold;
}
.block:hover { transform: scale(1.05); }

button {
    background: linear-gradient(135deg,#2563eb,#1d4ed8);
    border-radius: 14px;
    font-size: 16px;
    height: 50px;
}

textarea { font-size: 15px !important; }

footer { display: none !important; }
"""

# =========================
# Core Functions
# =========================
def refine_code(code, lang):
    if not code:
        return "⚠️ Enter code first!"
    return f"✨ Refined {lang} Code:\n\n{code.upper()}"

def optimize_code(code, lang):
    if not code:
        return "⚠️ Enter code first!"
    return f"⚡ Optimized {lang} Code:\n\n{code[::-1]}"

def convert_code(code, f, t):
    if not code:
        return "⚠️ Enter code first!"
    return f"🔄 Converted from {f} → {t}\n\n{code}"

# =========================
# Layout
# =========================
with gr.Blocks(css=custom_css, title="CodeRefine AI") as app:

    # -------- HOME PAGE --------
    with gr.Column(visible=True) as home:
        gr.Markdown("# 🚀 CodeRefine AI")
        gr.Markdown("### Fix • Optimize • Convert Code Instantly")

        with gr.Row():
            btn1 = gr.Button("✨ Refine Code", elem_classes="block")
            btn2 = gr.Button("⚡ Optimize Code", elem_classes="block")
            btn3 = gr.Button("🔄 Convert Code", elem_classes="block")

    # -------- REFINE --------
    with gr.Column(visible=False) as refine_page:
        gr.Markdown("## ✨ Refine Code")

        code1 = gr.Code(label="Paste Code", lines=15)
        lang1 = gr.Dropdown(list(EXTENSIONS.keys()), label="Language")

        out1 = gr.Code(label="Result")
        run1 = gr.Button("Refine Now")
        back1 = gr.Button("⬅ Back")

        run1.click(refine_code, [code1, lang1], out1)

    # -------- OPTIMIZE --------
    with gr.Column(visible=False) as optimize_page:
        gr.Markdown("## ⚡ Optimize Code")

        code2 = gr.Code(label="Paste Code", lines=15)
        lang2 = gr.Dropdown(list(EXTENSIONS.keys()), label="Language")

        out2 = gr.Code(label="Result")
        run2 = gr.Button("Optimize Now")
        back2 = gr.Button("⬅ Back")

        run2.click(optimize_code, [code2, lang2], out2)

    # -------- CONVERT --------
    with gr.Column(visible=False) as convert_page:
        gr.Markdown("## 🔄 Convert Code")

        code3 = gr.Code(label="Paste Code", lines=15)
        from_lang = gr.Dropdown(list(EXTENSIONS.keys()), label="From")
        to_lang = gr.Dropdown(list(EXTENSIONS.keys()), label="To")

        out3 = gr.Code(label="Result")
        run3 = gr.Button("Convert Now")
        back3 = gr.Button("⬅ Back")

        run3.click(convert_code, [code3, from_lang, to_lang], out3)

    # =========================
    # Navigation
    # =========================
    def show_refine():
        return False, True, False, False

    def show_optimize():
        return False, False, True, False

    def show_convert():
        return False, False, False, True

    def show_home():
        return True, False, False, False

    btn1.click(show_refine, outputs=[home, refine_page, optimize_page, convert_page])
    btn2.click(show_optimize, outputs=[home, refine_page, optimize_page, convert_page])
    btn3.click(show_convert, outputs=[home, refine_page, optimize_page, convert_page])

    back1.click(show_home, outputs=[home, refine_page, optimize_page, convert_page])
    back2.click(show_home, outputs=[home, refine_page, optimize_page, convert_page])
    back3.click(show_home, outputs=[home, refine_page, optimize_page, convert_page])

# =========================
# Launch
# =========================
app.launch(server_name="0.0.0.0", server_port=7860)
