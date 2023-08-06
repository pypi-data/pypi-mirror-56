""" Url router for the explore federated search application
"""
from django.conf.urls import url, include

import core_explore_federated_search_app.views.user.ajax as user_ajax
import core_explore_federated_search_app.views.user.views as user_views

urlpatterns = [
    url(r'^get_data_sources', user_ajax.get_data_source_list_federated,
        name='core_explore_federated_search_app_get_data_sources'),
    url(r'^update_data_sources', user_ajax.update_data_source_list_federated,
        name='core_explore_federated_search_app_update_data_sources'),
    url(r'^data', user_views.ViewData.as_view(),
        name='core_explore_federated_search_app_data_detail'),
    url(r'^rest/', include('core_explore_federated_search_app.rest.urls')),
]
