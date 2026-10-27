"""Extração de vetores faciais e comparação com o cadastro pelo DeepFace."""

from deepface import DeepFace

from .config import MODELO


def representar(imagem):
    try:
        return DeepFace.represent(
            img_path=imagem,
            model_name=MODELO,
            detector_backend="opencv",
            enforce_detection=True,
            align=True,
        )
    except ValueError as erro:
        # Apenas a ausência de rosto é um resultado normal; outros erros são propagados.
        if "face could not be detected" in str(erro).lower():
            return []
        raise


def identificar(embedding, cadastro, limiar):
    melhor = None
    for referencia in cadastro:
        comparacao = DeepFace.verify(
            img1_path=embedding,
            img2_path=referencia["embedding"],
            model_name=MODELO,
            distance_metric="cosine",
            threshold=limiar,
            silent=True,
        )
        if comparacao["verified"] and (
            melhor is None or comparacao["distance"] < melhor["distancia"]
        ):
            melhor = {
                "pessoa": referencia["pessoa"],
                "foto_referencia": referencia["foto"],
                "distancia": float(comparacao["distance"]),
                "limiar": float(comparacao["threshold"]),
            }
    return melhor
