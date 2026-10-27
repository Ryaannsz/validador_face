"""Fluxo de análise de uma foto e geração da imagem e relatório finais."""

from .anotacao import escrever_texto, marcar_rosto, mostrar_imagem
from .arquivos import ler_imagem, salvar_resultados
from .config import MODELO, VERMELHO
from .reconhecimento import identificar, representar


def processar(caminho, destino, cadastro, limiar, mostrar):
    imagem = ler_imagem(caminho)
    rostos = representar(imagem)
    relatorio = {"imagem": str(caminho), "modelo": MODELO, "rostos": []}
    for numero, rosto in enumerate(rostos, start=1):
        identidade = identificar(rosto["embedding"], cadastro, limiar)
        liberado = identidade is not None
        marcar_rosto(imagem, rosto["facial_area"], liberado)
        area = {chave: int(rosto["facial_area"][chave]) for chave in ("x", "y", "w", "h")}
        relatorio["rostos"].append({
            "numero": numero,
            "status": "ACESSO LIBERADO" if liberado else "ACESSO NEGADO",
            "bounding_box": area,
            "identidade": identidade,
        })
        print(f"  Rosto {numero}: {'ACESSO LIBERADO - ' + identidade['pessoa'] if liberado else 'ACESSO NEGADO'}")
    if not rostos:
        relatorio["status"] = "ACESSO NEGADO - nenhum rosto detectado"
        escrever_texto(imagem, relatorio["status"], 8, 30, VERMELHO)
        print("  ACESSO NEGADO - nenhum rosto detectado")
    salvar_resultados(imagem, relatorio, destino)
    print(f"  Resultado: {destino}")
    if mostrar:
        mostrar_imagem(imagem)
