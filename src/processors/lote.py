import json
from pathlib import Path
from typing import List, Dict, Optional
import cv2
from src.core.contador import ContadorObjetosIndustrial
from src.core.visualizador import VisualizadorResultados


class ProcessadorLote:
    def __init__(self, contador: ContadorObjetosIndustrial):
        self.contador = contador
        self.resultados: List[Dict] = []
    
    def processar_diretorio(
        self, 
        diretorio_entrada: str,
        diretorio_saida: Optional[str] = None,
        extensoes: List[str] = None,
        salvar_visualizacoes: bool = True,
        salvar_resultados: bool = True
    ) -> List[Dict]:
        if extensoes is None:
            extensoes = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        
        diretorio_entrada = Path(diretorio_entrada)
        if not diretorio_entrada.exists():
            print(f"Erro: Diretório não encontrado: {diretorio_entrada}")
            return []
        
        if diretorio_saida:
            diretorio_saida = Path(diretorio_saida)
            diretorio_saida.mkdir(parents=True, exist_ok=True)
            (diretorio_saida / 'visualizacoes').mkdir(exist_ok=True)
            (diretorio_saida / 'resultados').mkdir(exist_ok=True)
        
        imagens = []
        for ext in extensoes:
            imagens.extend(diretorio_entrada.glob(f'*{ext}'))
            imagens.extend(diretorio_entrada.glob(f'*{ext.upper()}'))
        
        if not imagens:
            print(f"Nenhuma imagem encontrada em {diretorio_entrada}")
            return []
        
        print(f"Processando {len(imagens)} imagem(ns)...")
        resultados = []
        
        for idx, caminho_imagem in enumerate(imagens, 1):
            print(f"\n[{idx}/{len(imagens)}] Processando: {caminho_imagem.name}")
            
            resultado = self.contador.processar(str(caminho_imagem))
            
            if resultado:
                if diretorio_saida:
                    nome_base = caminho_imagem.stem
                    caminho_resultado = diretorio_saida / 'resultados' / f'{nome_base}_resultado.jpg'
                    cv2.imwrite(str(caminho_resultado), resultado.imagem_resultado)
                
                if salvar_visualizacoes and diretorio_saida:
                    nome_base = caminho_imagem.stem
                    caminho_viz = diretorio_saida / 'visualizacoes' / f'{nome_base}_visualizacao.png'
                    VisualizadorResultados.visualizar(
                        resultado, salvar=True, caminho_saida=str(caminho_viz), mostrar=False
                    )
                
                resultado_dict = {
                    'arquivo': caminho_imagem.name,
                    'caminho': str(caminho_imagem),
                    'total_objetos': resultado.total_objetos,
                    'estatisticas': resultado.estatisticas,
                    'objetos_detectados': resultado.objetos_detectados
                }
                resultados.append(resultado_dict)
                
                print(f"  ✓ {resultado.total_objetos} objeto(s) detectado(s)")
        
        if salvar_resultados and diretorio_saida:
            caminho_json = diretorio_saida / 'resultados_lote.json'
            with open(caminho_json, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Resultados salvos em: {caminho_json}")

        if resultados:
            total_objetos_geral = sum(r['total_objetos'] for r in resultados)
            print(f"\n{'='*50}")
            print(f"RESUMO DO PROCESSAMENTO EM LOTE")
            print(f"{'='*50}")
            print(f"Total de imagens processadas: {len(resultados)}")
            print(f"Total de objetos detectados: {total_objetos_geral}")
            print(f"Média de objetos por imagem: {total_objetos_geral/len(resultados):.2f}")
            print(f"{'='*50}")
        
        self.resultados = resultados
        return resultados

