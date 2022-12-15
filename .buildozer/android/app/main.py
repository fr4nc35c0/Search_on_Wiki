"""Main module"""
import certifi
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest


class WikiRead(MDApp):
    """ Main Class """

    dialog_info = None
    dialog_contact = None

    def build(self):
        """Overwrite the build function to build the app"""
        self.title = 'Search on Wiki'
        self.theme_cls.theme_style = 'Light'  # Dark
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.primary_hue = '300'
        return Builder.load_file('layout.kv')

    def wiki_search(self):
        """Take the input and search the given argument"""
        query = self.root.ids['mdinput'].text
        if query != '':
            self.get_data(title=query)

    def wiki_search_rand(self):
        """Set the endpoint for a random argument"""
        endpoint = \
            "https://de.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json"
        self.root.ids['mdlabel'].text = '\nLoading...'
        self.rs_request = UrlRequest(endpoint,
                                     on_success=self.get_data,
                                     ca_file=certifi.where())

    def get_data(self, *args, title=None):
        """Get a selected argument or a random argument"""
        if title is None:
            response = args[1]
            article = response['query']['random'][0]
            title = article['title']
        endpoint = \
            f'https://de.wikipedia.org/w/api.php?prop=extracts&explaintext&exintro&format=json&action=query&titles={title.replace(" ","%20")}'
        self.rs_request_data = UrlRequest(endpoint,
                                          on_success=self.set_text_area,
                                          ca_file=certifi.where())

    def set_text_area(self, request, response):
        """Set the text inside a label with the received text argument"""
        extracted_info = response['query']['pages']
        page_id = next(iter(extracted_info))
        page_title = extracted_info[page_id]['title']
        try:
            page = extracted_info[page_id]['extract']
        except KeyError:
            page = 'Sorry! Nothing matched your search terms!'
        self.root.ids['mdlabel'].text = \
            f'\n[b][size=20sp][color=6A329F]{page_title}[/color][/size][/b]\n\n{page}'

    def show_info_app(self):
        """Show the information about the App"""
        str_info_app = 'by Francesco Cocciro\n\nANG. - Punkt und Gut GmbH'
        if not self.dialog_info:
            self.dialog_info = MDDialog(
                title='Search on Wiki',
                text=str_info_app,
                auto_dismiss=True
            )
        self.dialog_info.open()

    def show_contact(self):
        """Show the contact for feedback"""
        str_contact = 'maxmustermann@email.de'
        if not self.dialog_contact:
            self.dialog_contact = MDDialog(
                title='Contact',
                text=str_contact,
                auto_dismiss=True
            )
        self.dialog_contact.open()


WikiRead().run()
