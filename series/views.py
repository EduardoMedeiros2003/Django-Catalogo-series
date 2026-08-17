from django.shortcuts import render

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .schemas import Serie


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
        with open("series.json", "r", encoding="utf-8") as arquivo:
            series = json.load(arquivo)

        series.append(serie.model_dump())

        with open("series.json", "w", encoding="utf-8") as arquivo:
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
# Create your views here.
