import smtplib
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Mail
from email.mime.text import MIMEText


auth_password = None


class HomePageView(ListView):
	template_name = 'home.html'
	model = Mail
	context_object_name = 'mails'

	username = ''

	def get(self, request, *args, **kwargs):
		self.queryset = Mail.objects.filter(from_addr=request.user.username)
		return super().get(request, *args, **kwargs)


def login_page_view(request):

	if request.method.lower() == 'post':

		username = request.POST.get('username')
		password = request.POST.get('password')

		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(username, password)
			server.quit()
			global auth_password
			auth_password = password
		except:
			print("we can't log in")
			return redirect('sender:login')

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = User.objects.create_user(username=username, password=password)
			user.save()
		else:
			user.set_password(password)
			user.save()
			auth_user = authenticate(request, username=username, password=password)
			if auth_user is None:
				return redirect('sender:login')
			else:
				login(request, auth_user)
				return redirect('sender:home')

	return render(request, 'login.html')


def logout_view(request):
	global auth_password
	auth_password = None
	logout(request)
	return redirect('sender:login')


def send_message_view(request):

	if not request.user.is_authenticated:
		return redirect('sender:login')

	if request.method.lower() == 'post':
		from_addrs = request.user.username
		to_addrs = request.POST['to']
		subject = request.POST['subject']
		body = request.POST['body']

		message = MIMEText(body)
		message['Subject'] = subject
		message['From'] = from_addrs
		message['To'] = to_addrs

		server = smtplib.SMTP('smtp.gmail.com', 587)

		server.starttls()

		global auth_password

		server.login(request.user.username, auth_password)

		server.sendmail(from_addrs, to_addrs, message.as_string())

		mail = Mail.objects.create(from_addr=request.user.username, to_addr=to_addrs, subject=subject, body=body)
		mail.save()

		return redirect('sender:home')


	return render(request, 'send_message.html')


def error_404_view(request, exception):

	return render(request, '404.html')