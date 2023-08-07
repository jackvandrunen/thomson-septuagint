import bs4
import re


def clean_text(text):
    text = ' '.join(text.strip().split())
    return text


def load_osis(path):
    with open(path, 'r') as f:
        return bs4.BeautifulSoup(f.read(), features='xml')


def _format_text(parent, result, footnotes):
    for element in parent.children:
        if element.name == 'title':
            if element.get('type') == 'runningHead':
                pass
            elif element.get('type') == 'main':
                result.append('{0} {1}\n'.format('#' * int(element.get('level')), clean_text(element.text)))
            elif element.get('type') == 'psalm':
                result.append('\n*')
                _format_text(element, result, footnotes)
                result.append('*\n')
            elif element.get('type') is None:
                result.append('\n##### {0}\n'.format(clean_text(element.text)))
            else:
                print(element)
        elif element.name == 'div':
            _format_text(element, result, footnotes)
        elif element.name == 'chapter':
            if element.get('sID'):
                result.append('\n#### Chapter {0}\n'.format(element.get('sID').split('.')[-1]))
        elif element.name == 'p':
            if element.get('type') != 'x-nobreak':
                result.append('\n')
            if element.get('type') == 'x-embedded':
                result.append('> ')
            _format_text(element, result, footnotes)
            result.append('\n')
        elif element.name == 'verse':
            if element.get('sID'):
                result.append(' **{0}** '.format(element.get('sID').split('.')[-1]))
        elif element.name == 'transChange':
            if element.get('type') == 'added':
                result.append(' [')
                _format_text(element, result, footnotes)
                result.append('] ')
            else:
                print(element)
        elif element.name == 'speaker':
            result.append('  \n*{0}*  \n'.format(clean_text(element.text)))
        elif element.name == 'note':
            if element.get('placement') == 'foot':
                ref = element.reference
                footnotes.append(clean_text(ref.text))
                note_id = len(footnotes)
                result.append(' [[{0}]](#note-{0} "{1}") '.format(note_id, clean_text(ref.text)))
            else:
                print(element)
        elif element.name == 'lg':
            result.append('  \n')
            _format_text(element, result, footnotes)
        elif element.name == 'l':
            indent = int(element.get('level'))
            result.append('&emsp;' * indent)
            _format_text(element, result, footnotes)
            result.append('  \n')
        elif element.name == 'lb':
            result.append('\n<br />\n')
        elif element.name == 'hi':
            if element.get('type') == 'emphasis':
                result.append(' *')
                _format_text(element, result, footnotes)
                result.append('* ')
            else:
                print(element)
        elif element.name in ('name', 'divineName'):
            result.append(' *')
            _format_text(element, result, footnotes)
            result.append('* ')
        elif element.name == 'foreign':
            result.append(' *')
            _format_text(element, result, footnotes)
            result.append('* ')
        elif type(element) is bs4.element.NavigableString:
            result.append(clean_text(str(element)))
        elif type(element) is bs4.element.Comment:
            pass
        else:
            print(element)


def osis2md(osis):
    result = []
    footnotes = []
    for element in osis.find_all('div'):
        if element.get('type') == 'book':
            _format_text(element, result, footnotes)
            break
    result.append('\n\n---\n\n')
    for note_id, footnote in enumerate(footnotes, 1):
        result.append('<a name="note-{0}"></a>**[{0}]** {1}  \n'.format(note_id, footnote))
    return '{0}\n'.format(''.join(result))


if __name__ == '__main__':
    import sys
    import os
    if len(sys.argv) != 3:
        print('Missing parameters!')
        sys.exit(1)
    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    books = sorted(os.listdir(src_dir))
    for book in books:
        osis = load_osis(os.path.join(src_dir, book))
        with open(os.path.join(dest_dir, book[:-3] + 'md'), 'w') as f:
            f.write(osis2md(osis))
    #
    # if len(sys.argv) == 3:
    #     osis = load_osis(sys.argv[1])
    #     with open(sys.argv[2], 'w') as f:
    #         f.write(osis2html(osis))
    # elif len(sys.argv) == 2:
    #     osis = load_osis(sys.argv[1])
    #     with open('output.html', 'w') as f:
    #         f.write(osis2html(osis))
    # else:
    #     print('Error: No input file specified!')
