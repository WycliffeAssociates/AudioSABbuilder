from xml.dom.minidom import Document, parse
from tinytag import TinyTag
from mutagen.mp3 import MP3
import json
import os

generic_app_def_location = "/home/dan/repos/AudioSABbuilder/resources/AudioBible.appDef"
output_app_def_location = "/home/dan/repos/AudioSABbuilder/resources/audiobible_modified.appDef"

def get_chapter_number(file):
    file_info = TinyTag.get(file.name)
    return str(int(json.loads(file_info.artist)['chapter']))

class BookXMLGenerator:
    def __init__(self, book_slug, book_type, anthology, files=None):
        if files is None:
            files = []
        self.root = Document()
        # self.book_name = book_name
        self.book_slug = book_slug.upper()
        self.book_type = book_type
        self.anthology = anthology
        # self.sub_group = sub_group
        self.num_chapters = len(files)
        self.files = files

    def get_text_node(self, text=''):
        return self.root.createTextNode(text)

    def get_chapter_file_by_num(self, chapter_num):
        for file in self.files:
            if int(get_chapter_number(file)) == chapter_num:
                return file
        return None

    def get_book_tag(self):
        book_el = self.root.createElement('book')
        book_el.setAttribute('id', self.book_slug)
        book_el.setAttribute('type', self.book_type)

        for tag in self.get_book_header():
            book_el.appendChild(tag)
        for file in self.files:
            book_el.appendChild(
                self.get_audio_tag(file, 'a1')
            )
        book_el.appendChild(self.get_features_tag())

        return book_el

    def get_book_header(self):
        name_el = self.root.createElement('name')
        group_el = self.root.createElement('group')
        # sub_group_el = self.root.createElement('sub-group')
        audio_image_filename_el = self.root.createElement('audio-image-filename')
        filename_el = self.root.createElement('filename')

        name_el.appendChild(self.get_text_node())
        group_el.appendChild(self.get_text_node(self.anthology))
        # sub_group_el.appendChild(self.get_text_node(self.sub_group))
        audio_image_filename_el.appendChild(self.get_text_node('null'))
        filename_el.appendChild(self.get_text_node())

        return [
            name_el,
            group_el,
            # sub_group_el,
            self.get_audio_chapters_tag(),
            audio_image_filename_el,
            filename_el
        ]

    def get_audio_chapters_tag(self):
        audio_chapters_el = self.root.createElement('audio-chapters')

        chapters = []
        for file in self.files:
            chapters.append(get_chapter_number(file))

        audio_chapters_el.setAttribute('value', ','.join(chapters))

        return audio_chapters_el

    def get_audio_tag(self, file, src=''):
        audio_el = self.root.createElement('audio')
        audio_el.setAttribute('chapter', get_chapter_number(file))

        filename_el = self.root.createElement('filename')

        filename_el.setAttribute('src', src)
        filename_el.setAttribute('len', str(round(1000 * MP3(file.name).info.length)))
        filename_el.setAttribute('size', str(os.path.getsize(file.name)))
        filename_el.appendChild(
            self.get_text_node("/audio/{}".format(os.path.basename(file.name)))
        )

        audio_el.appendChild(filename_el)

        return audio_el

    def get_features_tag(self):
        features_el = self.root.createElement('features')
        features_el.setAttribute('type', 'book')

        features = [
            {'name' : 'show-chapter-numbers', 'value' : 'inherit'},
            {'name' : 'audio-goto-next-chapter', 'value' : 'inherit'},
            {'name' : 'lock-orientation', 'value' : 'none'}
        ]

        for feature in features:
            feature_el = self.root.createElement('feature')
            feature_el.setAttribute('name', feature['name'])
            feature_el.setAttribute('value', feature['value'])

            features_el.appendChild(feature_el)

        return features_el

    def write_to_app_def_file(self):
        book_el = self.get_book_tag()
        xml_dom = parse(generic_app_def_location)

        books_el = xml_dom.getElementsByTagName('books')[0]
        books_el.appendChild(book_el)

        f = open(output_app_def_location, "w")
        f.write(xml_dom.toxml())
        f.close()

        return output_app_def_location


# system_files = [
#     open("/home/dj/Documents/BibleAudioFiles/tit/en_nt_ulb_tit_c01.mp3"),
#     open("/home/dj/Documents/BibleAudioFiles/tit/en_nt_ulb_tit_c02.mp3"),
#     open("/home/dj/Documents/BibleAudioFiles/tit/en_nt_ulb_tit_c03.mp3")
# ]
#
# xml_gen = BookXMLGenerator('TIT', 'audio-only', 'NT', system_files)
# print(xml_gen.get_book_tag().toprettyxml())
# xml_gen.write_to_app_def_file()