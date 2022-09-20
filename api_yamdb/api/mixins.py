from rest_framework import mixins


class ListCreateDestroyMixins(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin
):
    pass
