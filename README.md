# Site do Crosscheck BR

Site de apresentação e documentação do [Crosscheck BR](https://github.com/thiago-cg/CrossCheckBR),
feito com o template [al-folio](https://github.com/alshedivat/al-folio) (Jekyll, licença MIT).

## Rodar localmente

Precisa do Docker aberto.

```bash
docker compose up -d
```

O site fica em <http://localhost:8080/crosscheckbr-site/>. A primeira geração
leva cerca de um minuto. Para parar:

```bash
docker compose down
```

## Onde editar

| O quê | Arquivo |
| --- | --- |
| Nome, descrição, endereço do site | `_config.yml` |
| Página inicial | `_pages/about.md` |
| Como funciona | `_pages/como-funciona.md` |
| Equipe | `_pages/equipe.md` |
| Repositórios exibidos | `_data/repositories.yml` |
| Documentos (requisitos e produto de IA) | **não edite aqui** (veja abaixo) |

O visual (layouts, estilos) vem dos componentes do al-folio e não fica neste
repositório. As regras estão em `AGENTS.md`.

## Páginas de documentação

`requisitos.md` e `produto-de-ia.md`, em `_pages/`, são cópias dos documentos
de `docs/` do repositório CrossCheckBR, que é a fonte da verdade. Antes de
sincronizar, confira os documentos com `python3 docs/verificar_docs.py` no
CrossCheckBR (links, identificadores e números repetidos). O menu "documentação" é montado em `_pages/documentacao.md`.
Para atualizar:

```bash
python3 bin/sync_docs.py /caminho/para/CrossCheckBR
```

## Antes de publicar

Em `_config.yml`, ajuste `url` e `baseurl` para o endereço real do GitHub
Pages. O `baseurl` é o nome do repositório onde o site for publicado, com uma
barra na frente. Com o valor errado, o site abre sem estilo e com links
quebrados.

A documentação do template está em `docs/`.
