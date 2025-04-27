

import polib
import pathlib

langs = ['fr']

for lang in langs:
    pofile = polib.pofile(pathlib.Path('.') / 'locales' / lang / 'LC_MESSAGES' / 'messages.po')
    pofile.save_as_mofile(pathlib.Path('.') / 'locales' / lang / 'LC_MESSAGES' / 'messages.mo')
