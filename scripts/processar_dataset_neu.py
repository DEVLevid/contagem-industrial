import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.contador import MetodoSegmentacao
from src.processors.dataset_neu import ProcessadorDatasetNEU


def main():
    parser = argparse.ArgumentParser(
        description='Processar dataset NEU Metal Surface Defects Data completo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python processar_dataset_neu.py
  python processar_dataset_neu.py --sem-visualizacoes
  python processar_dataset_neu.py -m adaptive -a 100
        """
    )
    
    parser.add_argument('-d', '--dataset', type=str, default='NEU Metal Surface Defects Data',
                       help='Caminho para o diretório do dataset')
    parser.add_argument('-o', '--saida', type=str, default='resultados_neu', help='Diretório de saída')
    parser.add_argument('-m', '--metodo', type=str, choices=['otsu', 'adaptive', 'canny'], default='otsu',
                       help='Método de segmentação')
    parser.add_argument('-a', '--area-minima', type=int, default=50, help='Área mínima em pixels')
    parser.add_argument('--sem-visualizacoes', action='store_true', help='Não salvar visualizações')
    parser.add_argument('--sem-imagens-resultado', action='store_true', help='Não salvar imagens marcadas')
    
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

