import json

from rag.infra.mongoRepository import findByQuery
from rag.service.openAiService import functionCallService


def ragService(request):
    ## 추천 목록 조회
    recommend = findByQuery(request.command)
    result = functionCallService(request, recommend)

    clean = result.replace("json", "").replace("```", "")
    return convert(clean)


def convert(data):
    try:
        return json.loads(data)
    except:
        return data

