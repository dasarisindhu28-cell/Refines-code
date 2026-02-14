import gradio as gr
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANGS = ["Python", "C", "C++", "Java", "JavaScript"]
history_store = []

# ================= AI FUNCTIONS =================
def ask_ai(prompt):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def refine(code, lang):
    result = ask_ai(f"Fix and improve this {lang} code:\n{code}")
    history_store.append("REFINE:\n" + result)
    return result

def optimize(code, lang):
    result = ask_ai(f"Optimize this {lang} code:\n{code}")
    history_store.append("OPTIMIZE:\n" + result)
    return result

def convert(code, f, t):
    result = ask_ai(f"Convert {f} code to {t}:\n{code}")
    history_store.append("CONVERT:\n" + result)
    return result

def chatbot(msg, chat):
    reply = ask_ai(msg)
    history_store.append("CHAT:\n" + reply)
    chat = chat + [(msg, reply)]  # safer for remote deploy
    return "", chat

def show_history():
    return "\n\n-----------------\n\n".join(history_store)

# ================= CUSTOM CSS =================
css = """
body {
    background: linear-gradient(135deg,#020617,#0f172a,#020617);
}
footer {display:none !important;}
.sidebar {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 18px;
    padding: 20px;
}
h1 {
    text-align:center;
    font-size:42px;
    font-weight:800;
    background: linear-gradient(90deg,#38bdf8,#22c55e);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
button {
    background: linear-gradient(90deg,#22c55e,#06b6d4);
    border:none !important;
    border-radius:12px !important;
    font-weight:bold !important;
    height:50px;
    transition:.3s;
}
button:hover {
    transform:scale(1.05);
    box-shadow:0 0 15px #22c55e;
}
.cm-editor, textarea {
    background:#020617 !important;
    border-radius:12px !important;
}
.tabitem {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius:18px;
    padding:25px;
}
"""

# ================= UI =================
with gr.Blocks(css=css) as app:
    gr.Markdown("# 🚀 CodeRefine AI")

    with gr.Row():
        # ===== SIDEBAR =====
        with gr.Column(scale=1, elem_classes="sidebar"):
            gr.Markdown("### ⚡ Features")
            gr.Markdown("""
• Refine Code  
• Optimize Performance  
• Convert Languages  
• AI Coding Chatbot  
• Full History Tracking  
""")

        # ===== MAIN AREA =====
        with gr.Column(scale=4):
            with gr.Tabs():

                # ===== REFINE =====
                with gr.Tab("✨ Refine"):
                    code1 = gr.Code(lines=12, label="Paste code here")
                    lang1 = gr.Dropdown(LANGS, label="Language")
                    out1 = gr.Code(label="Refined Code")
                    gr.Button("Refine with AI").click(refine, [code1, lang1], out1)

                # ===== OPTIMIZE =====
                with gr.Tab("⚡ Optimize"):
                    code2 = gr.Code(lines=12, label="Paste code here")
                    lang2 = gr.Dropdown(LANGS, label="Language")
                    out2 = gr.Code(label="Optimized Code")
                    gr.Button("Optimize with AI").click(optimize, [code2, lang2], out2)

                # ===== CONVERT =====
                with gr.Tab("🔄 Convert"):
                    code3 = gr.Code(lines=12, label="Paste code here")
                    f = gr.Dropdown(LANGS, label="From")
                    t = gr.Dropdown(LANGS, label="To")
                    out3 = gr.Code(label="Converted Code")
                    gr.Button("Convert with AI").click(convert, [code3, f, t], out3)

                # ===== CHATBOT =====
                with gr.Tab("🤖 AI Chatbot"):
                    chatbot_ui = gr.Chatbot(height=420, label="Chat with AI")
                    msg = gr.Textbox(placeholder="Ask coding questions...", label="Your Message")
                    msg.submit(chatbot, [msg, chatbot_ui], [msg, chatbot_ui])

                # ===== HISTORY =====
                with gr.Tab("📜 History"):
                    history_box = gr.Textbox(lines=20, label="History")
                    gr.Button("Load History").click(show_history, None, history_box)

# ================= LAUNCH =================
if __name__ == "__main__":
    import gradio
    print("Gradio version:", gradio.__version__)
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # REQUIRED for Render
    )
