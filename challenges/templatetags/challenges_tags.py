from django import template

register = template.Library()


@register.simple_tag
def btn_challenge_class(current_user, challenge):
    if current_user.profile.solved_challenges.filter(pk=challenge.pk).exists():
        return 'btn-success'
    if current_user.profile.team is not None and \
        current_user.profile.team.solved_challenges.filter(pk=challenge.pk).exists():
        return 'btn-info'
    return 'btn-primary'


@register.simple_tag(takes_context=True)
def challenge_is_solved(context, *args):
    return context['user'].profile.solved_challenges.filter(pk=context['challenge'].pk).exists()