import json
import vgamepad as vg


def get_button(button_field):
    return vg.XUSB_BUTTON.__getattr__(button_field)


class Config:

    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path) as f:
            self.data = json.load(f)

    def get_button(self, label):
        try:
            return get_button(self.data[label])
        except KeyError:
            return None
