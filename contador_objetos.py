"""
Módulo principal para contagem de objetos em imagens industriais.
Suporta segmentação, morfologia e rotulagem de componentes conectados.
"""

import cv2
import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class MetodoSegmentacao(Enum):
    """Enum para métodos de segmentação disponíveis."""
    OTSU = "otsu"
    ADAPTIVE = "adaptive"
    CANNY = "canny"


@dataclass
class ResultadoContagem:
    """Classe para armazenar resultados da contagem."""
    total_objetos: int
    imagem_original: np.ndarray
    imagem_binaria: np.ndarray
    imagem_resultado: np.ndarray
    objetos_detectados: List[Dict]
    estatisticas: Dict


class ContadorObjetosIndustrial:
    """
    Classe principal para contagem de objetos em imagens industriais.
    
    Utiliza técnicas de:
    - Segmentação (Otsu, Adaptativa, Canny)
    - Morfologia matemática
    - Componentes conectados
    """
    
    def __init__(
        self,
        area_minima: int = 50,
        blur_kernel: Tuple[int, int] = (5, 5),
        morph_kernel_size: int = 3,
        morph_iterations: int = 2,
        metodo_segmentacao: MetodoSegmentacao = MetodoSegmentacao.OTSU
    ):
        """
        Inicializa o contador de objetos.
        
        Args:
            area_minima: Área mínima em pixels para considerar um objeto
            blur_kernel: Tamanho do kernel para blur gaussiano
            morph_kernel_size: Tamanho do kernel morfológico
            morph_iterations: Número de iterações para operações morfológicas
            metodo_segmentacao: Método de segmentação a ser usado
        """
        self.area_minima = area_minima
        self.blur_kernel = blur_kernel
        self.morph_kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
        self.morph_iterations = morph_iterations
        self.metodo_segmentacao = metodo_segmentacao
    
    def preprocessar_imagem(self, imagem: np.ndarray) -> np.ndarray:
        """
        Pré-processa a imagem convertendo para escala de cinza e aplicando blur.
        
        Args:
            imagem: Imagem BGR de entrada
            
        Returns:
            Imagem em escala de cinza com blur aplicado
        """
        if len(imagem.shape) == 3:
            img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = imagem.copy()
        
        img_blur = cv2.GaussianBlur(img_gray, self.blur_kernel, 0)
        return img_blur
    
    def segmentar_imagem(self, imagem: np.ndarray) -> np.ndarray:
        """
        Segmenta a imagem usando o método selecionado.
        
        Args:
            imagem: Imagem em escala de cinza pré-processada
            
        Returns:
            Imagem binária segmentada
        """
        if self.metodo_segmentacao == MetodoSegmentacao.OTSU:
            _, img_binaria = cv2.threshold(
                imagem, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )
        
        elif self.metodo_segmentacao == MetodoSegmentacao.ADAPTIVE:
            img_binaria = cv2.adaptiveThreshold(
                imagem, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
        
        elif self.metodo_segmentacao == MetodoSegmentacao.CANNY:
            edges = cv2.Canny(imagem, 50, 150)
            img_binaria = cv2.dilate(edges, self.morph_kernel, iterations=1)
        
        return img_binaria
    
    def aplicar_morfologia(self, imagem_binaria: np.ndarray) -> np.ndarray:
        """
        Aplica operações morfológicas para limpar a imagem binária.
        
        Args:
            imagem_binaria: Imagem binária segmentada
            
        Returns:
            Imagem binária após operações morfológicas
        """
        # Opening: remove ruído pequeno
        img_morph = cv2.morphologyEx(
            imagem_binaria, cv2.MORPH_OPEN, 
            self.morph_kernel, iterations=self.morph_iterations
        )
        
        # Closing: preenche buracos pequenos
        img_morph = cv2.morphologyEx(
            img_morph, cv2.MORPH_CLOSE, 
            self.morph_kernel, iterations=self.morph_iterations
        )
        
        return img_morph
    
    def contar_componentes(self, imagem_binaria: np.ndarray) -> Tuple[int, np.ndarray, np.ndarray, np.ndarray]:
        """
        Conta componentes conectados na imagem binária.
        
        Args:
            imagem_binaria: Imagem binária processada
            
        Returns:
            Tupla com (num_labels, labels, stats, centroids)
        """
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            imagem_binaria, connectivity=8
        )
        return num_labels, labels, stats, centroids
    
    def processar(self, caminho_imagem: str) -> Optional[ResultadoContagem]:
        """
        Processa uma imagem e retorna os resultados da contagem.
        
        Args:
            caminho_imagem: Caminho para a imagem a ser processada
            
        Returns:
            ResultadoContagem com todos os dados processados ou None se houver erro
        """
        # Carregar imagem
        img_original = cv2.imread(caminho_imagem)
        if img_original is None:
            print(f"Erro: Imagem não encontrada em {caminho_imagem}")
            return None
        
        # Pré-processamento
        img_preprocessada = self.preprocessar_imagem(img_original)
        
        # Segmentação
        img_binaria = self.segmentar_imagem(img_preprocessada)
        
        # Morfologia
        img_morph = self.aplicar_morfologia(img_binaria)
        
        # Contagem de componentes
        num_labels, labels, stats, centroids = self.contar_componentes(img_morph)
        
        # Filtrar objetos por área mínima e criar imagem resultado
        img_resultado = img_original.copy()
        objetos_detectados = []
        contagem_final = 0
        
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            
            if area > self.area_minima:
                contagem_final += 1
                
                # Desenhar retângulo e número
                cv2.rectangle(img_resultado, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    img_resultado, str(contagem_final), (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
                )
                
                # Armazenar informações do objeto
                objetos_detectados.append({
                    'id': contagem_final,
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'area': int(area),
                    'centroid': (float(centroids[i][0]), float(centroids[i][1]))
                })
        
        # Estatísticas
        areas = [obj['area'] for obj in objetos_detectados]
        estatisticas = {
            'total': contagem_final,
            'area_media': np.mean(areas) if areas else 0,
            'area_mediana': np.median(areas) if areas else 0,
            'area_min': np.min(areas) if areas else 0,
            'area_max': np.max(areas) if areas else 0,
            'desvio_padrao': np.std(areas) if areas else 0
        }
        
        return ResultadoContagem(
            total_objetos=contagem_final,
            imagem_original=img_original,
            imagem_binaria=img_binaria,
            imagem_resultado=img_resultado,
            objetos_detectados=objetos_detectados,
            estatisticas=estatisticas
        )

