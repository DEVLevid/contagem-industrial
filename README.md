# Sistema de Contagem de Objetos em Imagens Industriais

Sistema completo para identificação e contagem de objetos (parafusos, peças, moedas, defeitos) em imagens industriais utilizando técnicas avançadas de processamento de imagem.

## 🎯 Características

- **Segmentação Avançada**: Suporta múltiplos métodos (Otsu, Adaptativa, Canny)
- **Morfologia Matemática**: Operações de abertura e fechamento para limpeza de imagens
- **Componentes Conectados**: Rotulagem e contagem precisa de objetos
- **Processamento em Lote**: Processa múltiplas imagens automaticamente
- **Visualizações Detalhadas**: Gráficos e estatísticas dos objetos detectados
- **Suporte ao Dataset NEU**: Otimizado para o NEU Metal Surface Defects Dataset

## 📋 Requisitos

- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- Matplotlib 3.7+

## 🚀 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Processamento de Imagem Única

```bash
# Processamento básico
python main.py -i caminho/para/imagem.jpg

# Com método de segmentação específico
python main.py -i imagem.jpg -m adaptive

# Ajustando parâmetros
python main.py -i imagem.jpg -a 100 -k 5 --iteracoes 3

# Salvar resultados
python main.py -i imagem.jpg --salvar -o resultados/
```

### Processamento em Lote

```bash
# Processar diretório completo
python main.py -d dataset/ -o resultados/

# Com salvamento automático
python main.py -d dataset/ -o resultados/ --salvar
```

### Parâmetros Disponíveis

- `-i, --imagem`: Caminho para uma única imagem
- `-d, --diretorio`: Caminho para diretório com múltiplas imagens
- `-o, --saida`: Diretório de saída (padrão: `resultados`)
- `-m, --metodo`: Método de segmentação (`otsu`, `adaptive`, `canny`)
- `-a, --area-minima`: Área mínima em pixels (padrão: 50)
- `-k, --kernel-morph`: Tamanho do kernel morfológico (padrão: 3)
- `--iteracoes`: Número de iterações morfológicas (padrão: 2)
- `--sem-visualizacao`: Não exibir visualizações
- `--salvar`: Salvar visualizações e resultados

## 🔬 Métodos de Segmentação

### Otsu (Padrão)
- Melhor para imagens com bom contraste
- Threshold automático baseado em histograma
- Recomendado para a maioria dos casos

### Adaptativa
- Útil para imagens com iluminação variável
- Threshold adaptativo local
- Melhor para condições de iluminação não uniformes

### Canny
- Baseado em detecção de bordas
- Útil para objetos bem definidos
- Pode requerer ajustes de parâmetros

## 📊 Estrutura do Projeto

```
contagem-industrial/
├── main.py                 # Script principal (CLI)
├── contador_objetos.py     # Classe principal de contagem
├── visualizador.py         # Visualização de resultados
├── processador_lote.py     # Processamento em lote
├── requirements.txt        # Dependências
└── README.md              # Documentação
```

## 🎓 Dataset NEU Metal Surface

Este projeto foi otimizado para trabalhar com o [NEU Metal Surface Defects Dataset](https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data).

### Como usar com o dataset NEU:

1. Baixe o dataset do Kaggle
2. Organize as imagens em um diretório:
```
dataset/
├── imagem1.jpg
├── imagem2.jpg
└── ...
```

3. Execute o processamento em lote:
```bash
python main.py -d dataset/ -o resultados_neu/ --salvar
```

## 📈 Saídas do Sistema

O sistema gera:

1. **Imagens Resultado**: Imagens originais com objetos detectados marcados
2. **Visualizações**: Comparação lado a lado (original, segmentação, resultado)
3. **Estatísticas**: Histogramas e gráficos de distribuição de áreas
4. **JSON de Resultados**: Dados estruturados com informações de cada objeto

### Exemplo de Saída JSON:

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

## 🔧 Ajuste de Parâmetros

### Área Mínima (`-a`)
- **Valores baixos** (20-50): Detecta objetos pequenos, mas pode incluir ruído
- **Valores médios** (50-100): Balanceado para a maioria dos casos
- **Valores altos** (100+): Apenas objetos grandes, reduz falsos positivos

### Kernel Morfológico (`-k`)
- **3x3**: Para objetos pequenos e detalhes finos
- **5x5**: Balanceado, remove ruído médio
- **7x7+**: Para objetos grandes, remove ruído grosso

### Iterações (`--iteracoes`)
- **1-2**: Limpeza leve
- **3-5**: Limpeza moderada
- **5+**: Limpeza agressiva (pode remover objetos pequenos)

## 💡 Exemplos de Uso Programático

```python
from contador_objetos import ContadorObjetosIndustrial, MetodoSegmentacao
from visualizador import VisualizadorResultados

# Criar contador
contador = ContadorObjetosIndustrial(
    area_minima=50,
    metodo_segmentacao=MetodoSegmentacao.OTSU
)

# Processar imagem
resultado = contador.processar("imagem.jpg")

# Visualizar
VisualizadorResultados.visualizar(resultado)
```

## 🐛 Solução de Problemas

### Nenhum objeto detectado
- Reduza a área mínima (`-a`)
- Tente método de segmentação diferente (`-m`)
- Verifique se a imagem tem contraste adequado

### Muitos falsos positivos
- Aumente a área mínima (`-a`)
- Aumente o kernel morfológico (`-k`)
- Aumente as iterações (`--iteracoes`)

### Objetos não separados
- Ajuste o kernel morfológico
- Tente método Canny para objetos bem definidos
- Verifique se há sobreposição real dos objetos

## 📝 Licença

Este projeto é fornecido como está, para fins educacionais e de pesquisa.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📚 Referências

- [OpenCV Documentation](https://docs.opencv.org/)
- [NEU Metal Surface Defects Dataset](https://www.kaggle.com/datasets/fantacher/neu-metal-surface-defects-data)
- [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/)

