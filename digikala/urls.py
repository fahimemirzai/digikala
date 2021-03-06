"""digikala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

from graphene_django.views import GraphQLView #################### FOR GRAPH_QL
from .schema import schema #################### FOR GRAPH_QL


schema_view = get_swagger_view(title='digikala_api')

urlpatterns = [
    path('zarinpal/', include('app_zarinpal.urls')),
    path('admin/', admin.site.urls),
    path('api/product/', include('app_product.urls')),
    path('api/accounts/', include('app_accounts.urls')),
    path('', schema_view),

    path('graphql/',GraphQLView.as_view(schema=schema, graphiql=True)), #################### FOR GRAPH_QL
    # path('graphql',PrivateGraphQLView.as_view(graphiql=True, schema=schema)), #################### FOR GRAPH_QL



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
