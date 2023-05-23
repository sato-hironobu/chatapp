import os
import django
import openpyxl

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test.settings")
django.setup()

from main.models import FAQ

wb = openpyxl.load_workbook("faq_list.xlsx")
ws = wb.worksheets[0]

l = []
for i in range(1, ws.max_row):
    if ws[f"I{i}"].value == None:
         break

    # column I = questions, column J = answers
    l.append(FAQ(
        question=ws[f"I{i}"].value,
        answer=ws[f"J{i}"].value,
    ))

FAQ.objects.bulk_create(l)