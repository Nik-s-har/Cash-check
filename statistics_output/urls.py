from django.urls import path
from statistics_output.views import month_statistics, itemization, year_statistics

urlpatterns = [
    path('<int:year>', year_statistics),
    path('<int:year>/<int:month>', month_statistics),
    path('<int:year>/<int:month>/<str:category>', itemization)
]