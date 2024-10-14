import genanki
import typer
from rich.progress import track

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
    print(result["translatedText"])
    
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

def make_deck(book_name, sent):
    sent_keys = list(sent.keys())
    
    for i in track(range(len(sent)), description="translating sentences..."):
        note_list.append(genanki.Note(
            model=my_model,
            fields=[
            f"{sent_keys[i]}: {sent[sent_keys[i]]}",
            f"{translate_text("en", sent_keys[i])}: {translate_text("en", sent[sent_keys[i]])}"
        ]
        ))
    
    """
    my_note = genanki.Note(
    model=my_model,
    fields=['Capital of Argentina', 'Buenos Aires'])
    """
    
    my_deck = genanki.Deck(
    2059400110,
    book_name)
    
    for item in note_list:
        my_deck.add_note(item)
    
    genanki.Package(my_deck).write_to_file('output.apkg')

if __name__ == "__main__":
    typer.run(translate_text)
