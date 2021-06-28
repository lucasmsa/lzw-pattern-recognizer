# lzw-pattern-recognizer

🗜 Implementation of the second project of intro to Information theory at UFPB, plugging an LZW compressor to K-neighboors algorithm

## Equipe

[Lucas Moreira](https://github.com/lucasmsa),
[Marismar Costa](https://github.com/marismarcosta),
[Gustavo Eraldo](https://github.com/gustavoeraldo)

## Introdução

Objetivo do trabalho: Conectar o algoritmo de compressão LZW ao algoritmo k-vizinhos, este utilizado em larga escala para classificar padrões.

## Metodologia

Utilizou o banco de dados **X**, o qual contém 40 pessoas, cada uma com 10 imagens. O cabeçalho do arquivo de dados foi descartado. O projeto foi implementado através da linguagem Python.

A imagem de classificação foi obtida de forma aleatória, as utilizadas para treinamento são todas as outras que não são de classificação. 360 treino, 40 classificação. Dado que o banco tem 40 pessoas e 10 imagens por pessoa, 1 imagem para classificação por pessoa e 9 para treinamento.

Para todos os testes, utilizou-se o intervalo de variacao 9 a 16 para o valor de **k**.

O dicionário permaneceu estático durante todo o processo de classificação.

A métrica de distância utilizada foi a quantidade de índices do dicionário.

## Análise de resultados

No Gráfico 1, é apresentado a curva da **razão de acerto** em função da variação do **k** resultante da aplicação do algoritmo.

<figure>
  <img width="600px" src="./results/hit_rate_x_k.png">
  <figcaption>Gráfico 1 - Razão de acerto por K</figcaption>
</figure>

A taxa de acerto aumenta para números mais altos de **k**. Tendo em vista o gráfico acima, é possível perceber que a taxa de acerto da classificação
aumenta em função do incremento de **k**. Este comportamento condiz com o esperado, visto que
quanto maior for o dicionário, mais abrangente este será e consequentemente mais preciso.

O Gráfico 2 é referente a curva do **tempo de processamento** do código em função da variação do **k**.

<figure>
    <img width="600px" src="./results/time_x_k.png">
    <figcaption>Gráfico 2 - Tempo de processamento por K</figcaption>
</figure>

A curva de tempos de processamento por **k** não apresentou um padrão bem definido. De modo geral, os valores obtidos ficaram entre **40s** e **80s**, sendo a média aproximadamente de **58s**.

## Considerações finais

O trabalho desenvolvido permitiu uma expansão dos conhecimentos abordados em sala de aula, além da visão prática da teoria discutida por autores da literatura.

## Execução do código

Execute no terminal o seguinte comando:

```.bash
python lzw_pattern_recognizer.py
```
