#!/usr/bin/env python3
"""Copia os documentos de docs/ do CrossCheckBR para as páginas do site.

No caminho, cada menção a RF, RNF, RN, HU, IND ou P vira link para a definição.

A fonte da verdade é o repositório CrossCheckBR; as páginas são cópias.
Rode de novo sempre que um documento mudar:

    python3 bin/sync_docs.py /caminho/para/CrossCheckBR
"""
import re
import sys
from pathlib import Path

# arquivo em docs/ -> (página, endereço, título, descrição)
DOCUMENTOS = {
    "ENGENHARIA_DE_REQUISITOS.md": (
        "requisitos.md", "/requisitos/", "Engenharia de Requisitos",
        "Requisitos, histórias de usuário, regras de negócio e pendências, com a situação de cada item no código."),
    "ENGENHARIA_DE_PRODUTO_DE_IA.md": (
        "produto-de-ia.md", "/produto-de-ia/", "Engenharia de Produto de Inteligência Artificial",
        "Canvas do modelo, ciclo de vida, requisitos próprios de inteligência artificial, validação, operação e monitoramento."),
}

CABECALHO = """---
layout: page
permalink: {endereco}
title: "{titulo}"
description: "{descricao}"
nav: false
toc:
  sidebar: left
---

"""

# Alertas do GitHub (> [!NOTE]) viram as caixas de destaque do site.
# Verde: modelo e convergências. Mostarda: diretrizes. Terracota: restrições.
CLASSE_DO_ALERTA = {
    "NOTE": "block-tip",
    "TIP": "block-tip",
    "IMPORTANT": "block-warning",
    "WARNING": "block-danger",
    "CAUTION": "block-danger",
}


def converter_alertas(linhas: list[str]) -> list[str]:
    saida: list[str] = []
    classe = None
    for linha in linhas:
        if classe and not linha.startswith(">"):
            saida.append("{: ." + classe + " }")
            classe = None
        m = re.match(r"^>\s*\[!(\w+)\]\s*$", linha)
        if m and m.group(1).upper() in CLASSE_DO_ALERTA:
            classe = CLASSE_DO_ALERTA[m.group(1).upper()]
            continue  # a linha do marcador não vai para a página
        saida.append(linha)
    if classe:
        saida.append("{: ." + classe + " }")
    return saida


def remover_cabecalho_vazio(linhas: list[str]) -> list[str]:
    """Tabelas de duas colunas sem título: o GitHub exige a linha de cabeçalho
    (| | |), mas no site ela vira uma faixa vazia. O kramdown aceita tabela sem ela."""
    saida: list[str] = []
    i = 0
    while i < len(linhas):
        vazio = re.fullmatch(r"\|(\s*\|)+\s*", linhas[i]) is not None
        separador = i + 1 < len(linhas) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+\s*", linhas[i + 1]) is not None
        if vazio and separador:
            i += 2
            continue
        saida.append(linhas[i])
        i += 1
    return saida


ID = r"(?:RNF|RF|RN|HU|IND|P)\d{2}"
# Trechos que não recebem links: código, links já existentes e etiquetas HTML.
PROTEGIDO = re.compile(r"(`[^`]*`|\[[^\]]*\]\([^)]*\)(?:\{:[^}]*\})?|<[^>]+>)")


def ancora_titulo(titulo: str) -> str:
    """Âncora de um título, como o GitHub e o kramdown geram."""
    t = re.sub(r"[`*_]", "", titulo.strip().lower())
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE)
    return t.replace(" ", "-")


