"""
Módulo para processamento em lote de múltiplas imagens.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import cv2
from contador_objetos import ContadorObjetosIndustrial, ResultadoContagem
from visualizador import VisualizadorResultados


class ProcessadorLote:
    """Classe para processar múltiplas imagens em lote."""
    
    def __init__(self, contador: ContadorObjetosIndustrial):
        """
        Inicializa o processador em lote.
        
        Args:
            contador: Instância de ContadorObjetosIndustrial configurada
        """
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
        """
        Processa todas as imagens de um diretório.
        
        Args:
            diretorio_entrada: Caminho do diretório com imagens
            diretorio_saida: Caminho do diretório para salvar resultados (opcional)
            extensoes: Lista de extensões de arquivo a processar (padrão: ['.jpg', '.jpeg', '.png'])
            salvar_visualizacoes: Se True, salva visualizações das imagens processadas
            salvar_resultados: Se True, salva resultados em JSON
            
        Returns:
            Lista de dicionários com resultados de cada imagem
        """
        if extensoes is None:
            extensoes = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        
        diretorio_entrada = Path(diretorio_entrada)
        if not diretorio_entrada.exists():
            print(f"Erro: Diretório não encontrado: {diretorio_entrada}")
            return []
        
        # Criar diretório de saída se especificado
        if diretorio_saida:
            diretorio_saida = Path(diretorio_saida)
            diretorio_saida.mkdir(parents=True, exist_ok=True)
            (diretorio_saida / 'visualizacoes').mkdir(exist_ok=True)
            (diretorio_saida / 'resultados').mkdir(exist_ok=True)
        
        # Encontrar todas as imagens
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
                # Salvar imagem resultado
                if diretorio_saida:
                    nome_base = caminho_imagem.stem
                    caminho_resultado = diretorio_saida / 'resultados' / f'{nome_base}_resultado.jpg'
                    cv2.imwrite(str(caminho_resultado), resultado.imagem_resultado)
                
                # Salvar visualização
                if salvar_visualizacoes and diretorio_saida:
                    nome_base = caminho_imagem.stem
                    caminho_viz = diretorio_saida / 'visualizacoes' / f'{nome_base}_visualizacao.png'
                    VisualizadorResultados.visualizar(
                        resultado, salvar=True, caminho_saida=str(caminho_viz), mostrar=False
                    )
                
                # Armazenar resultado
                resultado_dict = {
                    'arquivo': caminho_imagem.name,
                    'caminho': str(caminho_imagem),
                    'total_objetos': resultado.total_objetos,
                    'estatisticas': resultado.estatisticas,
                    'objetos_detectados': resultado.objetos_detectados
                }
                resultados.append(resultado_dict)
                
                print(f"  ✓ {resultado.total_objetos} objeto(s) detectado(s)")
        
        # Salvar resultados em JSON
        if salvar_resultados and diretorio_saida:
            caminho_json = diretorio_saida / 'resultados_lote.json'
            with open(caminho_json, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Resultados salvos em: {caminho_json}")
        
        # Estatísticas gerais
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

