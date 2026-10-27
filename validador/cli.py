"""Reconhecimento facial em imagens com OpenCV e DeepFace."""

import argparse
import math
from pathlib import Path

from .arquivos import listar_imagens
from .config import BASE, EXTENSOES, configurar_ambiente


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imagem", type=Path, help="Processar somente esta imagem.")
    parser.add_argument("--autorizados", type=Path, default=BASE / "pessoas_autorizadas")
    parser.add_argument("--testes", type=Path, default=BASE / "fotos_teste")
    parser.add_argument("--saida", type=Path, default=BASE / "resultados")
    parser.add_argument("--mostrar", action="store_true", help="Abrir cada resultado em uma janela.")
    parser.add_argument("--limiar", type=float, help="Distância cosseno máxima; padrão do DeepFace se omitido.")
    args = parser.parse_args()
    if args.limiar is not None and (not math.isfinite(args.limiar) or not 0 <= args.limiar <= 2):
        parser.error("--limiar deve estar entre 0 e 2.")
    for pasta in (args.autorizados, args.testes):
        if not pasta.is_dir():
            parser.error(f"Pasta não encontrada: {pasta}")
    if args.imagem:
        if not args.imagem.is_file() or args.imagem.suffix.lower() not in EXTENSOES:
            parser.error(f"Imagem inválida: {args.imagem}")
        imagens = [args.imagem.resolve()]
    else:
        imagens = listar_imagens(args.testes.resolve())
    if not imagens:
        print(f"Adicione imagens JPG, JPEG, PNG, BMP ou WEBP em: {args.testes}")
        return 0

    configurar_ambiente()
    print("Carregando DeepFace e o cadastro de pessoas autorizadas...", flush=True)
    try:
        # Imports após a configuração; --help e pasta vazia continuam rápidos.
        from .cadastro import carregar_autorizados
        from .processamento import processar
    except ImportError as erro:
        print(f"Dependência ausente: {erro}. Instale com: uv sync")
        return 1

    cadastro = carregar_autorizados(args.autorizados.resolve())
    print(f"Referências válidas: {len(cadastro)}")
    if not cadastro:
        print("[AVISO] Nenhuma pessoa cadastrada. Todos os rostos terão acesso negado.")
    falhas = 0
    for caminho in imagens:
        relativo = Path(caminho.name) if args.imagem else caminho.relative_to(args.testes.resolve())
        destino = args.saida.resolve() / relativo.parent / f"{relativo.name}_resultado.jpg"
        print(f"\nAnalisando: {caminho}")
        try:
            processar(caminho, destino, cadastro, args.limiar, args.mostrar)
        except Exception as erro:
            falhas += 1
            # Erro de processamento nunca é reportado como acesso liberado.
            print(f"[ERRO] Falha ao processar {caminho.name}: {erro}")
    return 1 if falhas else 0
