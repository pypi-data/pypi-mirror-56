import alsaaudio
from .template import MixerTemplate


class Mixer(MixerTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(
            get_mute_method=self._gmute,
            set_mute_method=self._smute,
            get_volume_method=self._gvol,
            set_volume_method=self._svol,
            *args,
            **kwargs,
        )
        self.mixer_name = "Master"

    def _gmute(self):

        mute_channels = alsaaudio.Mixer(control=self.mixer_name).getmute()

        mute = self._channel_average(mute_channels)

        return mute

    def _smute(self, new_mute):

        new_mute = bool(new_mute)

        alsaaudio.Mixer(control=self.mixer_name).setmute(new_mute)
        return new_mute

    def _gvol(self):

        volume_channels = alsaaudio.Mixer(control=self.mixer_name).getvolume()

        vol = self._channel_average(volume_channels)

        return vol

    def _svol(self, new_vol):

        new_vol = int(new_vol)

        alsaaudio.Mixer(control=self.mixer_name).setvolume(new_vol)
        return new_vol

    def _channel_average(self, channels):

        channel_sum = 0
        num_channels = len(channels)

        for channel in channels:
            channel_sum += channel

        return int(channel_sum / num_channels)


# print(alsaaudio.mixers())
# mixer = alsaaudio.Mixer(control='Master')
#
# print(mixer.cardname())
# print(mixer.mixer())
# print(mixer.mixerid())
# print(mixer.switchcap())
# print(mixer.volumecap())
# print(mixer.getenum())
# print(mixer.getmute())
# print(mixer.getrange())
# # print(mixer.getrec())
# print(mixer.getvolume())
# # print(mixer.setvolume())
# # print(mixer.setmute())
# # print(mixer.setrec())
# print(mixer.polldescriptors())
# print(mixer.handleevents())
