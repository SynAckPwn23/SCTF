from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.
@login_required
def index(request):
	user = request.user
	parameters = {
	}
	return render(request, 'user/index.html', parameters)