from django.conf.urls import url

from equipment.views import EquipmentsView, EquipmentTypesView, DetailTypeView, EquipmentLocationsView, DetailLocationView

urlpatterns = (
    url(r'^$', EquipmentsView.as_view(), name='equipments'),
    url(r'^types/$', EquipmentTypesView.as_view(), name='equipments_types'),
    url(r'^type/(?P<pk>\d+)$', DetailTypeView.as_view(), name='equipment_type'),
    url(r'^emplacements/$', EquipmentLocationsView.as_view(), name='equipments_locations'),
    url(r'^emplacement/(?P<pk>\d+)$', DetailLocationView.as_view(), name='equipment_emplacement')
)
