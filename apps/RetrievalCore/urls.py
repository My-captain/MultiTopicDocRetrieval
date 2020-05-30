from django.urls import path, re_path
from RetrievalCore import views

urlpatterns = [
    re_path(r'^list/(?P<user_id>\d+)/(?P<flag>\d+)/', views.DocumentListView.as_view(), name="document_list"),
    re_path(r'^detail/(?P<document_id>\d+)/(?P<session_id>\d+)/$', views.DocumentDetailView.as_view(), name="document_detail"),
    path('login/', views.UserLogin.as_view(), name="user_login"),
    path('register/', views.UserRegister.as_view(), name="user_register"),
    re_path(r'^assess/(?P<session_id>\d+)/(?P<flag>\d+)/', views.PreferenceAssess.as_view(), name="preference_assess"),
    re_path(r'^preference_customize/(?P<user_id>\d+)/(?P<flag>\d+)/', views.UserPreference.as_view(), name="user_preference"),
    re_path(r'^record_preference/(?P<user_id>\d+)/(?P<flag>\d+)/', views.RecordPreference.as_view(), name="record_preference"),
    re_path(r'^topic_choose/(?P<user_id>\d+)/', views.TopicChooseView.as_view(), name="topic_choose"),
]

app_name = 'RetrievalCore'
