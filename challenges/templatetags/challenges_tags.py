from django import template

register = template.Library()


@register.simple_tag
def btn_challenge_class(current_user, challenge):
    if current_user.solved_challenges.filter(pk=challenge.pk).exists():
        return 'btn-success'
    return 'btn-primary'
