"""Caminhos, parâmetros de reconhecimento e cores da aplicação."""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
EXTENSOES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MODELO = "Facenet512"
VERMELHO = (0, 0, 255)  # OpenCV usa BGR.
VERDE = (0, 255, 0)


def configurar_ambiente():
    """Configura os arquivos do DeepFace antes de importar a biblioteca."""
    os.environ["DEEPFACE_HOME"] = str(BASE / "modelos")
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
