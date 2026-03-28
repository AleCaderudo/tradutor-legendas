import pysrt
import os
import re
from deep_translator import GoogleTranslator

LIMITE = 4500


def limpar_colchetes(texto):
    texto = re.sub(r"<.*?>", "", texto)
    texto = re.sub(r"\[.*?\]", "", texto)
    texto = re.sub(r"\(.*?\)", "", texto)
    texto = re.sub(r"\{.*?\}", "", texto)
    texto = re.sub(r"[♪♫♬]", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()


def dividir_em_blocos(textos, limite=LIMITE):
    blocos = []
    bloco_atual = []
    tamanho_atual = 0

    for texto in textos:
        texto = texto.strip()

        if not texto:
            continue

        adicional = len(texto) + (1 if bloco_atual else 0)

        if tamanho_atual + adicional > limite:
            blocos.append(bloco_atual)
            bloco_atual = [texto]
            tamanho_atual = len(texto)
        else:
            bloco_atual.append(texto)
            tamanho_atual += adicional

    if bloco_atual:
        blocos.append(bloco_atual)

    return blocos


def traduzir_lista_textos(textos, idioma_origem="auto", idioma_destino="pt"):
    tradutor = GoogleTranslator(source=idioma_origem, target=idioma_destino)
    textos_traduzidos = []

    blocos = dividir_em_blocos(textos)

    for bloco in blocos:
        traducao = tradutor.translate("\n".join(bloco))
        textos_traduzidos.extend(traducao.split("\n"))

    return textos_traduzidos


def salvar_traducao(arquivo_original, linhas):
    pasta_origem = os.path.dirname(arquivo_original)
    pasta_traduzido = os.path.join(pasta_origem, "traduzido")
    os.makedirs(pasta_traduzido, exist_ok=True)

    arquivo_saida = os.path.join(
        pasta_traduzido,
        os.path.basename(arquivo_original)
    )

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    return arquivo_saida


def traduzir_legenda(arquivo):
    ext = os.path.splitext(arquivo)[1].lower()

    if ext == ".srt":
        return traduzir_srt(arquivo)
    elif ext == ".ass":
        return traduzir_ass(arquivo)
    elif ext == ".vtt":
        return traduzir_vtt(arquivo)
    else:
        raise Exception("Formato não suportado")


def traduzir_srt(arquivo_entrada, idioma_origem="auto", idioma_destino="pt"):
    subs = pysrt.open(arquivo_entrada, encoding="utf-8")

    textos = []
    legendas_validas = []

    for s in subs:
        texto = s.text.replace("\n", " ")
        texto = limpar_colchetes(texto)

        if not texto:
            s.text = ""
            continue

        textos.append(texto)
        legendas_validas.append(s)

    textos_traduzidos = traduzir_lista_textos(textos, idioma_origem, idioma_destino)

    for legenda, texto in zip(legendas_validas, textos_traduzidos):
        legenda.text = texto

    subs = pysrt.SubRipFile([s for s in subs if s.text.strip()])

    pasta_origem = os.path.dirname(arquivo_entrada)
    pasta_traduzido = os.path.join(pasta_origem, "traduzido")
    os.makedirs(pasta_traduzido, exist_ok=True)

    arquivo_saida = os.path.join(
        pasta_traduzido,
        os.path.basename(arquivo_entrada)
    )

    subs.save(arquivo_saida, encoding="utf-8")
    return arquivo_saida


def traduzir_vtt(arquivo, idioma_origem="auto", idioma_destino="pt"):
    with open(arquivo, encoding="utf-8") as f:
        linhas = f.readlines()

    indices_texto = []
    textos = []

    for i, linha in enumerate(linhas):
        texto = linha.strip()

        if not texto or texto == "WEBVTT" or "-->" in texto:
            continue

        texto_limpo = limpar_colchetes(texto)

        if not texto_limpo:
            linhas[i] = "\n"
            continue

        indices_texto.append(i)
        textos.append(texto_limpo)

    textos_traduzidos = traduzir_lista_textos(textos, idioma_origem, idioma_destino)

    for i, texto_traduzido in zip(indices_texto, textos_traduzidos):
        linhas[i] = texto_traduzido + "\n"

    return salvar_traducao(arquivo, linhas)


def traduzir_ass(arquivo, idioma_origem="auto", idioma_destino="pt"):
    with open(arquivo, encoding="utf-8") as f:
        linhas = f.readlines()

    indices_dialogo = []
    partes_dialogo = []
    textos = []

    for i, linha in enumerate(linhas):
        if linha.startswith("Dialogue:"):
            partes = linha.split(",", 9)

            if len(partes) < 10:
                continue

            texto = partes[-1].strip()
            texto_limpo = limpar_colchetes(texto)

            if not texto_limpo:
                partes[-1] = "\n"
                linhas[i] = ",".join(partes)
                continue

            indices_dialogo.append(i)
            partes_dialogo.append(partes)
            textos.append(texto_limpo)

    textos_traduzidos = traduzir_lista_textos(textos, idioma_origem, idioma_destino)

    for i, partes, texto_traduzido in zip(indices_dialogo, partes_dialogo, textos_traduzidos):
        partes[-1] = texto_traduzido + "\n"
        linhas[i] = ",".join(partes)

    return salvar_traducao(arquivo, linhas)