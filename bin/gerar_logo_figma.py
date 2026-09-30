#!/usr/bin/env python3
"""Gera os SVGs do logotipo do site a partir das medidas da prancha no Figma.

Prancha: "CrossCheck BR — Identidade Visual", bloco 01 Logotipo (assinatura 478 x 85).
Símbolo: grade 3 x 3 com moldura, check Verde Oliva e linha diagonal que o cruza.
Wordmark: "Crosscheck" em Playfair Display SemiBold 64 (-1,5%), "BR" em Inter
Semi Bold 15 (+12%) dentro de uma etiqueta com borda de 1 px.

    pip install fonttools
    python3 bin/gerar_logo_figma.py --playfair "PlayfairDisplay[wght].ttf" --inter "Inter[opsz,wght].ttf"

Fontes (SIL OFL): https://github.com/google/fonts/tree/main/ofl
"""
from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SAIDA = Path(__file__).resolve().parent.parent / "assets" / "img" / "marca"
TINTA, PAPEL, OLIVA, OLIVA_CLARO = "#1A1D20", "#F8F7F4", "#2E6F40", "#7FB88D"


def simbolo(tinta: str, check: str, dx: float = 0, dy: float = 0, k: float = 0.6) -> str:
    """Símbolo de 120 unidades, escalado por k (0,6 = 72 px, como na assinatura)."""
    return (f'<g transform="translate({dx} {dy}) scale({k})" fill="none">'
            f'<rect x="1" y="1" width="118" height="118" stroke="{tinta}" stroke-width="2"/>'
            f'<path d="M40 1V119M80 1V119M1 40H119M1 80H119" stroke="{tinta}" stroke-opacity="0.22" stroke-width="1.5"/>'
            f'<path d="M24 62L50 88L98 30" stroke="{check}" stroke-width="13"/>'
            f'<path d="M62 28L96 84" stroke="{tinta}" stroke-width="3"/></g>')


class Texto:
    def __init__(self, caminho: str, eixos: dict):
        f = instantiateVariableFont(TTFont(caminho), eixos)
        self.g, self.cmap, self.upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm

    def contorno(self, texto: str, tam: float, x: float, base: float, espaco_em: float) -> tuple[str, float]:
        k, partes, cur = tam / self.upm, [], x
        for ch in texto:
            nome = self.cmap[ord(ch)]
            pen = SVGPathPen(self.g)
            self.g[nome].draw(TransformPen(pen, (k, 0, 0, -k, cur, base)))
            partes.append(pen.getCommands())
            cur += self.g[nome].width * k + espaco_em * tam   # o Figma aplica o espaçamento após cada letra
        return "".join(partes), cur - x


def assinatura(pf: Texto, it: Texto, tinta: str, check: str) -> str:
    alt = 85
    d1, w1 = pf.contorno("Crosscheck", 64, 94, 69, -0.015)       # 72 do símbolo + 22 de intervalo
    x_tag = 94 + w1 + 12
    d2, w2 = it.contorno("BR", 15, x_tag + 9.5, 47.5, 0.12)      # margem interna de 9 + meia borda
    larg_tag = round(9 + w2 + 9)
    largura = x_tag + larg_tag + 0.5
    corpo = (simbolo(tinta, check, 0, 6.5)
             + f'<path d="{d1}" fill="{tinta}"/>'
             + f'<rect x="{x_tag + 0.5:.2f}" y="28" width="{larg_tag}" height="29" stroke="{tinta}" fill="none"/>'
             + f'<path d="{d2}" fill="{tinta}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura:.2f} {alt}" width="{largura:.0f}" '
            f'height="{alt}" role="img" aria-label="Crosscheck BR"><title>Crosscheck BR</title>{corpo}</svg>\n')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--playfair", required=True)
    ap.add_argument("--inter", required=True)
    a = ap.parse_args()
    pf = Texto(a.playfair, {"wght": 600})
    it = Texto(a.inter, {"wght": 600, "opsz": 14})
    SAIDA.mkdir(parents=True, exist_ok=True)
    arquivos = {
        "crosscheck-br-horizontal-positiva.svg": assinatura(pf, it, TINTA, OLIVA),
        "crosscheck-br-horizontal-negativa.svg": assinatura(pf, it, PAPEL, OLIVA_CLARO),
        "simbolo-positiva.svg": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120" '
                                 'role="img" aria-label="Crosscheck BR"><title>Crosscheck BR</title>'
                                 + simbolo(TINTA, OLIVA, k=1) + "</svg>\n"),
        # ícone da aba: símbolo sobre Papel, para aparecer também em abas escuras
        "icone.svg": ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 136 136" width="136" height="136" '
                      'role="img" aria-label="Crosscheck BR"><title>Crosscheck BR</title>'
                      f'<rect width="136" height="136" fill="{PAPEL}"/>' + simbolo(TINTA, OLIVA, 8, 8, 1) + "</svg>\n"),
    }
    for nome, svg in arquivos.items():
        (SAIDA / nome).write_text(svg, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
