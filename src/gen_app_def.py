from xml.dom.minidom import Document, parse
root = Document()

def append_to_book_el(book_el):
    # Name #############################################################################################################
    name_el = root.createElement('name')
    name_el.appendChild(root.createTextNode('Genesis'))
    book_el.appendChild(name_el)

    # Abbrev ###########################################################################################################
    abbrev_el = root.createElement('abbrev')
    abbrev_el.appendChild(root.createTextNode('Gen'))
    book_el.appendChild(abbrev_el)

    # Group ############################################################################################################
    group_el = root.createElement('group')
    group_el.appendChild(root.createTextNode('OT'))
    book_el.appendChild(group_el)

    # Sub-Group ########################################################################################################
    sub_group_el = root.createElement('sub-group')
    sub_group_el.appendChild(root.createTextNode('Pentateuch'))
    book_el.appendChild(sub_group_el)

    # Filename #########################################################################################################
    filename_el = root.createElement('filename')
    filename_el.appendChild(root.createTextNode('01-GEN.usfm'))
    book_el.appendChild(filename_el)

    # Source ###########################################################################################################
    source_el = root.createElement('source')
    source_el.appendChild(root.createTextNode('/home/dan/Downloads/b1cdb05baa.zip'))
    book_el.appendChild(source_el)

    # Page #############################################################################################################
    book_el.appendChild(get_page('1', '/home/dj/Downloads/my_custom_file1.mp3', 'a1', '11624', '155637'))
    book_el.appendChild(get_page('2', '/home/dj/Downloads/my_custom_file2.mp3', 'a1', '8516', '114881'))
    for num in range(3, 51): book_el.appendChild(get_page(str(num), has_audio=False))

def get_page(num, filename='', src='', length='', size='', has_audio=True):
    page_el = root.createElement('page')
    page_el.setAttribute('num', num)

    # short circuit
    if not has_audio:
        page_el.appendChild(root.createTextNode('\n'))
        return page_el

    audio_el = root.createElement('audio')

    filename_el = root.createElement('filename')
    filename_el.setAttribute('src', src)
    filename_el.setAttribute('len', length)
    filename_el.setAttribute('size', size)
    filename_el.appendChild(root.createTextNode(filename))

    audio_el.appendChild(filename_el)

    page_el.appendChild(audio_el)

    return page_el

xml_dom = parse("/home/dj/PycharmProjects/HackathonSummer2020/resources/bible.appDef")

for book in xml_dom.getElementsByTagName('book'):
    if book.getAttribute('id') == "GEN":
        while book.hasChildNodes():
            book.removeChild(book.firstChild)
        append_to_book_el(book)

with open("/home/dj/PycharmProjects/HackathonSummer2020/resources/bible2.appDef", "w") as f:
    f.write(xml_dom.toxml())
