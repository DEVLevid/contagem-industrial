"""
Módulo para visualização dos resultados da contagem de objetos.
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2
from typing import Optional
from contador_objetos import ResultadoContagem


class VisualizadorResultados:
    """Classe para visualizar resultados da contagem de objetos."""
    
    @staticmethod
    def visualizar(resultado: ResultadoContagem, salvar: bool = False, 
                   caminho_saida: Optional[str] = None, mostrar: bool = True):
        """
        Visualiza os resultados da contagem em uma grade de imagens.
        
        Args:
            resultado: ResultadoContagem com os dados processados
            salvar: Se True, salva a visualização em arquivo
            caminho_saida: Caminho para salvar a imagem (se salvar=True)
            mostrar: Se True, exibe a visualização
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Imagem original
        img_original_rgb = cv2.cvtColor(resultado.imagem_original, cv2.COLOR_BGR2RGB)
        axes[0].imshow(img_original_rgb)
        axes[0].set_title('Imagem Original', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # Imagem binária segmentada
        axes[1].imshow(resultado.imagem_binaria, cmap='gray')
        axes[1].set_title('Segmentação Binária', fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        # Imagem com objetos detectados
        img_resultado_rgb = cv2.cvtColor(resultado.imagem_resultado, cv2.COLOR_BGR2RGB)
        axes[2].imshow(img_resultado_rgb)
        axes[2].set_title(
            f'Resultado: {resultado.total_objetos} Objetos Detectados',
            fontsize=14, fontweight='bold'
        )
        axes[2].axis('off')
        
        plt.tight_layout()
        
        if salvar and caminho_saida:
            plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {caminho_saida}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    @staticmethod
    def visualizar_estatisticas(resultado: ResultadoContagem, salvar: bool = False,
                                caminho_saida: Optional[str] = None, mostrar: bool = True):
        """
        Visualiza estatísticas dos objetos detectados.
        
        Args:
            resultado: ResultadoContagem com os dados processados
            salvar: Se True, salva a visualização em arquivo
            caminho_saida: Caminho para salvar a imagem (se salvar=True)
            mostrar: Se True, exibe a visualização
        """
        if resultado.total_objetos == 0:
            print("Nenhum objeto detectado para visualizar estatísticas.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Histograma de áreas
        areas = [obj['area'] for obj in resultado.objetos_detectados]
        axes[0].hist(areas, bins=min(20, len(areas)), edgecolor='black', alpha=0.7)
        axes[0].axvline(resultado.estatisticas['area_media'], color='r', 
                       linestyle='--', label=f"Média: {resultado.estatisticas['area_media']:.1f}")
        axes[0].axvline(resultado.estatisticas['area_mediana'], color='g', 
                       linestyle='--', label=f"Mediana: {resultado.estatisticas['area_mediana']:.1f}")
        axes[0].set_xlabel('Área (pixels)', fontsize=12)
        axes[0].set_ylabel('Frequência', fontsize=12)
        axes[0].set_title('Distribuição de Áreas dos Objetos', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Gráfico de barras com estatísticas
        stats_labels = ['Total', 'Média', 'Mediana', 'Mín', 'Máx']
        stats_values = [
            resultado.estatisticas['total'],
            resultado.estatisticas['area_media'],
            resultado.estatisticas['area_mediana'],
            resultado.estatisticas['area_min'],
            resultado.estatisticas['area_max']
        ]
        
        bars = axes[1].bar(stats_labels, stats_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        axes[1].set_ylabel('Valor', fontsize=12)
        axes[1].set_title('Estatísticas dos Objetos', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, stats_values):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        if salvar and caminho_saida:
            plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
            print(f"Estatísticas salvas em: {caminho_saida}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()

