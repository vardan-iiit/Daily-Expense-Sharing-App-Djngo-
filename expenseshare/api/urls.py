from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ExpenseViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('expenses/user/<int:user_id>/', ExpenseViewSet.as_view({'get': 'get_user_expenses'})),
    path('expenses/overall/', ExpenseViewSet.as_view({'get': 'overall_expenses'})),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('expenses/balancesheet/', ExpenseViewSet.as_view({'get': 'download_balance_sheet'}),name="balancesheet"),
    
]
