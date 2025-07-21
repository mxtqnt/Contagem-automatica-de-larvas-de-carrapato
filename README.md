# Contagem Automática de Larvas de Carrapato

## Objetivo

Este repositório apresenta um sistema automatizado para análise e contagem de larvas de carrapato em vídeos, distinguindo entre larvas vivas e mortas. A ferramenta é destinada a facilitar pesquisas e monitoramentos em ambientes laboratoriais, proporcionando uma análise rápida e precisa do comportamento dos parasitas.

## Descrição

O sistema processa vídeos armazenados em uma pasta específica, executando as seguintes etapas:

- Corte e pré-processamento dos frames do vídeo para focar nas regiões de interesse.
- Identificação do número mais recorrente de larvas detectadas por frame.
- Determinação do maior intervalo sequencial em que a contagem é consistente.
- Análise detalhada para classificação das larvas como vivas ou mortas com base em movimento e comportamento.
- Geração de uma planilha CSV com os resultados da análise, incluindo contagem de larvas vivas, mortas e tempo total de processamento.

Além disso, para cada vídeo, imagens ou vídeos são gerados destacando as larvas mortas para facilitar validação visual dos resultados.

## Estrutura do Repositório

- `videos/` – Pasta contendo os vídeos originais a serem analisados.
- `tratamento.py` – Funções para corte e pré-processamento dos vídeos.
- `selecao.py` – Algoritmos para identificar contagens recorrentes e intervalos sequenciais.
- `analisar.py` – Funções para acompanhamento e classificação das larvas ao longo dos frames.
- `AnaliseVideos.csv` – Arquivo gerado com o resumo das análises após execução.
  

<img src="https://github.com/mxtqnt/Contagem-automatica-de-larvas-de-carrapato/blob/main/imgreadme/original.png?raw=true" alt="frame original" width="25%%" height="25%">

<img src="https://github.com/mxtqnt/Contagem-automatica-de-larvas-de-carrapato/blob/main/imgreadme/contagem.png?raw=true" alt="frame tratado" width="25%" height="25%">

<img src="https://github.com/mxtqnt/Contagem-automatica-de-larvas-de-carrapato/blob/main/imgreadme/circuladas.png?raw=true" alt="larvas circuladas" width="25%" height="25%">
