import gradio as gr
import os
from groq import Groq
from dotenv import load_dotenv

# =========================
# LOAD API KEY
# =========================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# CUSTOM CSS (REMOVES HEADER + FOOTER)
# =========================
custom_css = """
footer {display:none !important;}
.gradio-container .built-with {display:none !important;}
header {display:none !important;}

body {
    background: #0f172a;
    color: white;
    font-family: Arial;
}
"""

# =========================
# AI FUNCTION
# =========================
def ask_llm(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


# =========================
# PAGE NAVIGATION FUNCTIONS
# =========================
def go_home():
    return (
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
    )

def open_analyzer():
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=False),
    )

def open_chat():
    return (
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )


# =========================
# UI
# =========================
with gr.Blocks(css=custom_css, title="CodeRefine AI") as demo:

    # ---------- HOME ----------
    with gr.Column(visible=True) as home:
        gr.Markdown("# 🚀 CodeRefine AI")
        gr.Markdown("Your all-in-one coding assistant")

        analyzer_btn = gr.Button("🔍 Code Analyzer", size="lg")
        chat_btn = gr.Button("💬 AI Chatbot", size="lg")

    # ---------- ANALYZER ----------
    with gr.Column(visible=False) as analyzer_page:
        gr.Markdown("## 🔍 Code Analyzer")

        code_input = gr.Textbox(lines=15, label="Paste Code")
        analyze_btn = gr.Button("Analyze")
        output_box = gr.Textbox(lines=15, label="Result")

        back1 = gr.Button("⬅ Back")

        analyze_btn.click(ask_llm, code_input, output_box)

    # ---------- CHATBOT ----------
    with gr.Column(visible=False) as chat_page:
        gr.Markdown("## 💬 AI Chatbot")

        chat_input = gr.Textbox(label="Ask anything")
        chat_btn_send = gr.Button("Send")
        chat_output = gr.Textbox(lines=15)

        back2 = gr.Button("⬅ Back")

        chat_btn_send.click(ask_llm, chat_input, chat_output)

    # =========================
    # NAVIGATION EVENTS
    # =========================
    analyzer_btn.click(open_analyzer, outputs=[home, analyzer_page, chat_page])
    chat_btn.click(open_chat, outputs=[home, analyzer_page, chat_page])

    back1.click(go_home, outputs=[home, analyzer_page, chat_page])
    back2.click(go_home, outputs=[home, analyzer_page, chat_page])


# =========================
# RENDER PORT FIX
# =========================
port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)
