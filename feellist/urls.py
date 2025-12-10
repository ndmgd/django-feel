from django.urls import path

from feellist import views

urlpatterns = [
    # 列表/新增接口
    path('userscore/', views.UserScoreListView.as_view(), name='user-score-list'),
    # 详情/修改/删除接口（pk为模型ID）
    path('userscore/<int:pk>/', views.UserScoreDetailView.as_view(), name='user-score-detail'),
]
