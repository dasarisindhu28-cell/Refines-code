import gradio as gr
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# PROFESSIONAL CSS
# ======================
css = """
footer {display:none !important;}
header {display:none !important;}

body {
    background: linear-gradient(135deg,#0f172a,#020617);
    color:white;
    font-family: 'Segoe UI';
}

.card {
    background:#111827;
    padding:30px;
    border-radius:16px;
    text-align:center;
    cursor:pointer;
    transition:0.3s;
    border:1px solid #1f2937;
}

.card:hover {
    transform:scale(1.05);
    background:#1e293b;
}

.bigtitle {
    font-size:48px;
    font-weight:bold;
    text-align:center;
}

.subtitle {
    text-align:center;
    color:#9ca3af;
}
"""

# ======================
# AI CALL
# ======================
def ask_llm(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


# ======================
# FILE ANALYZER
# ======================
def analyze_file(file):
    if file is None:
        return "Upload a file first."
    content = file.read().decode("utf-8")
    return ask_llm("Analyze this code and suggest improvements:\n" + content)


# ======================
# NAVIGATION
# ======================
def show_home():
    return [gr.update(visible=True)] + [gr.update(visible=False)]*4

def show_analyzer():
    return [gr.update(visible=False), gr.update(visible=True),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False)]

def show_chat():
    return [gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=True), gr.update(visible=False),
            gr.update(visible=False)]

def show_converter():
    return [gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False), gr.update(visible=True),
            gr.update(visible=False)]

def show_file():
    return [gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=False), gr.update(visible=False),
            gr.update(visible=True)]


# ======================
# UI
# ======================
with gr.Blocks(css=css, title="CodeRefine AI") as demo:

    chat_history = gr.State([])

    # HOME PAGE
    with gr.Column(visible=True) as home:
        gr.Markdown("<div class='bigtitle'>🚀 CodeRefine AI</div>")
        gr.Markdown("<div class='subtitle'>Professional AI Coding Platform</div>")

        with gr.Row():
            btn1 = gr.Button("🔍 Code Analyzer", elem_classes="card")
            btn2 = gr.Button("💬 AI Chatbot", elem_classes="card")
            btn3 = gr.Button("🔄 Code Converter", elem_classes="card")
            btn4 = gr.Button("📂 File Analyzer", elem_classes="card")


    # ================= ANALYZER =================
    with gr.Column(visible=False) as analyzer_page:
        gr.Markdown("## 🔍 Code Analyzer")

        code_input = gr.Textbox(lines=15, label="Paste Code")
        analyze_btn = gr.Button("Analyze")
        result = gr.Textbox(lines=15)
        download = gr.File(label="Download Result")

        def analyze(code):
            res = ask_llm("Analyze and optimize:\n" + code)
            path = "result.txt"
            with open(path, "w") as f:
                f.write(res)
            return res, path

        analyze_btn.click(analyze, code_input, [result, download])
        back1 = gr.Button("⬅ Back")


    # ================= CHAT =================
    with gr.Column(visible=False) as chat_page:
        gr.Markdown("## 💬 AI Chatbot")

        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox()
        send = gr.Button("Send")
        back2 = gr.Button("⬅ Back")

        def chat(user, history):
            history.append((user, ask_llm(user)))
            return history, history

        send.click(chat, [msg, chat_history], [chatbot, chat_history])


    # ================= CONVERTER =================
    with gr.Column(visible=False) as converter_page:
        gr.Markdown("## 🔄 Code Converter")

        code = gr.Textbox(lines=15)
        lang = gr.Dropdown(["Python","Java","C++","JavaScript"])
        convert_btn = gr.Button("Convert")
        output = gr.Textbox(lines=15)
        back3 = gr.Button("⬅ Back")

        convert_btn.click(
            lambda c,l: ask_llm(f"Convert this code into {l}:\n{c}"),
            [code, lang],
            output
        )


    # ================= FILE ANALYZER =================
    with gr.Column(visible=False) as file_page:
        gr.Markdown("## 📂 File Analyzer")

        file_upload = gr.File()
        analyze_file_btn = gr.Button("Analyze File")
        file_output = gr.Textbox(lines=15)
        back4 = gr.Button("⬅ Back")

        analyze_file_btn.click(analyze_file, file_upload, file_output)


    # ================= EVENTS =================
    btn1.click(show_analyzer, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    btn2.click(show_chat, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    btn3.click(show_converter, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    btn4.click(show_file, outputs=[home, analyzer_page, chat_page, converter_page, file_page])

    back1.click(show_home, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    back2.click(show_home, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    back3.click(show_home, outputs=[home, analyzer_page, chat_page, converter_page, file_page])
    back4.click(show_home, outputs=[home, analyzer_page, chat_page, converter_page, file_page])


# ======================
# RENDER PORT FIX
# ======================
port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port)
