"""
Exemplo de uso do sistema de contagem de objetos industriais.
Este arquivo demonstra como usar o sistema programaticamente.
"""

from contador_objetos import ContadorObjetosIndustrial, MetodoSegmentacao
from visualizador import VisualizadorResultados
from processador_lote import ProcessadorLote
import os


def exemplo_imagem_unica():
    """Exemplo de processamento de uma única imagem."""
    print("=" * 60)
    print("EXEMPLO 1: Processamento de Imagem Única")
    print("=" * 60)
    
    # Criar contador com configurações padrão
    contador = ContadorObjetosIndustrial(
        area_minima=50,
        metodo_segmentacao=MetodoSegmentacao.OTSU
    )
    
    # Caminho da imagem (ajuste conforme necessário)
    caminho_imagem = "teste_simulado.jpg"
    
    # Se a imagem não existir, criar uma de teste
    if not os.path.exists(caminho_imagem):
        print(f"Imagem não encontrada. Criando imagem de teste: {caminho_imagem}")
        import cv2
        import numpy as np
        
        # Criar imagem de teste com objetos simulados
        img_teste = np.ones((400, 400, 3), dtype=np.uint8) * 200
        
        # Adicionar alguns objetos (retângulos e círculos escuros)
        cv2.rectangle(img_teste, (50, 50), (120, 120), (50, 50, 50), -1)
        cv2.rectangle(img_teste, (200, 150), (280, 220), (40, 40, 40), -1)
        cv2.circle(img_teste, (300, 100), 30, (30, 30, 30), -1)
        cv2.rectangle(img_teste, (100, 250), (150, 300), (60, 60, 60), -1)
        cv2.circle(img_teste, (250, 300), 25, (35, 35, 35), -1)
        
        cv2.imwrite(caminho_imagem, img_teste)
        print(f"Imagem de teste criada: {caminho_imagem}")
    
    # Processar imagem
    resultado = contador.processar(caminho_imagem)
    
    if resultado:
        print(f"\n✓ Total de objetos detectados: {resultado.total_objetos}")
        print(f"  Área média: {resultado.estatisticas['area_media']:.1f} pixels")
        print(f"  Área mediana: {resultado.estatisticas['area_mediana']:.1f} pixels")
        
        # Visualizar resultados
        VisualizadorResultados.visualizar(resultado)
        
        # Visualizar estatísticas
        VisualizadorResultados.visualizar_estatisticas(resultado)
    else:
        print("Erro ao processar imagem.")


def exemplo_diferentes_metodos():
    """Exemplo comparando diferentes métodos de segmentação."""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Comparação de Métodos de Segmentação")
    print("=" * 60)
    
    caminho_imagem = "teste_simulado.jpg"
    
    if not os.path.exists(caminho_imagem):
        print(f"Imagem não encontrada: {caminho_imagem}")
        return
    
    metodos = [
        (MetodoSegmentacao.OTSU, "Otsu"),
        (MetodoSegmentacao.ADAPTIVE, "Adaptativa"),
        (MetodoSegmentacao.CANNY, "Canny")
    ]
    
    resultados = []
    
    for metodo, nome in metodos:
        print(f"\nProcessando com método: {nome}")
        contador = ContadorObjetosIndustrial(
            area_minima=50,
            metodo_segmentacao=metodo
        )
        
        resultado = contador.processar(caminho_imagem)
        if resultado:
            resultados.append((nome, resultado))
            print(f"  Objetos detectados: {resultado.total_objetos}")
    
    # Comparar resultados
    if resultados:
        print("\n" + "-" * 60)
        print("COMPARAÇÃO DE MÉTODOS:")
        print("-" * 60)
        for nome, resultado in resultados:
            print(f"{nome:15s}: {resultado.total_objetos:3d} objetos "
                  f"(área média: {resultado.estatisticas['area_media']:.1f})")


def exemplo_processamento_lote():
    """Exemplo de processamento em lote."""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Processamento em Lote")
    print("=" * 60)
    
    # Criar diretório de teste se não existir
    diretorio_teste = "dataset_teste"
    if not os.path.exists(diretorio_teste):
        os.makedirs(diretorio_teste)
        print(f"Diretório de teste criado: {diretorio_teste}")
        print("Adicione imagens neste diretório para processamento em lote.")
        return
    
    # Criar contador
    contador = ContadorObjetosIndustrial(
        area_minima=50,
        metodo_segmentacao=MetodoSegmentacao.OTSU
    )
    
    # Criar processador em lote
    processador = ProcessadorLote(contador)
    
    # Processar diretório
    resultados = processador.processar_diretorio(
        diretorio_entrada=diretorio_teste,
        diretorio_saida="resultados_lote",
        salvar_visualizacoes=True,
        salvar_resultados=True
    )
    
    if resultados:
        print(f"\n✓ Processamento concluído: {len(resultados)} imagem(ns)")


def exemplo_parametros_customizados():
    """Exemplo com parâmetros customizados."""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Parâmetros Customizados")
    print("=" * 60)
    
    caminho_imagem = "teste_simulado.jpg"
    
    if not os.path.exists(caminho_imagem):
        print(f"Imagem não encontrada: {caminho_imagem}")
        return
    
    # Contador com parâmetros customizados
    contador = ContadorObjetosIndustrial(
        area_minima=100,           # Área mínima maior
        blur_kernel=(7, 7),         # Blur mais forte
        morph_kernel_size=5,        # Kernel morfológico maior
        morph_iterations=3,         # Mais iterações
        metodo_segmentacao=MetodoSegmentacao.OTSU
    )
    
    print("Parâmetros customizados:")
    print(f"  Área mínima: {contador.area_minima}")
    print(f"  Blur kernel: {contador.blur_kernel}")
    print(f"  Kernel morfológico: {contador.morph_kernel.shape}")
    print(f"  Iterações: {contador.morph_iterations}")
    
    resultado = contador.processar(caminho_imagem)
    
    if resultado:
        print(f"\n✓ Objetos detectados: {resultado.total_objetos}")
        VisualizadorResultados.visualizar(resultado)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SISTEMA DE CONTAGEM DE OBJETOS INDUSTRIAIS")
    print("Exemplos de Uso")
    print("=" * 60)
    
    # Executar exemplos
    exemplo_imagem_unica()
    
    # Descomente para executar outros exemplos:
    # exemplo_diferentes_metodos()
    # exemplo_processamento_lote()
    # exemplo_parametros_customizados()
    
    print("\n" + "=" * 60)
    print("Exemplos concluídos!")
    print("=" * 60)

