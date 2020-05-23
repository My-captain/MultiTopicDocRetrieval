from django.urls import path, re_path
from apps.RetrievalCore import views

urlpatterns = [
    re_path(r'^list/', views.DocumentListView.as_view(), name="document_list"),
    re_path(r'^detail/(?P<document_id>\d+)/(?P<session_id>\d+)/$', views.DocumentDetailView.as_view(), name="document_detail"),
    path('login/', views.UserLogin.as_view(), name="user_login"),
    path('register/', views.UserRegister.as_view(), name="user_register"),
    re_path(r'^assess/', views.PreferenceAssess.as_view(), name="preference_assess"),
    re_path(r'^preference_customize/', views.UserPreference.as_view(), name="user_preference"),
    re_path(r'^record_preference/(?P<user_id>\d+)/', views.RecordPreference.as_view(), name="record_preference")
]

app_name = 'RetrievalCore'