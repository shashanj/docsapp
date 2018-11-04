from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'docs_appa_ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^ola/customer/', include('customer.urls')),
    url(r'^ola/dashboard/', include('dashboard.urls')),
    url(r'^ola/driver/', include('driver.urls'))
]
