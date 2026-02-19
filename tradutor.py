import pysrt
import os
import re
from deep_translator import GoogleTranslator

LIMITE = 4500  # limite seguro por requisição

def limpar_colchetes(texto):
    """
    Remove qualquer conteúdo entre colchetes, inclusive os colchetes.
    Ex: 'Oh, Deus, isso [bip] dói.' -> 'Oh, Deus, isso dói.'
    """
    texto = re.sub(r"\[.*?\]", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto)  # remove espaços extras
    return texto.strip()

def traduzir_srt(
    arquivo_entrada,
    idioma_origem="auto",
    idioma_destino="pt"
):
    subs = pysrt.open(arquivo_entrada, encoding="utf-8")

    tradutor = GoogleTranslator(
        source=idioma_origem,
        target=idioma_destino
    )

    textos = []
    legendas_validas = []

    # Limpa textos e remove legendas vazias
    for s in subs:
        texto = s.text.replace("\n", " ")
        texto = limpar_colchetes(texto)

        if not texto:
            s.text = ""
            continue

        textos.append(texto)
        legendas_validas.append(s)

    # Divide em blocos <= 5000 chars
    blocos = []
    bloco_atual = []
    tamanho_atual = 0

    for texto in textos:
        if tamanho_atual + len(texto) > LIMITE:
            blocos.append(bloco_atual)
            bloco_atual = []
            tamanho_atual = 0

        bloco_atual.append(texto)
        tamanho_atual += len(texto)

    if bloco_atual:
        blocos.append(bloco_atual)

    textos_traduzidos = []

    # Tradução bloco a bloco
    for bloco in blocos:
        traducao = tradutor.translate("\n".join(bloco))
        textos_traduzidos.extend(traducao.split("\n"))

    # Aplica traduções
    for legenda, texto in zip(legendas_validas, textos_traduzidos):
        legenda.text = texto

    # Remove legendas vazias definitivamente
    subs = pysrt.SubRipFile(
        [s for s in subs if s.text.strip()]
    )

    # Pasta "traduzido"
    pasta_origem = os.path.dirname(arquivo_entrada)
    pasta_traduzido = os.path.join(pasta_origem, "traduzido")
    os.makedirs(pasta_traduzido, exist_ok=True)

    arquivo_saida = os.path.join(
        pasta_traduzido,
        os.path.basename(arquivo_entrada)
    )

    subs.save(arquivo_saida, encoding="utf-8")
    return arquivo_saida
