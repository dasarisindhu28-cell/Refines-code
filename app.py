import gradio as gr
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANGS = ["Python","C","C++","Java","JavaScript"]
history_store = []

# ================= AI Helper =================
def ask_ai(prompt):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
    )
    return res.choices[0].message.content

# ================= Core Functions =================
def refine(code, lang):
    result = ask_ai(f"Fix and improve this {lang} code:\n{code}")
    history_store.append("REFINE:\n"+result)
    return result

def optimize(code, lang):
    result = ask_ai(f"Optimize this {lang} code:\n{code}")
    history_store.append("OPTIMIZE:\n"+result)
    return result

def convert(code, f, t):
    result = ask_ai(f"Convert {f} code to {t}:\n{code}")
    history_store.append("CONVERT:\n"+result)
    return result

def chatbot(msg, chat):
    reply = ask_ai(msg)
    history_store.append("CHAT:\n"+reply)
    chat.append((msg, reply))
    return "", chat

def show_history():
    return "\n\n-----------------\n\n".join(history_store)

# ================= CUSTOM CSS =================
css = """
body {
    background: linear-gradient(135deg,#0f172a,#020617);
}

.gradio-container {
    background: transparent !important;
}

h1 {
    color: #38bdf8;
    text-align: center;
}

button {
    background: linear-gradient(90deg,#22c55e,#06b6d4) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
}

textarea, .cm-editor {
    background: #020617 !important;
    color: #e2e8f0 !important;
}

.tabitem {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}
"""

# ================= UI =================
with gr.Blocks(title="CodeRefine AI", css=css) as app:

    gr.Markdown("# 🚀 CodeRefine AI")

    with gr.Tabs():

        # ===== REFINE =====
        with gr.Tab("Refine"):
            code1 = gr.Code(lines=12)
            lang1 = gr.Dropdown(LANGS)
            out1 = gr.Code()
            gr.Button("Refine Code").click(refine,[code1,lang1],out1)

        # ===== OPTIMIZE =====
        with gr.Tab("Optimize"):
            code2 = gr.Code(lines=12)
            lang2 = gr.Dropdown(LANGS)
            out2 = gr.Code()
            gr.Button("Optimize Code").click(optimize,[code2,lang2],out2)

        # ===== CONVERT =====
        with gr.Tab("Convert"):
            code3 = gr.Code(lines=12)
            f = gr.Dropdown(LANGS,label="From")
            t = gr.Dropdown(LANGS,label="To")
            out3 = gr.Code()
            gr.Button("Convert Code").click(convert,[code3,f,t],out3)

        # ===== CHATBOT =====
        with gr.Tab("AI Chatbot"):
            chatbot_ui = gr.Chatbot(height=400)
            msg = gr.Textbox(placeholder="Ask coding question...")
            msg.submit(chatbot,[msg,chatbot_ui],[msg,chatbot_ui])

        # ===== HISTORY =====
        with gr.Tab("History"):
            history_box = gr.Textbox(lines=20)
            gr.Button("Load History").click(show_history,None,history_box)

app.launch(server_name="0.0.0.0", server_port=7860)
