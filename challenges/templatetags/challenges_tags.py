from django import template

register = template.Library()


@register.simple_tag
def btn_challenge_class(current_user, challenge):
    if current_user.solved_challenges.filter(pk=challenge.pk).exists():
        return 'btn-success'
    return 'btn-primary'


@register.assignment_tag(takes_context=True)
def challenge_is_solved(context, *args):
    return context['user'].solved_challenges.filter(pk=context['challenge'].pk).exists()