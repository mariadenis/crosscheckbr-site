---
layout: about
title: Início
permalink: /
subtitle: Recebeu uma mensagem e ficou na dúvida? Checa AI.

selected_papers: false
social: false

announcements:
  enabled: false

latest_posts:
  enabled: false
---

O **Checa AI** é um assistente de checagem de fatos. Você envia o texto, o título ou o link de uma notícia e recebe uma estimativa da **propensão** de aquele conteúdo ser desinformação: baixa, média, alta ou indeterminada. A resposta vem com as fontes que embasam a estimativa, o que cada uma diz e o passo a passo da análise.

O sistema **não emite veredito**. Ele nunca afirma que algo "é falso" ou "é verdade": mostra os indícios e ajuda você a avaliar.

## De onde vem a estimativa

- **Checagens de agências**: o que Lupa, Aos Fatos, Boatos.org, AFP Checamos, UOL Confere, Comprova, G1 Fato ou Fake, Estadão Verifica e E-Farsas já publicaram sobre a afirmação. O selo aparece sempre atribuído à agência.
- **Notícias na web**: o que os veículos publicaram, lido por inteiro e avaliado frente à afirmação (confirma, contesta ou só relata), com um trecho citado que o sistema confere na página.
- **Fontes independentes**: republicações e veículos do mesmo grupo contam uma vez só.

O modelo próprio de aprendizado de máquina e os padrões textuais (apelo à urgência, fonte vaga) aparecem na resposta como sinais de estilo, mas **não alteram a estimativa**.

## Como usar

O Checa AI funciona como um robô no Telegram e como uma página na internet. Ele aceita texto, título ou link. Imagens, vídeos e áudios não são analisados: você recebe uma orientação sobre o que enviar.

## Neste site

- [Como funciona]({{ '/como-funciona/' | relative_url }}): as etapas da análise, da mensagem até a resposta.
- [Requisitos]({{ '/requisitos/' | relative_url }}): requisitos funcionais e não funcionais, regras de negócio e pendências, com o status de cada item no código.
- [Produto de Inteligência Artificial]({{ '/produto-de-ia/' | relative_url }}): o canvas do modelo, o ciclo de vida, a validação, a operação e o monitoramento.
- [Equipe e repositórios]({{ '/equipe/' | relative_url }}): quem faz o projeto, o código do robô e o conjunto de dados do modelo.
