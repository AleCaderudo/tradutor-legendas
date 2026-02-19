# 🎬 Tradutor de Legendas (.srt)

Aplicação desktop em Python com interface gráfica para tradução
automática de legendas `.srt`, com suporte a tradução em lote, barra de
progresso e limpeza automática de descrições sonoras.

------------------------------------------------------------------------

## 🚀 Funcionalidades

✔ Tradução automática utilizando Google Translate (via deep-translator)\
✔ Tradução em lote (vários arquivos `.srt`)\
✔ Barra de progresso (arquivo atual / total)\
✔ Remove descrições sonoras: - Linhas como `[birds chirping]` - Trechos
como `Oh, Deus, isso [bip] dói.`\
✔ Cria automaticamente pasta `traduzido`\
✔ Mantém o mesmo nome dos arquivos originais\
✔ Interface simples e intuitiva\
✔ Versão executável (.exe)

------------------------------------------------------------------------

## 🖥️ Interface

A aplicação possui interface gráfica simples com:

-   Botão para selecionar múltiplas legendas
-   Barra de progresso
-   Status de execução
-   Botão fechar
-   Link para o desenvolvedor

------------------------------------------------------------------------

## 📂 Como funciona

Ao selecionar os arquivos `.srt`, o programa:

1.  Remove textos entre colchetes `[ ... ]`
2.  Divide o conteúdo em blocos seguros (≤ 5000 caracteres)
3.  Traduz automaticamente
4.  Salva o resultado em:

```{=html}
<!-- -->
```
    pasta_original/traduzido/nome_original.srt

Os arquivos originais NÃO são modificados.

------------------------------------------------------------------------

## 📦 Instalação

Clone o repositório:

``` bash
git clone https://github.com/seu-usuario/tradutor-legendas.git
cd tradutor-legendas
```

Crie um ambiente virtual:

``` bash
python -m venv .venv
```

Ative o ambiente:

Windows:

``` bash
.venv\Scripts\activate
```

Instale as dependências:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Executar o programa

``` bash
python Tr.py
```

------------------------------------------------------------------------

## 🏗️ Gerar Executável (.exe)

Instale o PyInstaller:

``` bash
pip install pyinstaller
```

Gere o executável:

``` bash
pyinstaller --onefile --windowed --name TradutorLegendas Tr.py
```

O executável será criado na pasta:

    dist/TradutorLegendas.exe

------------------------------------------------------------------------

## 📁 Estrutura do Projeto

    tradutor-legendas/
    │
    ├── Tr.py
    ├── tradutor.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## 📚 Dependências

-   deep-translator==1.11.4
-   pysrt==1.1.2
-   tkinter (já incluso no Python)

------------------------------------------------------------------------

## ⚠️ Limitações

-   Requer conexão com internet.
-   O Google Translate possui limite de \~5000 caracteres por requisição
    (tratado internamente).
-   A qualidade da tradução depende do serviço externo.

------------------------------------------------------------------------

## 👨‍💻 Desenvolvido por

MHPS\
https://www.mhps.com.br

------------------------------------------------------------------------

## 📜 Licença

Este projeto é disponibilizado para uso pessoal e educacional.

Para uso comercial, verifique os termos de uso do Google Translate.
