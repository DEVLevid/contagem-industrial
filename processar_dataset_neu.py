"""
Script para processar todo o dataset NEU Metal Surface Defects Data.
Processa todas as imagens dos diretórios train, test e valid com um único comando.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import cv2
import numpy as np
from tqdm import tqdm
from contador_objetos import ContadorObjetosIndustrial, MetodoSegmentacao
from visualizador import VisualizadorResultados


def converter_para_json_serializavel(obj):
    """
    Converte valores NumPy (int64, float64, etc.) para tipos nativos do Python
    que são serializáveis pelo JSON.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: converter_para_json_serializavel(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [converter_para_json_serializavel(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(converter_para_json_serializavel(item) for item in obj)
    else:
        return obj


class ProcessadorDatasetNEU:
    
    def __init__(
        self,
        caminho_dataset: str = "NEU Metal Surface Defects Data",
        diretorio_saida: str = "resultados_neu",
        area_minima: int = 50,
        metodo_segmentacao: MetodoSegmentacao = MetodoSegmentacao.OTSU,
        salvar_visualizacoes: bool = True,
        salvar_imagens_resultado: bool = True
    ):
        self.caminho_dataset = Path(caminho_dataset)
        self.diretorio_saida = Path(diretorio_saida)
        self.salvar_visualizacoes = salvar_visualizacoes
        self.salvar_imagens_resultado = salvar_imagens_resultado
        
        self.contador = ContadorObjetosIndustrial(
            area_minima=area_minima,
            metodo_segmentacao=metodo_segmentacao
        )
        
        self.tipos_defeitos = ['Crazing', 'Inclusion', 'Patches', 'Pitted', 'Rolled', 'Scratches']
        
        self.diretorios_dataset = ['train', 'test', 'valid']
        
        self.estatisticas_globais = {
            'total_imagens': 0,
            'total_objetos': 0,
            'por_tipo_defeito': defaultdict(lambda: {'imagens': 0, 'objetos': 0}),
            'por_diretorio': defaultdict(lambda: {'imagens': 0, 'objetos': 0}),
            'resultados_detalhados': []
        }
    
    def criar_estrutura_saida(self):
        self.diretorio_saida.mkdir(parents=True, exist_ok=True)
        
        (self.diretorio_saida / 'imagens_resultado').mkdir(exist_ok=True)
        (self.diretorio_saida / 'visualizacoes').mkdir(exist_ok=True)
        
        for tipo in self.tipos_defeitos:
            (self.diretorio_saida / 'imagens_resultado' / tipo).mkdir(exist_ok=True)
            (self.diretorio_saida / 'visualizacoes' / tipo).mkdir(exist_ok=True)
    
    def processar_imagem(self, caminho_imagem: Path, tipo_defeito: str, 
                        diretorio: str) -> dict:
        resultado = self.contador.processar(str(caminho_imagem))
        
        if not resultado:
            return None
        
        nome_base = f"{diretorio}_{tipo_defeito}_{caminho_imagem.stem}"
        
        if self.salvar_imagens_resultado:
            caminho_resultado = (
                self.diretorio_saida / 'imagens_resultado' / tipo_defeito / 
                f'{nome_base}_resultado.jpg'
            )
            cv2.imwrite(str(caminho_resultado), resultado.imagem_resultado)
        
        if self.salvar_visualizacoes:
            caminho_viz = (
                self.diretorio_saida / 'visualizacoes' / tipo_defeito / 
                f'{nome_base}_visualizacao.png'
            )
            VisualizadorResultados.visualizar(
                resultado,
                salvar=True,
                caminho_saida=str(caminho_viz),
                mostrar=False
            )
        
        resultado_dict = {
            'arquivo': caminho_imagem.name,
            'caminho_completo': str(caminho_imagem),
            'tipo_defeito': tipo_defeito,
            'diretorio': diretorio,
            'total_objetos': resultado.total_objetos,
            'estatisticas': resultado.estatisticas,
            'objetos_detectados': resultado.objetos_detectados
        }
        
        return resultado_dict
    
    def processar_diretorio_tipo(self, diretorio: str, tipo_defeito: str) -> list:
        caminho_tipo = self.caminho_dataset / diretorio / tipo_defeito
        
        if not caminho_tipo.exists():
            print(f"  ⚠ Diretório não encontrado: {caminho_tipo}")
            return []
        
        imagens = list(caminho_tipo.glob('*.bmp')) + list(caminho_tipo.glob('*.BMP'))
        
        if not imagens:
            print(f"  ⚠ Nenhuma imagem encontrada em {caminho_tipo}")
            return []
        
        resultados = []
        total_objetos_detectados = 0
        
        # Barra de progresso para este tipo de defeito
        descricao = f"{tipo_defeito:12s}"
        with tqdm(total=len(imagens), desc=descricao, unit="img", 
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]',
                  postfix={'objetos': 0}) as pbar:
            for caminho_imagem in imagens:
                resultado = self.processar_imagem(caminho_imagem, tipo_defeito, diretorio)
                if resultado:
                    resultados.append(resultado)
                    total_objetos_detectados += resultado['total_objetos']
                    pbar.set_postfix({'objetos': total_objetos_detectados})
                pbar.update(1)
        
        return resultados
    
    def processar_dataset_completo(self):
        print("=" * 80)
        print("PROCESSAMENTO DO DATASET NEU METAL SURFACE DEFECTS")
        print("=" * 80)
        print(f"Dataset: {self.caminho_dataset}")
        print(f"Saída: {self.diretorio_saida}")
        print(f"Método de segmentação: {self.contador.metodo_segmentacao.value}")
        print(f"Área mínima: {self.contador.area_minima} pixels")
        print("=" * 80)
        
        self.criar_estrutura_saida()
        
        for diretorio in self.diretorios_dataset:
            print(f"\n{'='*80}")
            print(f"PROCESSANDO: {diretorio.upper()}")
            print(f"{'='*80}")
            
            resultados_diretorio = []
            
            for tipo_defeito in self.tipos_defeitos:
                resultados_tipo = self.processar_diretorio_tipo(diretorio, tipo_defeito)
                resultados_diretorio.extend(resultados_tipo)
                
                if resultados_tipo:
                    self.estatisticas_globais['por_tipo_defeito'][tipo_defeito]['imagens'] += len(resultados_tipo)
                    self.estatisticas_globais['por_tipo_defeito'][tipo_defeito]['objetos'] += sum(
                        r['total_objetos'] for r in resultados_tipo
                    )
            
            if resultados_diretorio:
                self.estatisticas_globais['por_diretorio'][diretorio]['imagens'] = len(resultados_diretorio)
                self.estatisticas_globais['por_diretorio'][diretorio]['objetos'] = sum(
                    r['total_objetos'] for r in resultados_diretorio
                )
            
            self.estatisticas_globais['resultados_detalhados'].extend(resultados_diretorio)
        
        self.estatisticas_globais['total_imagens'] = len(self.estatisticas_globais['resultados_detalhados'])
        self.estatisticas_globais['total_objetos'] = sum(
            r['total_objetos'] for r in self.estatisticas_globais['resultados_detalhados']
        )
        
        self.salvar_resultados()
        
        self.exibir_resumo()
    
    def salvar_resultados(self):
        caminho_json_completo = self.diretorio_saida / 'resultados_completo.json'
        
        # Preparar dados e converter tipos NumPy para tipos nativos
        dados_completos = {
            'metadata': {
                'data_processamento': datetime.now().isoformat(),
                'metodo_segmentacao': self.contador.metodo_segmentacao.value,
                'area_minima': self.contador.area_minima,
                'total_imagens': self.estatisticas_globais['total_imagens'],
                'total_objetos': self.estatisticas_globais['total_objetos']
            },
            'estatisticas': {
                'por_tipo_defeito': dict(self.estatisticas_globais['por_tipo_defeito']),
                'por_diretorio': dict(self.estatisticas_globais['por_diretorio'])
            },
            'resultados_detalhados': self.estatisticas_globais['resultados_detalhados']
        }
        
        # Converter todos os valores NumPy para tipos nativos
        dados_completos = converter_para_json_serializavel(dados_completos)
        
        with open(caminho_json_completo, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resultados completos salvos em: {caminho_json_completo}")
        
        caminho_resumo = self.diretorio_saida / 'resumo_estatistico.json'
        
        # Preparar dados e converter tipos NumPy para tipos nativos
        dados_resumo = {
            'metadata': {
                'data_processamento': datetime.now().isoformat(),
                'metodo_segmentacao': self.contador.metodo_segmentacao.value,
                'area_minima': self.contador.area_minima
            },
            'estatisticas': {
                'total_imagens': self.estatisticas_globais['total_imagens'],
                'total_objetos': self.estatisticas_globais['total_objetos'],
                'media_objetos_por_imagem': (
                    self.estatisticas_globais['total_objetos'] / 
                    self.estatisticas_globais['total_imagens']
                    if self.estatisticas_globais['total_imagens'] > 0 else 0
                ),
                'por_tipo_defeito': dict(self.estatisticas_globais['por_tipo_defeito']),
                'por_diretorio': dict(self.estatisticas_globais['por_diretorio'])
            }
        }
        
        # Converter todos os valores NumPy para tipos nativos
        dados_resumo = converter_para_json_serializavel(dados_resumo)
        
        with open(caminho_resumo, 'w', encoding='utf-8') as f:
            json.dump(dados_resumo, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Resumo estatístico salvo em: {caminho_resumo}")
    
    def exibir_resumo(self):
        print("\n" + "=" * 80)
        print("RESUMO DO PROCESSAMENTO")
        print("=" * 80)
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"  Total de imagens processadas: {self.estatisticas_globais['total_imagens']}")
        print(f"  Total de objetos detectados: {self.estatisticas_globais['total_objetos']}")
        if self.estatisticas_globais['total_imagens'] > 0:
            media = self.estatisticas_globais['total_objetos'] / self.estatisticas_globais['total_imagens']
            print(f"  Média de objetos por imagem: {media:.2f}")
        
        print(f"\n📁 POR DIRETÓRIO:")
        for diretorio in self.diretorios_dataset:
            stats = self.estatisticas_globais['por_diretorio'][diretorio]
            if stats['imagens'] > 0:
                print(f"  {diretorio:10s}: {stats['imagens']:4d} imagens, "
                      f"{stats['objetos']:5d} objetos "
                      f"({stats['objetos']/stats['imagens']:.2f} média)")
        
        print(f"\n🔍 POR TIPO DE DEFEITO:")
        for tipo in self.tipos_defeitos:
            stats = self.estatisticas_globais['por_tipo_defeito'][tipo]
            if stats['imagens'] > 0:
                print(f"  {tipo:12s}: {stats['imagens']:4d} imagens, "
                      f"{stats['objetos']:5d} objetos "
                      f"({stats['objetos']/stats['imagens']:.2f} média)")
        
        print(f"\n📂 RESULTADOS SALVOS EM: {self.diretorio_saida}")
        print("=" * 80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Processar dataset NEU Metal Surface Defects Data completo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Processar com configurações padrão
  python processar_dataset_neu.py
  
  # Especificar diretório de saída
  python processar_dataset_neu.py -o resultados_customizados
  
  # Usar método de segmentação adaptativa
  python processar_dataset_neu.py -m adaptive
  
  # Ajustar área mínima
  python processar_dataset_neu.py -a 100
  
  # Não salvar visualizações (mais rápido)
  python processar_dataset_neu.py --sem-visualizacoes
        """
    )
    
    parser.add_argument(
        '-d', '--dataset',
        type=str,
        default='NEU Metal Surface Defects Data',
        help='Caminho para o diretório do dataset (padrão: "NEU Metal Surface Defects Data")'
    )
    
    parser.add_argument(
        '-o', '--saida',
        type=str,
        default='resultados_neu',
        help='Diretório de saída (padrão: resultados_neu)'
    )
    
    parser.add_argument(
        '-m', '--metodo',
        type=str,
        choices=['otsu', 'adaptive', 'canny'],
        default='otsu',
        help='Método de segmentação (padrão: otsu)'
    )
    
    parser.add_argument(
        '-a', '--area-minima',
        type=int,
        default=50,
        help='Área mínima em pixels (padrão: 50)'
    )
    
    parser.add_argument(
        '--sem-visualizacoes',
        action='store_true',
        help='Não salvar visualizações (processamento mais rápido)'
    )
    
    parser.add_argument(
        '--sem-imagens-resultado',
        action='store_true',
        help='Não salvar imagens com objetos marcados'
    )
    
    args = parser.parse_args()
    
    metodo_map = {
        'otsu': MetodoSegmentacao.OTSU,
        'adaptive': MetodoSegmentacao.ADAPTIVE,
        'canny': MetodoSegmentacao.CANNY
    }
    metodo = metodo_map[args.metodo]
    
    caminho_dataset = Path(args.dataset)
    if not caminho_dataset.exists():
        print(f"❌ Erro: Dataset não encontrado em: {caminho_dataset}")
        print(f"   Verifique o caminho e tente novamente.")
        return
    
    processador = ProcessadorDatasetNEU(
        caminho_dataset=str(caminho_dataset),
        diretorio_saida=args.saida,
        area_minima=args.area_minima,
        metodo_segmentacao=metodo,
        salvar_visualizacoes=not args.sem_visualizacoes,
        salvar_imagens_resultado=not args.sem_imagens_resultado
    )
    
    processador.processar_dataset_completo()
    
    print("\n✅ Processamento concluído com sucesso!")


if __name__ == '__main__':
    main()
