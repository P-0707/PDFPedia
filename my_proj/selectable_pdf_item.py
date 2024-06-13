from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle

class SelectablePDFItem(BoxLayout):
    is_selected = BooleanProperty(False)  # Add a property to track selection
    parent_widget = ObjectProperty(None)

    def __init__(self, pdf_name, parent, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.pdf_name = pdf_name
        self.parent_widget = parent  # Set the parent reference

        self.label = Label(text=pdf_name)
        self.add_widget(self.label)

        # Bind to the property to update the visual state
        self.bind(is_selected=self.update_visual_state)

        # Update visual state initially
        self.update_visual_state()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent_widget.update_selected_pdf(self.pdf_name)
            # Set the selected state
            self.is_selected = True
            return True
        return super().on_touch_down(touch)

    def update_visual_state(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(0.5, 0.7, 0.9, 1)  # Light blue color for selected state
            else:
                Color(0.529, 0.808, 0.922, 1)  # White color for default state
            Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.update_visual_state()

class PDFListView(BoxLayout):
    def __init__(self, pdf_list, parent, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.parent_widget = parent  # Set the parent reference
        self.update_pdf_list(pdf_list)

    def update_pdf_list(self, pdf_list):
        self.clear_widgets()
        for pdf_name in pdf_list:
            pdf_item = SelectablePDFItem(pdf_name, self.parent_widget)
            self.add_widget(pdf_item)

        # Reset selection when updating the list
        self.parent_widget.update_selected_pdf(None)
