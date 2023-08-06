import shutil
from pathlib import Path

from fp_xls_2_xml import xls2xml, xml2xls

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window


Builder.load_string('''
<Tair>:
    TextInput:
        text: 'drag and drop the file into this window'
        font_size: 30
        padding_x:
            [self.center[0] - self._get_text_width(max(self._lines, key=len), self.tab_width, self._label_cached) / 2.0,
            0] if self.text else [self.center[0], 0]
        padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
''')
class Tair(BoxLayout):
    pass


class FPXLS2XML(App):
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.tair = Tair()
        return self.tair

    def _on_file_drop(self, window, file_path):
        file = Path(file_path.decode())
        try:
            if "xls" in file.name[-5:]:
                out = file.parent / "out.xml"
                xls2xml(file, out)
            else:
                out = file.parent / "out.xls"
                xml2xls(file, out)
            content = Label(text='Saved to: {}'.format(out))
            popup = Popup(title="Success!", content=content, auto_dismiss=False)
            content.bind(on_touch_down=popup.dismiss)
            popup.open()
        except Exception:
            content = Label(text='Failed to save: {}'.format(file))
            popup = Popup(title="Failed!", content=content, auto_dismiss=False)
            content.bind(on_touch_down=popup.dismiss)
            popup.open()


if __name__ == '__main__':
    FPXLS2XML().run()