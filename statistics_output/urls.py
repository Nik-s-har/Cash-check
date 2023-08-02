from django.urls import path
from statistics_output.views import month_statistics, itemization, year_statistics

urlpatterns = [
    path('<str:year>', year_statistics),
    path('<str:year>/<str:month>', month_statistics),
    path('<str:year>/<str:month>/<str:category>', itemization)
]