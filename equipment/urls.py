from django.conf.urls import url

from equipment.views import EquipmentIndexView, EquipmentTypesView, EquipmentTypeView, EquipmentLocationsView, EquipmentEmplacementView, EquipmentChownView

urlpatterns = (
    url(r'^$', EquipmentIndexView.as_view(), name='index'),
    url(r'^types/$', EquipmentTypesView.as_view(), name='types'),
    url(r'^type/(?P<pk>\d+)$', EquipmentTypeView.as_view(), name='type'),
    url(r'^emplacements/$', EquipmentLocationsView.as_view(), name='locations'),
    url(r'^emplacement/(?P<pk>\d+)$', EquipmentEmplacementView.as_view(), name='emplacement'),
    url(r'(?P<pk>\d+)/chown/$', EquipmentChownView.as_view(), name='chown')
)
