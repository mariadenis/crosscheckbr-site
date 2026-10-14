# Site do Checa AI

Site de apresentação e documentação do [Checa AI](https://github.com/thiago-cg/Checa-AI),
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
| Documentos (requisitos, versão anterior e produto de IA) | **não edite aqui** (veja abaixo) |
| Logo e favicon | `assets/img/marca/` (azul-petróleo `#155563`) |
| Cores e tipografia | `_sass/_themes.scss` |

O visual (layouts, estilos) vem dos componentes do al-folio e não fica neste
repositório. As regras estão em `AGENTS.md`.

## Páginas de documentação

`requisitos.md`, `requisitos-versao-anterior.md` e `produto-de-ia.md`, em
`_pages/`, são cópias dos documentos de `entrega/requisitos/` do repositório
Checa-AI, que é a fonte da verdade: o relatório de requisitos vigente
(`requisitos.md`) e a versão de 30/09 (`versao-anterior/`). Antes de
sincronizar a versão anterior, confira-a com
`python3 entrega/requisitos/versao-anterior/verificar_docs.py` no Checa-AI. O menu "documentação" é montado em `_pages/documentacao.md`.
Para atualizar:

```bash
python3 bin/sync_docs.py /caminho/para/Checa-AI
```

## Antes de publicar

Em `_config.yml`, ajuste `url` e `baseurl` para o endereço real do GitHub
Pages. O `baseurl` é o nome do repositório onde o site for publicado, com uma
barra na frente. Com o valor errado, o site abre sem estilo e com links
quebrados.

A documentação do template está em `docs/`.
