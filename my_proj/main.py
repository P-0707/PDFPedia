import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from sections.section_manager import SectionManager
from kivy.base import EventLoop


Builder.load_file('pdf_manager.kv')

class PDFPediaApp(App):
    def build(self):
        return SectionManager()
    
    def restart_app(self):
        self.clear_pdfs()

        # Close the current application instance
        EventLoop.close()

        # Restart the application by creating a new instance and running it
        PDFPediaApp().run()
    
    def clear_pdfs(self):
        # Check if there are any PDFs present
        if self.root.has_pdfs():
            # Clear the PDF data structure or storage here
            # For example, if your PDF data is stored in SectionManager, you can call a method to clear it
            self.root.clear_pdfs() 
        else:
            print("No PDFs present to clear.")

if __name__ == '__main__':
    PDFPediaApp().run()