from django.urls import path
from .views import HomePageView, login_page_view, logout_view, send_message_view

app_name = 'sender'
urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('login/', login_page_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('send/', send_message_view, name='send')
]