# Sistema de Contagem de Objetos em Imagens Industriais

Sistema para identificação e contagem de objetos e defeitos em imagens industriais utilizando processamento de imagem com OpenCV.

## Estrutura do Projeto

```
contagem-industrial/
├── src/
│   ├── core/              # Módulos principais
│   │   ├── contador.py    # Processamento de imagens
│   │   └── visualizador.py # Visualização de resultados
│   ├── processors/        # Processadores
│   │   ├── lote.py        # Processamento em lote
│   │   └── dataset_neu.py # Processamento dataset NEU
│   └── utils/             # Utilitários
│       └── json_utils.py  # Conversão JSON
├── scripts/               # Scripts executáveis
│   ├── main.py           # CLI principal
│   └── processar_dataset_neu.py
├── docs/                  # Documentação
├── requirements.txt
└── README.md
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Processamento de Imagem Única

```bash
python scripts/main.py -i imagem.jpg
```

### Processamento em Lote

```bash
python scripts/main.py -d dataset/ -o resultados/
```

### Processamento Dataset NEU

```bash
python scripts/processar_dataset_neu.py --sem-visualizacoes
```

## Requisitos

- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- Matplotlib 3.7+
- tqdm 4.65+

