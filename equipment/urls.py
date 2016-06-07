from django.conf.urls import url

from equipment.views import EquipmentsView

urlpatterns = (
    url(r'^$', EquipmentsView.as_view(), name='equipments'),
)