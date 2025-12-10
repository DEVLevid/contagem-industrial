import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import cv2
from tqdm import tqdm
from src.core.contador import ContadorObjetosIndustrial, MetodoSegmentacao
from src.core.visualizador import VisualizadorResultados
from src.utils.json_utils import converter_para_json_serializavel


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
    
    def processar_imagem(self, caminho_imagem: Path, tipo_defeito: str, diretorio: str) -> dict:
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
        
        dados_completos = converter_para_json_serializavel(dados_completos)
        
        caminho_json_completo = self.diretorio_saida / 'resultados_completo.json'
        with open(caminho_json_completo, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resultados completos salvos em: {caminho_json_completo}")
        
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
        
        dados_resumo = converter_para_json_serializavel(dados_resumo)
        
        caminho_resumo = self.diretorio_saida / 'resumo_estatistico.json'
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

