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
# FUNCTION TO CALL AI
# =========================
def ask_llm(prompt):
    if not prompt:
        return "Please enter a question."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# UI NAVIGATION FUNCTIONS
# =========================
def show_home():
    return (
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
    )

def show_analyzer():
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=False),
    )

def show_chat():
    return (
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )


# =========================
# BUILD UI
# =========================
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    # ---------- HOME PAGE ----------
    with gr.Column(visible=True) as home:
        gr.Markdown("# 🚀 CodeRefine AI")
        gr.Markdown("### Your All-in-One Coding Assistant")

        btn1 = gr.Button("🔍 Code Analyzer")
        btn2 = gr.Button("💬 AI Chatbot")

    # ---------- ANALYZER PAGE ----------
    with gr.Column(visible=False) as analyzer:
        gr.Markdown("## 🔍 Code Analyzer")

        code_input = gr.Textbox(lines=10, label="Paste your code")
        analyze_btn = gr.Button("Analyze")
        analyze_output = gr.Textbox(label="Result")

        back1 = gr.Button("⬅ Back")

        analyze_btn.click(ask_llm, code_input, analyze_output)

    # ---------- CHAT PAGE ----------
    with gr.Column(visible=False) as chat:
        gr.Markdown("## 💬 AI Chatbot")

        chat_input = gr.Textbox(label="Ask a coding question")
        chat_btn = gr.Button("Ask")
        chat_output = gr.Textbox(label="Answer")

        back2 = gr.Button("⬅ Back")

        chat_btn.click(ask_llm, chat_input, chat_output)

    # ---------- NAVIGATION ----------
    btn1.click(show_analyzer, outputs=[home, analyzer, chat])
    btn2.click(show_chat, outputs=[home, analyzer, chat])

    back1.click(show_home, outputs=[home, analyzer, chat])
    back2.click(show_home, outputs=[home, analyzer, chat])


# =========================
# IMPORTANT FOR RENDER
# =========================
demo.launch(server_name="0.0.0.0", server_port=7860)
