---
layout: about
title: Início
permalink: /
subtitle: Checagem cruzada de fatos em larga escala.

selected_papers: false
social: false

announcements:
  enabled: false

latest_posts:
  enabled: false
---

O **Crosscheck BR** é um assistente de checagem de fatos. Você envia o texto, o título ou o link de uma notícia e recebe uma estimativa da **propensão** de aquele conteúdo ser desinformação: baixa, média, alta ou indeterminada. A resposta vem com as evidências encontradas, os endereços das fontes e o passo a passo da análise.

O sistema **não emite veredito**. Ele nunca afirma que algo "é falso" ou "é verdade": mostra os indícios e ajuda você a avaliar.

## O que ele combina

- **Checagens existentes**: o que agências como Lupa, Aos Fatos e Comprova já publicaram sobre a afirmação.
- **Corroboração**: em quantos veículos de comunicação independentes a informação aparece, e se eles concordam entre si.
- **Modelo próprio**: um classificador treinado com textos em português, que estima a probabilidade de o texto ser desinformação.
- **Padrões textuais**: marcas típicas de desinformação, como apelo à urgência e fonte vaga.

## Como usar

Hoje o Crosscheck BR funciona como um robô no Telegram e como uma página na internet. Ele aceita texto, título ou link. Imagens, vídeos e áudios ainda não são analisados.

## Neste site

- [Como funciona]({{ '/como-funciona/' | relative_url }}): as etapas da análise, da mensagem até a resposta.
- [Engenharia de Requisitos]({{ '/requisitos/' | relative_url }}): requisitos, histórias de usuário, regras de negócio e pendências, com a situação de cada item no código.
- [Produto de Inteligência Artificial]({{ '/produto-de-ia/' | relative_url }}): o canvas do modelo, o ciclo de vida, a validação, a operação e o monitoramento.
- [Equipe e repositórios]({{ '/equipe/' | relative_url }}): quem faz o projeto, o código do robô e o conjunto de dados do modelo.
