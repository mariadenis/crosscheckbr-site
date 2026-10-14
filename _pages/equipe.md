---
layout: page
permalink: /equipe/
title: Equipe e Repositórios 
description: Quem faz o Checa AI.
nav: true
nav_order: 3
---
## Equipe 

O **Product Owner** do projeto são os mentores do programa, que propuseram o desafio e avaliam as entregas. Os papéis, as frentes de cada integrante e a forma de trabalho estão em [Organização, Scrum e papéis]({{ '/organizacao/' | relative_url }}).

| Foto | Integrante | GitHub | Papel |
| :---: | :--- | :---: | :---: | :--- |
| <img src="https://github.com/github.png" width="50" style="border-radius: 50%;"> | Daltro Oliveira Vinuto | - | Scrum Master |
| <img src="https://github.com/mariadenis.png" width="50" style="border-radius: 50%;"> | Maria Eduarda Denis Duarte Marques | [@mariadenis](https://github.com/mariadenis) | Time de Desenvolvimento |
| <img src="https://github.com/thiago-cg.png" width="50" style="border-radius: 50%;"> | Thiago Correia Gonzaga | [@thiago-cg](https://github.com/thiago-cg) | Time de Desenvolvimento |
| <img src="https://github.com/github.png" width="50" style="border-radius: 50%;"> | Gabriella Oliveira de Souza Dias | - | Time de Desenvolvimento |
| <img src="https://github.com/github.png" width="50" style="border-radius: 50%;"> | Guilherme Silva Dutra | - | Time de Desenvolvimento |
| <img src="https://github.com/github.png" width="50" style="border-radius: 50%;"> | Eliane Orlandin do Carmo | - | Time de Desenvolvimento |

## Repositórios 

O projeto tem dois repositórios. O **Checa-AI** é o robô: recebe a notícia, consulta as fontes e monta a resposta. O **FakenewsBR** reúne o conjunto de dados em português e o modelo de detecção treinado com ele.

{% if site.data.repositories.github_repos %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}


Dúvidas e sugestões: abra uma issue no [repositório do projeto](https://github.com/thiago-cg/Checa-AI).


