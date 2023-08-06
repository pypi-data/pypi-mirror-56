# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_midicsv', 'py_midicsv.midi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-midicsv',
    'version': '1.10.0',
    'description': 'A library for converting MIDI files from and to CSV format',
    'long_description': '# py_midicsv\n\n[![CircleCI](https://circleci.com/gh/timwedde/py_midicsv.svg?style=svg)](https://circleci.com/gh/timwedde/py_midicsv)\n[![codecov](https://codecov.io/gh/timwedde/py_midicsv/branch/master/graph/badge.svg)](https://codecov.io/gh/timwedde/py_midicsv)\n\nA Python library inspired by the midicsv tool (originally found [here](http://www.fourmilab.ch/webtools/midicsv/)).\n\n## Disclaimer\nThis library is currently in Beta. This means that the interface might change and that the encoding scheme is not yet finalised. Expect slight inconsistencies.\n\n## Installation\npy_midicsv is available from PyPI, so you can install via `pip`:\n```bash\n$ pip install py_midicsv\n```\n\n## Usage\n```python\nimport py_midicsv\n\n# Load the MIDI file and parse it into CSV format\ncsv_string = py_midicsv.midi_to_csv("example.mid")\n\n# Parse the CSV output of the previous command back into a MIDI file\nmidi_object = py_midicsv.csv_to_midi(csv_string)\n\n# Save the parsed MIDI file to disk\nwith open("example_converted.mid", "wb") as output_file:\n    midi_writer = py_midicsv.FileWriter(output_file)\n    midi_writer.write(midi_object)\n```\n\n## Differences\nThis library adheres as much as possible to how the original library works, however generated files are not guaranteed to be entirely identical when compared bit-by-bit.  \nThis is mostly due to the handling of meta-event data, especially lyric events, since the encoding scheme has changed. The original library did not encode some of the characters in the Latin-1 set, while this version does.\n',
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'url': 'https://github.com/timwedde/py_midicsv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
