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
# CUSTOM CSS
# =========================
custom_css = """
/* REMOVE HEADER */
header {display: none !important;}

/* REMOVE FOOTER */
footer {display: none !important;}
.gradio-container .footer {display: none !important;}

/* BACKGROUND */
body {
    background: #0f172a !important;
    font-family: 'Segoe UI', sans-serif;
}

/* CENTER CONTAINER */
.gradio-container {
    max-width: 600px !important;
    margin: auto !important;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}

/* BUTTON STYLE */
.big-btn {
    background: #374151 !important;
    color: white !important;
    font-size: 20px !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin-bottom: 15px !important;
}
"""

# =========================
# AI FUNCTION
# =========================
def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


# =========================
# NAVIGATION FUNCTIONS
# =========================
def show_analyzer():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def show_chat():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def go_home():
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)


# =========================
# UI
# =========================
with gr.Blocks(css=custom_css) as demo:

    # -------- HOME --------
    home = gr.Column(visible=True)

    with home:
        gr.Markdown("<div class='title'>Your All-in-One Coding Assistant</div>")

        analyzer_btn = gr.Button("🔍 Code Analyzer", elem_classes="big-btn")
        chat_btn = gr.Button("💬 AI Chatbot", elem_classes="big-btn")


    # -------- ANALYZER PAGE --------
    analyzer_page = gr.Column(visible=False)

    with analyzer_page:
        gr.Markdown("## 🔍 Code Analyzer")

        code_input = gr.Textbox(lines=10, placeholder="Paste your code here...")
        analyze_btn = gr.Button("Analyze")
        output = gr.Textbox(lines=10)

        back1 = gr.Button("⬅ Back")

        analyze_btn.click(ask_ai, code_input, output)
        back1.click(go_home, outputs=[home, analyzer_page, chat_page])


    # -------- CHAT PAGE --------
    chat_page = gr.Column(visible=False)

    with chat_page:
        gr.Markdown("## 💬 AI Chatbot")

        chat_input = gr.Textbox(placeholder="Ask coding question...")
        send_btn = gr.Button("Send")
        chat_output = gr.Textbox(lines=10)

        back2 = gr.Button("⬅ Back")

        send_btn.click(ask_ai, chat_input, chat_output)
        back2.click(go_home, outputs=[home, analyzer_page, chat_page])


    # -------- NAVIGATION --------
    analyzer_btn.click(show_analyzer, outputs=[home, analyzer_page, chat_page])
    chat_btn.click(show_chat, outputs=[home, analyzer_page, chat_page])


# =========================
# RUN APP
# =========================
demo.launch(server_name="0.0.0.0", server_port=7860)
