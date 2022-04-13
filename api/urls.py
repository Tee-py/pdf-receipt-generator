from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views as api_views
from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', api_views.root, name="root"),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('api/create_user/', api_views.CreateUserView.as_view(), name="create_user"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/receipt/', api_views.ReceiptView.as_view(), name="receipt"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='docs'),
    #path('api/docs/redoc/', SpectacularRedocView.as_view(), name='docs'),
]