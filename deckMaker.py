import genanki
import json
import click

import os

from google.cloud import translate_v3

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


# Initialize Translation client
def batch_translate_to_english(
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    language_code: str = "fr",
) -> translate_v3.TranslateTextResponse:
    """Translating Text from English.
    Args:
        text: The content to translate.
        language_code: The language code for the translation.
            E.g. "fr" for French, "es" for Spanish, etc.
            Available languages: https://cloud.google.com/translate/docs/languages#neural_machine_translation_model
    """

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"
    # Translate text from English to chosen language
    # Supported mime types: # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        contents=[text],
        target_language_code=language_code,
        parent=parent,
        mime_type="text/plain",
        source_language_code="en-US",
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")
    # Example response:
    # Translated text: Bonjour comment vas-tu aujourd'hui?

    return response
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
    click.echo("Text: {}".format(result["input"]))
    click.echo("Translation: {}".format(result["translatedText"]))
    click.echo("Detected source language: {}".format(result["detectedSourceLanguage"]))
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
    click.echo(len(fr))
    click.echo(i)
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

if __name__ == "__main__":
    click.echo("")
