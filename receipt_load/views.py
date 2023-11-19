from django.shortcuts import render
from django.views import View
from receipt_load.read_json import reed_json



# Create your views here.

class ReceiptLoad(View):
    def get(self, request):
        return render(request, 'receipt_load/load_file.html')

    def post(self, request):
        reed_json(request.FILES['receipts'])
        return render(request, 'receipt_load/load_file.html')
