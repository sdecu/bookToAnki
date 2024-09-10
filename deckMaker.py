import genanki
import json

my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'French'},
    {'name': 'English'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{French}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{English}}',
    },
  ])

note_list = []
fr = None
en = None

with open('./sentences.json') as f:
    fr = json.load(f)

with open('./senteng.json') as f:
    en = json.load(f)

fr_keys = list(fr.keys())
en_keys = list(en.keys())

for i in range(len(fr)):
    note_list.append(genanki.Note(
        model=my_model,
        fields=[
        f"{fr_keys[i]}: {fr[fr_keys[i]]}",
        f"{en_keys[i]}: {en[en_keys[i]]}"
    ]
    ))

"""
my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires'])
"""

my_deck = genanki.Deck(
  2059400110,
  "le'tranger")

for item in note_list:
    my_deck.add_note(item)

genanki.Package(my_deck).write_to_file('output.apkg')
