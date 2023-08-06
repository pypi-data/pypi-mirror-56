from django.http import JsonResponse, HttpResponse


def output_json(code, msg, data):
    return JsonResponse({'code': code, 'msg': msg, 'data': data})


def output_txt(message):
    return HttpResponse(message)
