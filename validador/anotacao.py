"""Desenho das caixas, textos de acesso e janela de visualização."""

import cv2

from .config import VERDE, VERMELHO


def escrever_texto(imagem, texto, x, y, cor):
    altura, largura = imagem.shape[:2]
    escala = min(0.7, max(0.2, largura / 650))
    espessura = 1 if escala < 0.5 else 2
    (w, h), base = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, escala, espessura)
    if w + 8 > largura:
        escala *= max(1, largura - 8) / (w + 8)
        (w, h), base = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, escala, espessura)
    x = max(0, min(int(x), largura - w - 8))
    y = min(altura - base - 3, max(h + 5, int(y)))
    cv2.rectangle(imagem, (x, y - h - 5), (x + w + 8, y + base + 3), (0, 0, 0), -1)
    cv2.putText(imagem, texto, (x + 4, y), cv2.FONT_HERSHEY_SIMPLEX,
                escala, cor, espessura, cv2.LINE_AA)


def marcar_rosto(imagem, area, liberado):
    altura, largura = imagem.shape[:2]
    x = max(0, min(int(area["x"]), largura - 1))
    y = max(0, min(int(area["y"]), altura - 1))
    direita = min(largura - 1, x + int(area["w"]))
    baixo = min(altura - 1, y + int(area["h"]))
    cv2.rectangle(imagem, (x, y), (direita, baixo), VERDE if liberado else VERMELHO, 2)
    texto = "ACESSO LIBERADO" if liberado else "ACESSO NEGADO"
    escrever_texto(imagem, texto, x, y - 8, VERDE if liberado else VERMELHO)


def mostrar_imagem(imagem):
    escala = min(1.0, 1280 / imagem.shape[1], 800 / imagem.shape[0])
    previa = cv2.resize(imagem, None, fx=escala, fy=escala)
    cv2.imshow("Reconhecimento facial - pressione uma tecla", previa)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
