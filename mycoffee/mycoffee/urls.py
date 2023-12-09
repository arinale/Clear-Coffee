
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('',include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/ ',include('orders.urls')),
    path('products/',include('products.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
