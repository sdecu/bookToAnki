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
words = None

with open('./dict5k.json') as f:
    words = json.load(f)

i = 1
for i in range(1, len(words) + 1):
    note_list.append(genanki.Note(model=my_model, fields=[words[str(i)], words[str(i)]]))

my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires'])


my_deck = genanki.Deck(
  2059400110,
  'montecristo')

for item in note_list:
    my_deck.add_note(item)

genanki.Package(my_deck).write_to_file('output.apkg')
