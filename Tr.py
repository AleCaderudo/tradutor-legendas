import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import webbrowser

from tradutor import traduzir_srt

def iniciar_traducao():
    arquivos = filedialog.askopenfilenames(
        title="Selecionar legendas",
        filetypes=[("Legendas", "*.srt")]
    )

    if not arquivos:
        return

    progresso["value"] = 0
    progresso["maximum"] = len(arquivos)
    status_label.config(text="Iniciando...")
    botao.config(state="disabled")

    thread = threading.Thread(
        target=traduzir_em_lote,
        args=(arquivos,),
        daemon=True
    )
    thread.start()

def traduzir_em_lote(arquivos):
    erros = []
    total = len(arquivos)

    for i, arquivo in enumerate(arquivos, start=1):
        try:
            traduzir_srt(arquivo)
        except Exception as e:
            erros.append(f"{arquivo}\n{e}")

        janela.after(0, atualizar_progresso, i, total)

    janela.after(0, finalizar, erros, total)

def atualizar_progresso(atual, total):
    progresso["value"] = atual
    status_label.config(
        text=f"Traduzindo arquivo {atual} de {total}"
    )

def finalizar(erros, total):
    botao.config(state="normal")
    status_label.config(text="Concluído")

    if erros:
        messagebox.showwarning(
            "Concluído com erros",
            f"{total - len(erros)} arquivo(s) traduzido(s)\n\nErros:\n\n" +
            "\n\n".join(erros)
        )
    else:
        messagebox.showinfo(
            "Concluído",
            f"{total} arquivo(s) traduzido(s) com sucesso."
        )

def fechar():
    janela.destroy()

# -------- Interface --------

janela = tk.Tk()
janela.title("Tradutor de Legendas")
janela.geometry("300x250")
janela.configure(bg="#B0E0E6")

botao = tk.Button(
    janela,
    text="Selecionar legendas (.srt)",
    command=iniciar_traducao,
    font=("Arial", 11, "bold"),
    width=35,
    height=2
)
botao.pack(padx=20, pady=(20, 10))

progresso = ttk.Progressbar(
    janela,
    orient="horizontal",
    length=300,
    mode="determinate"
)
progresso.pack(padx=20, pady=5)

status_label = tk.Label( janela, text="Aguardando seleção de arquivos" , bg="#B0E0E6")
status_label.pack(pady=(5, 20))

botao_fechar = tk.Button(
    janela, 
    text="Fechar",
    command=fechar,
    width=10,
    height=1
)
botao_fechar.pack( pady=10)

def abrir_link(url):
    webbrowser.open_new_tab(url)

link = tk.Label(text="Desenvolvido por MHPS", bg="#B0E0E6", fg="blue", cursor="hand2")
link.pack(side=tk.BOTTOM, pady=10)
link.bind("<Button-1>", lambda e: abrir_link("https://www.mhps.com.br"))

janela.mainloop()
