from yandex_music import YandexMusicObject


class Normalization(YandexMusicObject):
    def __init__(self,
                 gain,
                 peak,
                 client=None,
                 **kwargs):
        self.gain = gain
        self.peak = peak

        self.client = client
        self._id_attrs = (self.gain, self.peak)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Normalization, cls).de_json(data, client)

        return cls(client=client, **data)
