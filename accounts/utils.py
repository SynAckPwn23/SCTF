from collections import Counter


def group_solved_by_category(element):
    """
    :param element: UserProfile or Team (needs element.solved_challenges)
    :return: dict: {Category: #solved}
    """
    return Counter(c.category.name for c in element.team.solved_challenges)


def user_without_team(user):
    return user.profile.team is None