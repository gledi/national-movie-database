import io
import secrets
from typing import Any

from django.core.files.images import ImageFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .avatargenerator import generate_avatar_from_name
from .models import Profile, User


def _gen_avatar(name: str, variant: str) -> ImageFile:
    img = generate_avatar_from_name(name, font_variant="bold")
    filename = "{}_{}.png".format(slugify(name).replace("-", "_"), secrets.token_hex(5))
    output = io.BytesIO()
    img.save(output, format="png")
    output.seek(0)
    return ImageFile(output, name=filename)


@receiver(post_save, sender=User)
def user_saved_handler(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: Any,
) -> None:
    if created:
        at_sign_ix = instance.email.index("@")
        nickname = instance.email[:at_sign_ix][:32]
        profile, _ = Profile.objects.get_or_create(
            user=instance, defaults={"nickname": nickname}
        )
        img = _gen_avatar(instance.get_full_name(), variant="bold")
        profile.photos.create(
            photo=img,
            caption=instance.get_full_name(),
            is_primary=True,
        )
