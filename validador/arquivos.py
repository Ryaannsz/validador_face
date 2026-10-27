"""Leitura de imagens e gravação dos resultados em disco."""

import json

from .config import EXTENSOES


def listar_imagens(pasta):
    return sorted(p for p in pasta.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSOES)


def ler_imagem(caminho):
    import cv2
    import numpy as np

    # imdecode permite caminhos com acentos em diferentes sistemas operacionais.
    imagem = cv2.imdecode(np.frombuffer(caminho.read_bytes(), dtype=np.uint8), cv2.IMREAD_COLOR)
    if imagem is None:
        raise ValueError(f"Não foi possível ler a imagem: {caminho}")
    return imagem


def salvar_resultados(imagem, relatorio, destino):
    import cv2

    destino.parent.mkdir(parents=True, exist_ok=True)
    sucesso, dados = cv2.imencode(".jpg", imagem)
    if not sucesso:
        raise OSError(f"Falha ao salvar resultado: {destino}")
    destino.write_bytes(dados.tobytes())
    destino.with_suffix(".json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8"
    )
