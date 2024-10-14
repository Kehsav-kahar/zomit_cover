from django.urls import path
from . import views
from .generate import GenerateCoverView
from .generate import GetAllGeneratedCoversView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.get_cover, name='get_cover'),  # For GET all
    path('add/', views.add_cover, name='add_cover'),  # For POST
    path('update/<int:pk>/', views.update_cover, name='update_cover'),  # For PUT (update)
    path('delete/<int:pk>/', views.delete_cover, name='delete_cover'),  # For DELETE
    path('generate_cover/', GenerateCoverView.as_view(), name='generate_cover'),
    path('generated-covers/', GetAllGeneratedCoversView.as_view(), name='get_all_generated_covers'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])