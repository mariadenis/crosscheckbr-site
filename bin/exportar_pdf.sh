#!/usr/bin/env bash
# Exporta a página de requisitos em PDF (A4, margens de 2,5 cm, logo no topo).
# Precisa do site rodando (docker compose up -d) e do Node.js.
#   bin/exportar_pdf.sh [arquivo-de-saida.pdf]
set -euo pipefail
SAIDA="${1:-ENGENHARIA_DE_REQUISITOS.pdf}"
URL="${URL:-http://127.0.0.1:8080/crosscheckbr-site/requisitos/}"
npx -y playwright@latest install chromium >/dev/null
npx -y playwright@latest pdf --paper-format=A4 --wait-for-timeout=3000 "$URL" "$SAIDA"
echo "PDF salvo em $SAIDA"
