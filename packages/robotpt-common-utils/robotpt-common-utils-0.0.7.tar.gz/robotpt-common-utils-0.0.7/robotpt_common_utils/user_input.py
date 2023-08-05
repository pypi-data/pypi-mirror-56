YES_CHOICES = ['yes', 'yup', 'y', 'correct', 'yessir', 'yeah', 'si']
NO_CHOICES = ['no', 'nope', 'n', 'incorrect', 'nah']


def is_yes(text):

    if type(text) is not str:
        raise TypeError

    if text.lower() in YES_CHOICES:
        return True
    elif text.lower() in NO_CHOICES:
        return False
    else:
        raise ValueError