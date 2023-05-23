from django.http.response import JsonResponse
from django.views import generic
from .models import FAQ, History

class Chatbot(generic.ListView):
    model = History
    template_name = "main/chatbot.html"
    context_object_name = "history"

    def get_queryset(self):
        return History.objects.all().order_by("sent_time")


def search(request):

    hist_list = []
    answer_list = []

    search_word = request.POST.get('search_word')
    hist_list.append(History(message=search_word, is_from_bot=False))
    answer_list .append({"message": search_word, "from": "user"})

    query_set = FAQ.objects.filter(question__icontains=search_word)[:5]

    if len(query_set) <= 0:
        message = f"申し訳ございません。「{search_word}」に関連する情報が見つかりませんでした。"
        hist_list.append(History(message=message, is_from_bot=True))
        answer_list.append({"message": message, "from": "bot"})

    else:
        message = f"「{search_word}」に関する質問："
        hist_list.append(History(message=message, is_from_bot=True))
        answer_list.append({"message": message, "from": "bot"})

        for item in query_set:
            message = f"【質問】{item.question}<br>【回答】{item.answer}"
            hist_list.append(History(message=message, is_from_bot=True,))
            answer_list.append({"message": message, "from": "bot"})

    History.objects.bulk_create(hist_list)
    return JsonResponse({"context": answer_list})

