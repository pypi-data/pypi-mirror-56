class MixerTemplate:
    def __init__(
        self,
        get_mute_method,
        set_mute_method,
        get_volume_method,
        set_volume_method,
    ):
        self.gmute = get_mute_method
        self.smute = set_mute_method
        self.gvol = get_volume_method
        self.svol = set_volume_method
