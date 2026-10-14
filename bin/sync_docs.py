#!/usr/bin/env python3
"""Copia os documentos de requisitos do repositório do Checa AI para as páginas do site.

No caminho, cada menção a RF, RNF, RN, HU, IND ou P vira link para a definição. Um
identificador definido na própria página aponta para ela; senão, para o primeiro documento
de DOCUMENTOS que o define (os requisitos vigentes vêm primeiro).

A fonte da verdade é o repositório do Checa AI (pasta entrega/requisitos/); as páginas são
cópias. Rode de novo sempre que um documento mudar:

    python3 bin/sync_docs.py /caminho/para/Checa-AI
"""
import posixpath
import re
import sys
from pathlib import Path

# caminho no repositório -> (página, endereço, título, descrição, versão anterior?)
DOCUMENTOS = {
    "entrega/requisitos/requisitos.md": (
        "requisitos.md", "/requisitos/", "Requisitos",
        "Requisitos funcionais e não funcionais, regras de negócio e pendências do Checa AI, "
        "com o status de cada item no código.", False),
    "entrega/organizacao/organizacao.md": (
        "organizacao.md", "/organizacao/", "Organização, Scrum e papéis",
        "Papéis do Scrum, frentes de cada integrante, forma de trabalho e linha do tempo do Checa AI.", False),
    "entrega/requisitos/versao-anterior/ENGENHARIA_DE_REQUISITOS.md": (
        "requisitos-versao-anterior.md", "/requisitos/versao-anterior/",
        "Engenharia de Requisitos (versão de 30/09/2026)",
        "Versão anterior dos requisitos, com histórias de usuário, indicadores e métricas do modelo.", True),
    "entrega/requisitos/versao-anterior/ENGENHARIA_DE_PRODUTO_DE_IA.md": (
        "produto-de-ia.md", "/produto-de-ia/", "Engenharia de Produto de Inteligência Artificial",
        "Canvas do modelo, ciclo de vida, validação, operação e monitoramento (versão de 30/09/2026).", True),
}

# Faixa no topo dos documentos da versão anterior: os requisitos vigentes estão em /requisitos/.
AVISO_VERSAO_ANTERIOR = (
    "> **Versão de 30/09/2026.** Os requisitos funcionais e não funcionais e as regras de negócio "
    "vigentes estão em [Requisitos]({requisitos}), versão 2.0, que substitui os requisitos desta "
    "página. Ela continua publicada pelo conteúdo que a versão 2.0 não repete e pelo histórico.\n"
    "{: .block-warning }\n\n")

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


def relativo(destino: str, origem: str) -> str:
    """Endereço de `destino` visto da página `origem` (ambos como "/a/b/"), sempre com barra final."""
    r = posixpath.relpath(destino, origem)
    return "" if r == "." else r + "/"


def ancora_titulo(titulo: str) -> str:
    """Âncora de um título, como o GitHub e o kramdown geram."""
    t = re.sub(r"[`*_]", "", titulo.strip().lower())
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE)
    return t.replace(" ", "-")


def mapear_definicoes(origem: Path) -> dict[str, list[tuple[str, str]]]:
    """identificador -> [(endereço da página, âncora da definição)], na ordem de DOCUMENTOS."""
    defs: dict[str, list[tuple[str, str]]] = {}
    for arquivo, (_, endereco, _, _, _) in DOCUMENTOS.items():
        for linha in (origem / arquivo).read_text(encoding="utf-8").splitlines():
            m = re.match(rf"^#{{3,4}}\s+((RNF|RF)\d{{2}})\s+—\s+.+$", linha)
            if m:
                defs.setdefault(m.group(1), []).append((endereco, ancora_titulo(linha.lstrip("#"))))
                continue
            m = re.match(r"^\|\s*((?:RNF|RF|RN|HU|P)\d{2})\s*\|", linha) or re.search(r"(IND\d{2}) ·", linha)
            if m and endereco not in [e for e, _ in defs.get(m.group(1), [])]:
                defs.setdefault(m.group(1), []).append((endereco, m.group(1).lower()))
    return defs


def definicao(ident: str, endereco: str, defs: dict) -> tuple[str, str] | None:
    """A definição na própria página, se houver; senão a primeira (requisitos vigentes)."""
    opcoes = defs.get(ident) or []
    return next((d for d in opcoes if d[0] == endereco), opcoes[0] if opcoes else None)


def ligar_identificadores(linhas: list[str], endereco: str, defs: dict) -> list[str]:
    """Cria âncoras nas definições (linhas de tabela e cartões) e transforma cada
    menção a RF, RNF, RN, HU, IND ou P em link para a definição."""
    def alvo(ident: str) -> str:
        pagina, anc = definicao(ident, endereco, defs)
        return f"#{anc}" if pagina == endereco else f"{relativo(pagina, endereco)}#{anc}"

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
        m = re.match(rf"^(\|\s*)((?:RNF|RF|RN|HU|P)\d{{2}})(\s*\|)(.*)$", linha) \
            or re.match(r"^(\|\s*)(IND\d{2})( · [^|]*\|)(.*)$", linha)
        if m and (definicao(m.group(2), endereco, defs) or (None,))[0] == endereco:   # linha que define o identificador
            ident = m.group(2)
            saida.append(f'{m.group(1)}<span id="{ident.lower()}"></span>{ident}{ligar(m.group(3) + m.group(4))}')
            continue
        saida.append(ligar(linha))
    return saida


def converter_links(texto: str, origem: str) -> str:
    """Links entre documentos ([…](pasta/ARQUIVO.md#secao)) viram links entre páginas, relativos à página `origem`."""
    for arquivo, (_, endereco, _, _, _) in DOCUMENTOS.items():
        nome = re.escape(Path(arquivo).name)
        texto = re.sub(rf"\]\((?:[\w./-]*/)?{nome}", f"]({relativo(endereco, origem)}", texto)
    return texto


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    origem = Path(sys.argv[1])
    paginas = Path(__file__).resolve().parent.parent / "_pages"
    defs = mapear_definicoes(origem)
    for arquivo, (pagina, endereco, titulo, descricao, anterior) in DOCUMENTOS.items():
        linhas = (origem / arquivo).read_text(encoding="utf-8").splitlines()
        if linhas and linhas[0].startswith("# "):
            linhas = linhas[1:]  # o título vem do cabeçalho da página
        linhas = ligar_identificadores(remover_cabecalho_vazio(converter_alertas(linhas)), endereco, defs)
        corpo = "\n".join(linhas).lstrip("\n") + "\n"
        corpo = converter_links(corpo, endereco)
        if "{{" in corpo or "{%" in corpo:
            # chaves do Liquid no documento seriam interpretadas pelo Jekyll
            corpo = "{% raw %}\n" + corpo + "{% endraw %}\n"
        if anterior:
            corpo = AVISO_VERSAO_ANTERIOR.replace("{requisitos}", relativo("/requisitos/", endereco)) + corpo
        cab = CABECALHO.format(endereco=endereco, titulo=titulo, descricao=descricao)
        (paginas / pagina).write_text(cab + corpo, encoding="utf-8")
        print(f"{arquivo} -> _pages/{pagina} ({len(linhas)} linhas)")


if __name__ == "__main__":
    main()
