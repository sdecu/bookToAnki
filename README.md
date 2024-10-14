# bookToAnki
convert a book to an anki deck based off the most common words
go to google console
create a new project
select project
go to api & services
search for and enable "Cloud Translation API" after clicking "Library"
Select Credentials
Select service accounts
name it "booktoanki"
select "Cloud Translation API Admin"

install google cloud cli https://cloud.google.com/sdk/docs/install#deb
run gcloud init and select your project with the api enabled
run gcloud auth application-default login

