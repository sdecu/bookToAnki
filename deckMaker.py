import genanki
import json

def translate_text(target: str, text: str):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    """
    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))
    """
    return result["translatedText"]

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
    print(len(fr))
    print(i)
    note_list.append(genanki.Note(
        model=my_model,
        fields=[
        f"{fr_keys[i]}: {fr[fr_keys[i]]}",
        f"{translate_text("en", fr_keys[i])}: {translate_text("en", fr[fr_keys[i]])}"
    ]
    ))

"""
my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires'])
"""

my_deck = genanki.Deck(
  2059400110,
  "le'tranger 2")

for item in note_list:
    my_deck.add_note(item)

genanki.Package(my_deck).write_to_file('output.apkg')
