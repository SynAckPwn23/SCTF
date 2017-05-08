from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from challenges.models import Challenge


@login_required
def index(request):
    user = request.user
    parameters = {
        'challenges_count': Challenge.objects.count(),
        'total_points_count': Challenge.objects.total_points(),
        'user_points_count': user.solved_challenges.total_points(),
    }
    return render(request, 'scoreboard/index.html', parameters)

