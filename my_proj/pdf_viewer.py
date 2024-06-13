import fitz  # PyMuPDF
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class PDFViewer(Popup):
    def __init__(self, pdf_path, **kwargs):
        super().__init__(**kwargs)
        self.title = "PDF Viewer"
        self.size_hint = (1, 1)
        self.pdf_path = pdf_path
        self.content = self.build_content()
        self.load_pdf_async()

    def build_content(self):
        return BoxLayout()

    def load_pdf_async(self):
        Clock.schedule_once(self.load_pdf)

    def load_pdf(self, dt):
        try:
            doc = fitz.open(self.pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = Image(size=(pix.width, pix.height))
            self.content.add_widget(img)

            tex = Texture.create(size=(pix.width, pix.height))
            tex.blit_buffer(pix.samples, colorfmt='rgba', bufferfmt='ubyte')
            tex.flip_vertical()
            img.texture = tex

            doc.close()
        except Exception as e:
            print(f"Error loading PDF: {e}")
