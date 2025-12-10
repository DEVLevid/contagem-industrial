# Sistema de Contagem de Objetos em Imagens Industriais

Sistema para identificação e contagem de objetos e defeitos em imagens industriais utilizando processamento de imagem com OpenCV.

## Características

- Segmentação com múltiplos métodos (Otsu, Adaptativa, Canny)
- Morfologia matemática para limpeza de imagens
- Rotulagem de componentes conectados
- Processamento em lote automatizado
- Geração de relatórios JSON e estatísticas consolidadas
- Otimizado para o NEU Metal Surface Defects Dataset

## Requisitos

- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- Matplotlib 3.7+
- tqdm 4.65+

## Instalação

```bash
pip install -r requirements.txt
```

## Processamento Técnico

### Pipeline de Processamento

O sistema implementa um pipeline de processamento de imagem para detecção e contagem de objetos:

**1. Pré-processamento**
- Conversão para escala de cinza
- Filtro gaussiano (kernel 5x5) para redução de ruído

**2. Segmentação**
- **Otsu**: Threshold automático baseado em histograma (padrão)
- **Adaptativa**: Threshold local para iluminação não uniforme
- **Canny**: Detecção de bordas com dilatação

**3. Morfologia Matemática**
- Abertura (erosão + dilatação): remove ruído e separa objetos próximos
- Fechamento (dilatação + erosão): preenche buracos e conecta partes
- Kernel configurável (padrão: 3x3) com iterações ajustáveis

**4. Rotulagem de Componentes**
- Algoritmo `cv2.connectedComponentsWithStats` com conectividade 8
- Calcula para cada componente: posição, dimensões, área e centroide

**5. Filtragem**
- Remove objetos abaixo do threshold de área mínima (padrão: 50 pixels)

**6. Geração de Resultados**
- Marcação visual com retângulos e numeração
- Estatísticas: total, média, mediana, min, max, desvio padrão
- Exportação em JSON estruturado

### Processamento do Dataset NEU

O script `processar_dataset_neu.py` automatiza:
- Varredura de diretórios (train, test, valid)
- Processamento por tipo de defeito
- Barras de progresso em tempo real
- Organização automática de resultados
- Consolidação de estatísticas

**Tipos de defeitos**: Crazing, Inclusion, Patches, Pitted, Rolled, Scratches

## Uso

### Processamento de Imagem Única

```bash
python main.py -i caminho/para/imagem.jpg
python main.py -i imagem.jpg -m adaptive -a 100
python main.py -i imagem.jpg --salvar -o resultados/
```

### Processamento em Lote

```bash
python main.py -d dataset/ -o resultados/ --salvar
```

### Processamento Completo do Dataset NEU

```bash
# Processamento padrão
python processar_dataset_neu.py

# Processamento rápido (recomendado)
python processar_dataset_neu.py --sem-visualizacoes

# Com opções personalizadas
python processar_dataset_neu.py --sem-visualizacoes -m adaptive -a 75 -o resultados_customizados
```

O comando `--sem-visualizacoes` processa mais rapidamente, gerando:
- Imagens com defeitos marcados
- Arquivos JSON com dados completos
- Estatísticas consolidadas
- Barras de progresso em tempo real

### Parâmetros

- `-i, --imagem`: Caminho para imagem única
- `-d, --diretorio`: Diretório com múltiplas imagens
- `-o, --saida`: Diretório de saída (padrão: `resultados`)
- `-m, --metodo`: Segmentação (`otsu`, `adaptive`, `canny`)
- `-a, --area-minima`: Área mínima em pixels (padrão: 50)
- `-k, --kernel-morph`: Tamanho do kernel morfológico (padrão: 3)
- `--iteracoes`: Iterações morfológicas (padrão: 2)
- `--sem-visualizacoes`: Não salvar visualizações
- `--sem-imagens-resultado`: Não salvar imagens marcadas

## Métodos de Segmentação

**Otsu**: Threshold automático baseado em histograma. Recomendado para a maioria dos casos.

**Adaptativa**: Threshold local adaptativo. Útil para iluminação não uniforme.

**Canny**: Detecção de bordas. Adequado para objetos com bordas bem definidas.

## Estrutura do Projeto

```
contagem-industrial/
├── main.py                      # Script principal (CLI)
├── contador_objetos.py          # Classe principal de contagem
├── visualizador.py              # Visualização de resultados
├── processador_lote.py          # Processamento em lote
├── processar_dataset_neu.py     # Processamento completo do dataset NEU
├── requirements.txt             # Dependências
└── README.md                    # Documentação
```

## Saídas do Sistema

**Estrutura de saída do dataset NEU:**
```
resultados_neu/
├── imagens_resultado/
│   ├── Crazing/
│   ├── Inclusion/
│   ├── Patches/
│   ├── Pitted/
│   ├── Rolled/
│   └── Scratches/
├── visualizacoes/
├── resultados_completo.json
└── resumo_estatistico.json
```

**Formato JSON:**
```json
{
  "arquivo": "imagem.jpg",
  "total_objetos": 15,
  "estatisticas": {
    "total": 15,
    "area_media": 234.5,
    "area_mediana": 220.0,
    "area_min": 120,
    "area_max": 450,
    "desvio_padrao": 89.3
  },
  "objetos_detectados": [
    {
      "id": 1,
      "x": 50,
      "y": 50,
      "width": 20,
      "height": 20,
      "area": 400,
      "centroid": [60.0, 60.0]
    }
  ]
}
```

## Ajuste de Parâmetros

**Área Mínima (`-a`)**
- 20-50: Detecta objetos pequenos (pode incluir ruído)
- 50-100: Balanceado (recomendado)
- 100+: Apenas objetos grandes (reduz falsos positivos)

**Kernel Morfológico (`-k`)**
- 3x3: Objetos pequenos e detalhes finos
- 5x5: Balanceado
- 7x7+: Objetos grandes

**Iterações (`--iteracoes`)**
- 1-2: Limpeza leve
- 3-5: Limpeza moderada
- 5+: Limpeza agressiva

## Uso Programático

```python
from contador_objetos import ContadorObjetosIndustrial, MetodoSegmentacao
from visualizador import VisualizadorResultados

contador = ContadorObjetosIndustrial(
    area_minima=50,
    metodo_segmentacao=MetodoSegmentacao.OTSU
)

resultado = contador.processar("imagem.jpg")
VisualizadorResultados.visualizar(resultado)
```

## Solução de Problemas

**Nenhum objeto detectado**
- Reduza a área mínima (`-a`)
- Tente método de segmentação diferente (`-m`)
- Verifique contraste da imagem

**Muitos falsos positivos**
- Aumente a área mínima (`-a`)
- Aumente o kernel morfológico (`-k`)
- Aumente as iterações (`--iteracoes`)

**Objetos não separados**
- Ajuste o kernel morfológico
- Use método Canny para objetos bem definidos

## Referências

- [OpenCV Documentation](https://docs.opencv.org/)
- [NEU Metal Surface Defects Dataset](https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data)
- [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/)

## Licença

Este projeto é fornecido como está, para fins educacionais e de pesquisa.
