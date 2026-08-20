from django.shortcuts import render

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .schemas import Serie
from pathlib import Path
from .database import buscar_por_titulo

BASE_DIR = Path(__file__).resolve().parent.parent
SERIES_FILE = BASE_DIR / "series.json"

@csrf_exempt
def criar_serie(request):
    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método HTTP não permitido."},
            status=405
        )

    try:
        dados = json.loads(request.body)
        serie = Serie(**dados)

    except json.JSONDecodeError:
        return JsonResponse(
            {"erro": "O corpo da requisição deve ser um JSON válido."},
            status=400
        )

    except Exception as erro:
        return JsonResponse(
            {"erro": str(erro)},
            status=400
        )

    try:
        with open(SERIES_FILE, "r", encoding="utf-8") as arquivo:
            series = json.load(arquivo)

        series.append(serie.model_dump())

        with open(SERIES_FILE, "w", encoding="utf-8") as arquivo:
            json.dump(series, arquivo, ensure_ascii=False, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        return JsonResponse(
            {"erro": "Não foi possível acessar o arquivo de séries."},
            status=500
        )

    return JsonResponse(
        {
            "mensagem": "Série cadastrada com sucesso!",
            "serie": serie.model_dump()
        },
        status=201
    )


def listar_series(request):
    if request.method != "GET":
        return JsonResponse(
            {"erro": "Método HTTP não permitido."},
            status=405
        )

    try:
        with open(SERIES_FILE, "r", encoding="utf-8") as arquivo:
            series = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return JsonResponse(
            {'erro': 'não foi possível acessar o arquivo de séries.'},
        )
    return JsonResponse(series, safe=False, status=200)


@csrf_exempt
def series(request):
    if request.method == 'GET':
        return listar_series(request)

    if request.method == 'POST':
        return criar_serie(request)

    return JsonResponse(
        {'erro': 'Método HTTP não permitido.'},
        status=405
    )
# Create your views here.
def buscar_serie(request, titulo):
    serie = buscar_por_titulo(titulo)

    if serie is None:
        return JsonResponse(
            {"detail": "Série não encontrada."},
            status=404
        )

    return JsonResponse({
        "titulo": serie[0],
        "genero": serie[1],
        "ano_lancamento": serie[2],
        "temporadas": serie[3]
    })