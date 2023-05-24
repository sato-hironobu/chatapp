from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import generic
from .models import FAQ, History, Class, Unit, Lesson
    
def index(request):
    classes = Class.objects.all()
    return render(request, "main/chatbot.html", context={"classes": classes})


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
        answer_list.append({"message": message, "from": "bot", "type": "info"})

    else:
        message = f"「{search_word}」に関する質問："
        hist_list.append(History(message=message, is_from_bot=True))
        answer_list.append({"message": message, "from": "bot", "type": "info"})

        for item in query_set:
            question = f"【質問】{item.question}"
            answer = f"【回答】{item.answer}"
            hist_list.append(History(message=question, is_from_bot=True,))
            hist_list.append(History(message=answer, is_from_bot=True,))
            answer_list.append({"question": question, "answer": answer, "from": "bot", "type": "answer"})

    History.objects.bulk_create(hist_list)
    return JsonResponse({"context": answer_list})


def select_category(request):
    
    level = request.POST.get("level")
    name = request.POST.get("name")
    
    item_list = []
    
    if level == "Class":
        data = Unit.objects.filter(parent__name=name)
        for d in data:
            item_list.append({
                "name": d.name,
                "level": "Unit"
            })
        finished = False
    elif level == "Unit":
        data = Lesson.objects.filter(parent__name=name)
        for d in data:
            item_list.append({
                "name": d.name,
                "level": "Lesson"
            })
        finished = False
    elif level == "Lesson":
        data = FAQ.objects.filter(lesson__name=name)
        for d in data:
            item_list.append({
                "name": d.question,
                "level": "FAQ"
            })
        finished = False
    elif level == "FAQ":
        data = FAQ.objects.get(question=name)
        item_list.append({
            "question": data.question,
            "answer": data.answer
        })
        finished = True

    return JsonResponse({"context": item_list, "finished": finished})