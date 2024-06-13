import os
import json
import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from plyer import filechooser

from .utils import get_internal_storage_path, load_data, save_data
from selectable_pdf_item import PDFListView, SelectablePDFItem

class SectionManager(BoxLayout):
    genres = ListProperty(
        ['ArtisticHub', 'NovelNest', 'StorySaga', 'BrainyBooks', 'ThinkTankTome', 'SkillSetSavvy', 
         'FinanceFortune', 'VentureVoyage', 'MindMatters', 'MindMuscleBooks', 'DisciplineDomain', 
         'InterviewInsight', 'CodeCogitation', 'AlgoArena', 'PyramidPassion', 'JavaJourney', 'RLand', 
         'CCodeCraze', 'SQLSanctuary', 'MathsMystique', 'DataDive', 'DataDreams', 'HackHaven', 
         'ProjectPinnacle', 'AptiAgora', 'BodyLanguageBoulevard', 'CertifiCity','MosaicMiscellany', 
         'MiscellanyMingle', 'EtceteraEmporium', 'AssortedAssortment' ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_genre = None
        self.current_pdf = None
        self.pdf_data = self.load_data()
        self.update_pdf_list()

    def get_genres(self):
        return self.genres if self.genres else []

    def clear_pdfs(self):
        self.pdf_data.clear()
        self.update_pdf_list()

    def update_pdf_list(self):
        if self.current_genre:
            pdf_list = self.pdf_data.get(self.current_genre, [])
            self.ids.pdf_list.clear_widgets()
            pdf_view = PDFListView(pdf_list, self)  # Pass self as parent
            self.ids.pdf_list.add_widget(pdf_view)
            self.ids.pdf_list.height = len(pdf_list) * 56
            print(f"PDF list for genre {self.current_genre}: {pdf_list}")
        else:
            self.ids.pdf_list.clear_widgets()
            self.ids.pdf_list.height = 0
            print("No genre selected, PDF list is empty.")

    def add_pdf(self):
        file_paths = self.open_file_dialog()
        if file_paths:
            pdf_name = os.path.basename(file_paths[0])
            if self.current_genre:
                if self.current_genre not in self.pdf_data:
                    self.pdf_data[self.current_genre] = []
                self.pdf_data[self.current_genre].append(pdf_name)
                self.update_pdf_list()
                self.save_data()
                print(f"Added PDF '{pdf_name}' to genre '{self.current_genre}'.")
            else:
                print("No genre selected. Cannot add PDF.")
        else:
            print("No file selected.")

    def view_pdf(self):
        if self.current_genre:
            if self.current_pdf:
                pdf_path = get_internal_storage_path(os.path.join(self.current_genre, self.current_pdf))
                print("PDF Path:", pdf_path)
                if os.path.exists(pdf_path):
                    if platform.system() == 'Windows':
                        os.startfile(pdf_path)
                    else:
                        print("Viewing PDF is not supported on this platform.")
                else:
                    print(f"PDF file '{self.current_pdf}' not found.")
            else:
                print("No PDF selected. Cannot view PDF.")
        else:
            print("No genre selected. Cannot view PDF.")

    def delete_pdf(self, *args):
        if self.current_genre:
            if self.current_pdf:
                pdf_list = self.pdf_data.get(self.current_genre, [])
                if self.current_pdf in pdf_list:
                    pdf_list.remove(self.current_pdf)
                    self.update_pdf_list()
                    self.save_data()
                    print(f"Deleted PDF '{self.current_pdf}' from genre '{self.current_genre}'.")
                    self.current_pdf = None  # Clear the current PDF selection
                else:
                    print(f"PDF '{self.current_pdf}' not found in genre '{self.current_genre}'.")
            else:
                print("No PDF selected to delete.")
        else:
            print("No genre selected. Cannot delete PDF.")
             

    def save_data(self):
        save_path = get_internal_storage_path('pdf_data.json')
        save_data(save_path, self.pdf_data)
        print("Data saved successfully.")

    def has_pdfs(self):
        for pdf_list in self.pdf_data.values():
            if pdf_list:
                return True
        return False

    def load_data(self):
        load_path = get_internal_storage_path('pdf_data.json')
        return load_data(load_path)

    def update_genre(self, genre):
        self.current_genre = genre
        self.update_pdf_list()
        print(f"Current genre updated to: {self.current_genre}")

    def update_selected_pdf(self, pdf_name):
        self.current_pdf = pdf_name
        print(f"Current PDF updated to: {self.current_pdf}")

    @staticmethod
    def open_file_dialog():
        return filechooser.open_file(title="Pick a PDF file", filters=[("PDF Files", "*.pdf")])