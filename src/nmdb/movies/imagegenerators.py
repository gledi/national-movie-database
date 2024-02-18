from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, Thumbnail


class ExtraLargeSpec(ImageSpec):
    processors = [ResizeToFill(600, 800)]
    format = "PNG"


class LargeSpec(ImageSpec):
    processors = [ResizeToFill(480, 640)]
    format = "PNG"


class MediumSpec(ImageSpec):
    processors = [ResizeToFill(360, 480)]
    format = "PNG"


class SmallSpec(ImageSpec):
    processors = [ResizeToFill(240, 360)]
    format = "PNG"


class ExtraSmallSpec(ImageSpec):
    processors = [ResizeToFill(120, 160)]
    format = "PNG"


class ThumbnailSpec(ImageSpec):
    processors = [Thumbnail(96, 96)]
    format = "PNG"


register.generator("movies:xl", ExtraLargeSpec)
register.generator("movies:lg", LargeSpec)
register.generator("movies:md", MediumSpec)
register.generator("movies:sm", SmallSpec)
register.generator("movies:xs", ExtraSmallSpec)
register.generator("movies:thumb", ThumbnailSpec)
