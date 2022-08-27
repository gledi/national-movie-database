from django.db.models.signals import post_save

from .models import Movie


def movie_saved_handler(sender, instance, created, *args, **kwargs):
    with open("post_save.txt", "a", encoding="utf-8") as f:
        f.write(f"sender={sender}, instance={instance}, created={created}\n")


def movie_saved_handler_other(sender, instance, created, *args, **kwargs):
    print("movie saved::sender =", sender)
    print("movie saved::instance =", instance)
    print("movie saved::created =", created)
    print("movie saved::args =", args)
    print("movie saved::kwargs =", kwargs)


post_save.connect(movie_saved_handler, sender=Movie)
post_save.connect(movie_saved_handler_other, sender=Movie)
