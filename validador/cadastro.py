"""Carregamento e validação das fotos de pessoas autorizadas."""

from .arquivos import ler_imagem, listar_imagens
from .reconhecimento import representar


def carregar_autorizados(pasta):
    cadastro = []
    for caminho in listar_imagens(pasta):
        try:
            rostos = representar(ler_imagem(caminho))
        except (OSError, ValueError) as erro:
            print(f"[AVISO] Cadastro ignorado: {caminho.name}: {erro}")
            continue
        if len(rostos) != 1:
            print(f"[AVISO] Cadastro ignorado: {caminho.name}: use uma foto com exatamente um rosto.")
            continue
        relativo = caminho.relative_to(pasta)
        pessoa = relativo.parts[0] if len(relativo.parts) > 1 else caminho.stem
        cadastro.append({"pessoa": pessoa, "foto": str(relativo), "embedding": rostos[0]["embedding"]})
    return cadastro
