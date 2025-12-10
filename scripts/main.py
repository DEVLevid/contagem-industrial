import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.contador import ContadorObjetosIndustrial, MetodoSegmentacao
from src.core.visualizador import VisualizadorResultados
from src.processors.lote import ProcessadorLote


def main():
    parser = argparse.ArgumentParser(
        description='Sistema de Contagem de Objetos em Imagens Industriais',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py -i imagem.jpg
  python main.py -d dataset/ -o resultados/
  python main.py -i imagem.jpg -m adaptive -a 100
        """
    )
    
    parser.add_argument('-i', '--imagem', type=str, help='Caminho para uma única imagem')
    parser.add_argument('-d', '--diretorio', type=str, help='Caminho para diretório com múltiplas imagens')
    parser.add_argument('-o', '--saida', type=str, default='resultados', help='Diretório de saída')
    parser.add_argument('-m', '--metodo', type=str, choices=['otsu', 'adaptive', 'canny'], default='otsu',
                       help='Método de segmentação')
    parser.add_argument('-a', '--area-minima', type=int, default=50, help='Área mínima em pixels')
    parser.add_argument('-k', '--kernel-morph', type=int, default=3, help='Tamanho do kernel morfológico')
    parser.add_argument('--iteracoes', type=int, default=2, help='Número de iterações morfológicas')
    parser.add_argument('--sem-visualizacao', action='store_true', help='Não exibir visualizações')
    parser.add_argument('--salvar', action='store_true', help='Salvar visualizações e resultados')
    
    args = parser.parse_args()
    
    if not args.imagem and not args.diretorio:
        parser.error("É necessário fornecer -i/--imagem ou -d/--diretorio")
    
    metodo_map = {
        'otsu': MetodoSegmentacao.OTSU,
        'adaptive': MetodoSegmentacao.ADAPTIVE,
        'canny': MetodoSegmentacao.CANNY
    }
    metodo = metodo_map[args.metodo]
    
    contador = ContadorObjetosIndustrial(
        area_minima=args.area_minima,
        morph_kernel_size=args.kernel_morph,
        morph_iterations=args.iteracoes,
        metodo_segmentacao=metodo
    )
    
    if args.imagem:
        caminho_imagem = Path(args.imagem)
        if not caminho_imagem.exists():
            print(f"Erro: Imagem não encontrada: {caminho_imagem}")
            sys.exit(1)
        
        print(f"Processando: {caminho_imagem}")
        resultado = contador.processar(str(caminho_imagem))
        
        if resultado:
            print(f"\n✓ Total de objetos detectados: {resultado.total_objetos}")
            print(f"  Área média: {resultado.estatisticas['area_media']:.1f} pixels")
            
            if not args.sem_visualizacao:
                VisualizadorResultados.visualizar(
                    resultado,
                    salvar=args.salvar,
                    caminho_saida=str(Path(args.saida) / f'{caminho_imagem.stem}_visualizacao.png') if args.salvar else None,
                    mostrar=not args.sem_visualizacao
                )
            
            if args.salvar:
                caminho_resultado = Path(args.saida) / f'{caminho_imagem.stem}_resultado.jpg'
                Path(args.saida).mkdir(parents=True, exist_ok=True)
                import cv2
                cv2.imwrite(str(caminho_resultado), resultado.imagem_resultado)
                print(f"\n✓ Resultado salvo em: {caminho_resultado}")
        else:
            print("Erro ao processar imagem.")
            sys.exit(1)
    
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

