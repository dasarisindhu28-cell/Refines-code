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
    chat = chat + [(msg, reply)]
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
    height:60px;
    font-size:18px;
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
.block-button {
    width:100%;
    height:120px;
    font-size:24px;
    margin:15px 0;
}

/* Smooth transitions */
.fade {
    transition: opacity 0.4s ease-in-out, transform 0.4s ease-in-out;
}
.hidden {
    opacity: 0;
    pointer-events: none;
    transform: scale(0.95);
}
.visible {
    opacity: 1;
    pointer-events: auto;
    transform: scale(1);
}
"""

# ================= UI =================
with gr.Blocks(css=css) as app:

    # FRONT PAGE
    with gr.Column(visible=True, elem_classes="fade visible") as front_page:
        gr.Markdown("# 🚀 CodeRefine AI")
        gr.Markdown("### Select a tool to get started:")
        refine_btn = gr.Button("✨ Refine / Optimize Code", elem_classes="block-button")
        convert_btn = gr.Button("🔄 Convert Code", elem_classes="block-button")
        chat_btn = gr.Button("🤖 AI Chatbot", elem_classes="block-button")

    # ================= REFINE/OPTIMIZE TAB =================
    with gr.Column(visible=False, elem_classes="fade hidden") as refine_tab:
        gr.Markdown("### ✨ Refine / Optimize Code")
        back1 = gr.Button("⬅ Back to Home")
        code1 = gr.Code(lines=12, label="Paste code here")
        lang1 = gr.Dropdown(LANGS, label="Language")
        out1 = gr.Code(label="Refined Code")
        refine_btn_tab = gr.Button("Refine with AI")
        refine_btn_tab.click(refine, [code1, lang1], out1)
        optimize_btn_tab = gr.Button("Optimize with AI")
        optimize_btn_tab.click(optimize, [code1, lang1], out1)

    # ================= CONVERT TAB =================
    with gr.Column(visible=False, elem_classes="fade hidden") as convert_tab:
        gr.Markdown("### 🔄 Convert Code")
        back2 = gr.Button("⬅ Back to Home")
        code2 = gr.Code(lines=12, label="Paste code here")
        f = gr.Dropdown(LANGS, label="From")
        t = gr.Dropdown(LANGS, label="To")
        out2 = gr.Code(label="Converted Code")
        convert_btn_tab = gr.Button("Convert with AI")
        convert_btn_tab.click(convert, [code2, f, t], out2)

    # ================= CHATBOT TAB =================
    with gr.Column(visible=False, elem_classes="fade hidden") as chat_tab:
        gr.Markdown("### 🤖 AI Chatbot")
        back3 = gr.Button("⬅ Back to Home")
        chatbot_ui = gr.Chatbot(height=420, label="Chat with AI")
        msg = gr.Textbox(placeholder="Ask coding questions...", label="Your Message")
        msg.submit(chatbot, [msg, chatbot_ui], [msg, chatbot_ui])

    # ================= HISTORY TAB (optional) =================
    with gr.Column(visible=False, elem_classes="fade hidden") as history_tab:
        gr.Markdown("### 📜 History")
        back4 = gr.Button("⬅ Back to Home")
        history_box = gr.Textbox(lines=20, label="History")
        load_history_btn = gr.Button("Load History")
        load_history_btn.click(show_history, None, history_box)

    # ================= NAVIGATION LOGIC =================
    def show_columns(front, refine_c, convert_c, chat_c, history_c):
        return (
            front, refine_c, convert_c, chat_c, history_c
        )

    # Front page buttons
    refine_btn.click(lambda: show_columns(False, True, False, False, False),
                     [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])
    convert_btn.click(lambda: show_columns(False, False, True, False, False),
                      [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])
    chat_btn.click(lambda: show_columns(False, False, False, True, False),
                   [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])

    # Back buttons
    back1.click(lambda: show_columns(True, False, False, False, False),
                [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])
    back2.click(lambda: show_columns(True, False, False, False, False),
                [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])
    back3.click(lambda: show_columns(True, False, False, False, False),
                [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])
    back4.click(lambda: show_columns(True, False, False, False, False),
                [], [front_page, refine_tab, convert_tab, chat_tab, history_tab])

# ================= LAUNCH =================
if __name__ == "__main__":
    import gradio
    print("Gradio version:", gradio.__version__)
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )
