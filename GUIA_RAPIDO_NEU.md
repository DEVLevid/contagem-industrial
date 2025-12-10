# Guia Rápido - Processamento do Dataset NEU

> **Nota**: Certifique-se de instalar as dependências primeiro:
> ```bash
> pip install -r requirements.txt
> ```
> Isso instalará o `tqdm` necessário para as barras de progresso.

## Comando Simples

Para processar **todo o dataset NEU** com um único comando:

```bash
python processar_dataset_neu.py
```

Isso processará automaticamente:
- ✅ Diretório `train/` (todas as imagens)
- ✅ Diretório `test/` (todas as imagens)
- ✅ Diretório `valid/` (todas as imagens)
- ✅ Todos os tipos de defeitos (Crazing, Inclusion, Patches, Pitted, Rolled, Scratches)

## Opções Disponíveis

### Básico
```bash
python processar_dataset_neu.py
```

### Personalizado
```bash
# Especificar diretório de saída
python processar_dataset_neu.py -o meus_resultados

# Usar método de segmentação adaptativa
python processar_dataset_neu.py -m adaptive

# Ajustar área mínima (filtrar objetos pequenos)
python processar_dataset_neu.py -a 100

# Processamento mais rápido (sem salvar visualizações)
python processar_dataset_neu.py --sem-visualizacoes
```

### Combinado
```bash
# Todas as opções juntas
python processar_dataset_neu.py -o resultados_final -m adaptive -a 75
```

## No Windows (PowerShell/CMD)

```cmd
# Opção 1: Python direto
python processar_dataset_neu.py

# Opção 2: Usar script batch
processar_neu.bat

# Opção 3: Com parâmetros
python processar_dataset_neu.py -m adaptive -a 100
```

## Estrutura de Saída

Após o processamento, você terá:

```
resultados_neu/
├── imagens_resultado/          # Imagens com objetos marcados
│   ├── Crazing/
│   ├── Inclusion/
│   ├── Patches/
│   ├── Pitted/
│   ├── Rolled/
│   └── Scratches/
├── visualizacoes/              # Visualizações lado a lado
│   └── [mesma estrutura]
├── resultados_completo.json    # Todos os dados detalhados
└── resumo_estatistico.json    # Estatísticas consolidadas
```

## Exemplo de Saída no Terminal

```
================================================================================
PROCESSAMENTO DO DATASET NEU METAL SURFACE DEFECTS
================================================================================
Dataset: NEU Metal Surface Defects Data
Saída: resultados_neu
Método de segmentação: otsu
Área mínima: 50 pixels
================================================================================

================================================================================
PROCESSANDO: TRAIN
================================================================================

Crazing      |████████████████████████████████| 300/300 [00:45<00:00, objetos: 890]
Inclusion    |████████████████████████████████| 300/300 [00:42<00:00, objetos: 920]
Patches      |████████████████████████████████| 300/300 [00:38<00:00, objetos: 850]
Pitted       |████████████████████████████████| 300/300 [00:40<00:00, objetos: 910]
Rolled       |████████████████████████████████| 300/300 [00:43<00:00, objetos: 880]
Scratches    |████████████████████████████████| 300/300 [00:41<00:00, objetos: 870]

================================================================================
RESUMO DO PROCESSAMENTO
================================================================================

📊 ESTATÍSTICAS GERAIS:
  Total de imagens processadas: 1800
  Total de objetos detectados: 5420
  Média de objetos por imagem: 3.01

📁 POR DIRETÓRIO:
  train     :  900 imagens,  2710 objetos (3.01 média)
  test      :  300 imagens,   905 objetos (3.02 média)
  valid     :  600 imagens,  1805 objetos (3.01 média)

🔍 POR TIPO DE DEFEITO:
  Crazing    :  300 imagens,   890 objetos (2.97 média)
  Inclusion  :  300 imagens,   920 objetos (3.07 média)
  ...
```

## Tempo de Processamento

- **Com visualizações**: ~2-5 minutos para 1800 imagens
- **Sem visualizações**: ~1-2 minutos para 1800 imagens

## Dicas

1. **Primeira execução**: Use `--sem-visualizacoes` para testar mais rápido
2. **Análise detalhada**: Deixe as visualizações ativadas para inspeção
3. **Ajuste de parâmetros**: Experimente diferentes valores de `-a` (área mínima)
4. **Métodos**: Teste `-m adaptive` se o método Otsu não funcionar bem

## Solução de Problemas

### Erro: "Dataset não encontrado"
- Verifique se o diretório `NEU Metal Surface Defects Data` está na mesma pasta do script
- Ou use: `python processar_dataset_neu.py -d "caminho/completo/para/dataset"`

### Processamento muito lento
- Use `--sem-visualizacoes` para acelerar
- Use `--sem-imagens-resultado` para acelerar ainda mais

### Muitos/few objetos detectados
- Ajuste a área mínima: `-a 100` (menos objetos) ou `-a 20` (mais objetos)
- Experimente diferentes métodos: `-m adaptive` ou `-m canny`

