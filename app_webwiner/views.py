from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .scraper.wine_scraper import WineScrapper
from django.shortcuts import render

@require_http_methods(["POST"])  # A view responderá apenas a requisições POST
def scrape_wines(request):
    scraper = WineScrapper()
    data = scraper.scrape()  
    return JsonResponse({'status': 'completed', 'data': data})

def home(request):
    # Adicione a lógica para a sua página inicial aqui, se necessário
    return render(request, 'home.html')  # Assegure-se de que 'home.html' existe em seu diretório de templates


