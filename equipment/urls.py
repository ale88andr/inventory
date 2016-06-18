from django.conf.urls import url

from equipment.views import EquipmentsView, EquipmentTypesView, DetailTypeView

urlpatterns = (
    url(r'^$', EquipmentsView.as_view(), name='equipments'),
    url(r'^types/$', EquipmentTypesView.as_view(), name='equipments_types'),
    url(r'^type/(?P<pk>\d+)$', DetailTypeView.as_view(), name='equipment_type')
)
