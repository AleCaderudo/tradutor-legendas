import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import webbrowser

from tkinterdnd2 import TkinterDnD, DND_FILES
from tradutor import traduzir_legenda


def buscar_legendas_em_pasta(pasta):
    arquivos = []
    for root, dirs, files in os.walk(pasta):
        for f in files:
            if f.lower().endswith((".srt", ".ass", ".vtt")):
                arquivos.append(os.path.join(root, f))
    return arquivos


def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(
        title="Selecionar legendas",
        filetypes=[("Legendas", "*.srt *.ass *.vtt")]
    )

    if arquivos:
        iniciar_traducao(list(arquivos))


def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecionar pasta")

    if not pasta:
        return

    arquivos = buscar_legendas_em_pasta(pasta)

    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhum arquivo de legenda encontrado.")
        return

    iniciar_traducao(arquivos)


def arquivos_arrastados(event):
    caminhos = janela.tk.splitlist(event.data)
    arquivos = []

    for caminho in caminhos:
        if os.path.isdir(caminho):
            arquivos.extend(buscar_legendas_em_pasta(caminho))
        elif caminho.lower().endswith((".srt", ".ass", ".vtt")):
            arquivos.append(caminho)

    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhum arquivo de legenda encontrado.")
        return

    iniciar_traducao(arquivos)


def iniciar_traducao(arquivos):
    progresso["value"] = 0
    progresso["maximum"] = len(arquivos)

    status_label.config(text=f"Preparando {len(arquivos)} arquivo(s)...")
    botao_arquivo.config(state="disabled")
    botao_pasta.config(state="disabled")

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
        nome = os.path.basename(arquivo)

        janela.after(0, status_label.config, {
            "text": f"Traduzindo {i} de {total}: {nome}"
        })

        try:
            traduzir_legenda(arquivo)
        except Exception as e:
            erros.append(f"{arquivo}\n{e}")

        janela.after(0, atualizar_progresso, i, total)

    janela.after(0, finalizar, erros, total)


def atualizar_progresso(atual, total):
    progresso["value"] = atual
    status_label.config(text=f"Concluído {atual} de {total}")


def finalizar(erros, total):
    botao_arquivo.config(state="normal")
    botao_pasta.config(state="normal")

    status_label.config(text="Concluído")

    if erros:
        messagebox.showwarning(
            "Concluído com erros",
            f"{total - len(erros)} arquivo(s) traduzido(s).\n\nErros:\n\n" +
            "\n\n".join(erros)
        )
    else:
        messagebox.showinfo(
            "Concluído",
            f"{total} arquivo(s) traduzido(s) com sucesso."
        )


def fechar():
    janela.destroy()


def abrir_link(url):
    webbrowser.open_new_tab(url)


janela = TkinterDnD.Tk()
janela.title("Tradutor de Legendas: 2.0")
janela.geometry("600x360")
janela.configure(bg="#B0E0E6")

titulo = tk.Label(
    janela,
    text="Tradutor de Legendas",
    font=("Arial", 16, "bold"),
    bg="#B0E0E6"
)
titulo.pack(pady=10)

botao_arquivo = tk.Button(
    janela,
    text="Selecionar arquivos .srt / .ass / .vtt",
    command=selecionar_arquivos,
    width=30,
    height=2
)
botao_arquivo.pack(pady=5)

botao_pasta = tk.Button(
    janela,
    text="Selecionar pasta",
    command=selecionar_pasta,
    width=30,
    height=2
)
botao_pasta.pack(pady=5)

drag_label = tk.Label(
    janela,
    text="ou arraste arquivos / pastas aqui",
    bg="#B0E0E6",
    font=("Arial", 10, "italic")
)
drag_label.pack(pady=10)

progresso = ttk.Progressbar(
    janela,
    orient="horizontal",
    length=350,
    mode="determinate"
)
progresso.pack(pady=10)

status_label = tk.Label(
    janela,
    text="Aguardando arquivos...",
    bg="#B0E0E6"
)
status_label.pack()

botao_fechar = tk.Button(
    janela,
    text="Fechar",
    command=fechar,
    width=10
)
botao_fechar.pack(pady=15)

link = tk.Label(
    text="Desenvolvido por MHPS",
    bg="#B0E0E6",
    fg="blue",
    cursor="hand2"
)
link.pack(side=tk.BOTTOM, pady=5)
link.bind("<Button-1>", lambda e: abrir_link("https://www.mhps.com.br"))

janela.drop_target_register(DND_FILES)
janela.dnd_bind("<<Drop>>", arquivos_arrastados)

janela.mainloop()