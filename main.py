"""
Script principal para contagem de objetos em imagens industriais.
Suporta processamento de imagem única ou lote.
"""

import argparse
import sys
from pathlib import Path
from contador_objetos import ContadorObjetosIndustrial, MetodoSegmentacao
from visualizador import VisualizadorResultados
from processador_lote import ProcessadorLote


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(
        description='Sistema de Contagem de Objetos em Imagens Industriais',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Processar uma única imagem
  python main.py -i imagem.jpg
  
  # Processar diretório completo
  python main.py -d dataset/ -o resultados/
  
  # Usar método de segmentação adaptativa
  python main.py -i imagem.jpg -m adaptive
  
  # Ajustar área mínima
  python main.py -i imagem.jpg -a 100
        """
    )
    
    parser.add_argument(
        '-i', '--imagem',
        type=str,
        help='Caminho para uma única imagem a processar'
    )
    
    parser.add_argument(
        '-d', '--diretorio',
        type=str,
        help='Caminho para diretório com múltiplas imagens'
    )
    
    parser.add_argument(
        '-o', '--saida',
        type=str,
        default='resultados',
        help='Diretório de saída para resultados (padrão: resultados)'
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
        help='Área mínima em pixels para considerar um objeto (padrão: 50)'
    )
    
    parser.add_argument(
        '-k', '--kernel-morph',
        type=int,
        default=3,
        help='Tamanho do kernel morfológico (padrão: 3)'
    )
    
    parser.add_argument(
        '--iteracoes',
        type=int,
        default=2,
        help='Número de iterações para operações morfológicas (padrão: 2)'
    )
    
    parser.add_argument(
        '--sem-visualizacao',
        action='store_true',
        help='Não exibir visualizações (útil para processamento em lote)'
    )
    
    parser.add_argument(
        '--salvar',
        action='store_true',
        help='Salvar visualizações e resultados em arquivos'
    )
    
    args = parser.parse_args()
    
    # Validar argumentos
    if not args.imagem and not args.diretorio:
        parser.error("É necessário fornecer -i/--imagem ou -d/--diretorio")
    
    # Converter método de segmentação
    metodo_map = {
        'otsu': MetodoSegmentacao.OTSU,
        'adaptive': MetodoSegmentacao.ADAPTIVE,
        'canny': MetodoSegmentacao.CANNY
    }
    metodo = metodo_map[args.metodo]
    
    # Criar contador configurado
    contador = ContadorObjetosIndustrial(
        area_minima=args.area_minima,
        morph_kernel_size=args.kernel_morph,
        morph_iterations=args.iteracoes,
        metodo_segmentacao=metodo
    )
    
    # Processar imagem única
    if args.imagem:
        caminho_imagem = Path(args.imagem)
        if not caminho_imagem.exists():
            print(f"Erro: Imagem não encontrada: {caminho_imagem}")
            sys.exit(1)
        
        print(f"Processando: {caminho_imagem}")
        print(f"Método de segmentação: {args.metodo}")
        print(f"Área mínima: {args.area_minima} pixels")
        print("-" * 50)
        
        resultado = contador.processar(str(caminho_imagem))
        
        if resultado:
            print(f"\n✓ Total de objetos detectados: {resultado.total_objetos}")
            print(f"  Área média: {resultado.estatisticas['area_media']:.1f} pixels")
            print(f"  Área mediana: {resultado.estatisticas['area_mediana']:.1f} pixels")
            print(f"  Área mín/máx: {resultado.estatisticas['area_min']:.0f} / {resultado.estatisticas['area_max']:.0f} pixels")
            
            # Visualizar
            if not args.sem_visualizacao:
                VisualizadorResultados.visualizar(
                    resultado,
                    salvar=args.salvar,
                    caminho_saida=str(Path(args.saida) / f'{caminho_imagem.stem}_visualizacao.png') if args.salvar else None,
                    mostrar=not args.sem_visualizacao
                )
            
            # Salvar imagem resultado
            if args.salvar:
                caminho_resultado = Path(args.saida) / f'{caminho_imagem.stem}_resultado.jpg'
                Path(args.saida).mkdir(parents=True, exist_ok=True)
                import cv2
                cv2.imwrite(str(caminho_resultado), resultado.imagem_resultado)
                print(f"\n✓ Resultado salvo em: {caminho_resultado}")
        else:
            print("Erro ao processar imagem.")
            sys.exit(1)
    
    # Processar diretório
    elif args.diretorio:
        processador_lote = ProcessadorLote(contador)
        processador_lote.processar_diretorio(
            diretorio_entrada=args.diretorio,
            diretorio_saida=args.saida,
            salvar_visualizacoes=args.salvar,
            salvar_resultados=args.salvar
        )


if __name__ == '__main__':
    main()