def mapear_definicoes(origem: Path) -> dict[str, tuple[str, str]]:
    """identificador -> (endereço da página, âncora da definição)."""
    defs: dict[str, tuple[str, str]] = {}
    for arquivo, (_, endereco, _, _) in DOCUMENTOS.items():
        for linha in (origem / arquivo).read_text(encoding="utf-8").splitlines():
            m = re.match(rf"^#{{3,4}}\s+((RNF|RF)\d{{2}})\s+—\s+.+$", linha)
            if m:
                defs[m.group(1)] = (endereco, ancora_titulo(linha.lstrip("#")))
                continue
            m = re.match(r"^\|\s*((?:RN|HU|P)\d{2})\s*\|", linha) or re.search(r"(IND\d{2}) ·", linha)
            if m and m.group(1) not in defs:
                defs[m.group(1)] = (endereco, m.group(1).lower())
    return defs


def ligar_identificadores(linhas: list[str], endereco: str, defs: dict) -> list[str]:
    """Cria âncoras nas definições (linhas de tabela e cartões) e transforma cada
    menção a RF, RNF, RN, HU, IND ou P em link para a definição."""
    def alvo(ident: str) -> str:
        pagina, anc = defs[ident]
        return f"#{anc}" if pagina == endereco else f"..{pagina}#{anc}"

    def ligar(trecho: str) -> str:
        partes = PROTEGIDO.split(trecho)
        for i in range(0, len(partes), 2):   # posições pares: texto comum
            partes[i] = re.sub(rf"\b({ID})\b",
                               lambda m: f"[{m.group(1)}]({alvo(m.group(1))}){{: .cc-ref}}"
                               if m.group(1) in defs else m.group(1), partes[i])
        return "".join(partes)

    saida = []
    for linha in linhas:
        if linha.startswith("#"):                      # títulos ficam sem links
            saida.append(linha)
            continue
        if linha.lstrip().startswith("<"):             # bloco HTML: só a âncora dos cartões
            saida.append(re.sub(r'(<span class="cc-kpi-rotulo")>(IND\d{2}) ·',
                                lambda m: f'{m.group(1)} id="{m.group(2).lower()}">{m.group(2)} ·', linha))
            continue
        m = re.match(rf"^(\|\s*)((?:RN|HU|P)\d{{2}})(\s*\|)(.*)$", linha) \
            or re.match(r"^(\|\s*)(IND\d{2})( · [^|]*\|)(.*)$", linha)
        if m and defs.get(m.group(2), (None,))[0] == endereco:   # linha que define o identificador
            ident = m.group(2)
            saida.append(f'{m.group(1)}<span id="{ident.lower()}"></span>{ident}{ligar(m.group(3) + m.group(4))}')
            continue
        saida.append(ligar(linha))
    return saida


def converter_links(texto: str) -> str:
    """Links entre documentos (ARQUIVO.md#secao) viram links entre páginas (../pagina/#secao)."""
    for arquivo, (_, endereco, _, _) in DOCUMENTOS.items():
        texto = texto.replace(f"]({arquivo}", f"](..{endereco}")
    return texto


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    origem = Path(sys.argv[1]) / "docs"
    paginas = Path(__file__).resolve().parent.parent / "_pages"
    defs = mapear_definicoes(origem)
    for arquivo, (pagina, endereco, titulo, descricao) in DOCUMENTOS.items():
        linhas = (origem / arquivo).read_text(encoding="utf-8").splitlines()
        if linhas and linhas[0].startswith("# "):
            linhas = linhas[1:]  # o título vem do cabeçalho da página
        linhas = ligar_identificadores(remover_cabecalho_vazio(converter_alertas(linhas)), endereco, defs)
        corpo = "\n".join(linhas).lstrip("\n") + "\n"
        corpo = converter_links(corpo)
        if "{{" in corpo or "{%" in corpo:
            # chaves do Liquid no documento seriam interpretadas pelo Jekyll
            corpo = "{% raw %}\n" + corpo + "{% endraw %}\n"
        cab = CABECALHO.format(endereco=endereco, titulo=titulo, descricao=descricao)
        (paginas / pagina).write_text(cab + corpo, encoding="utf-8")
        print(f"{arquivo} -> _pages/{pagina} ({len(linhas)} linhas)")


if __name__ == "__main__":
    main()
