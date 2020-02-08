## KontrolMaster
KontrolMaster to aplikacja do zarządzania kontrolami projektów.


## Funkcjonalności

Aplikacja przewiduje dwa rodzaje użytkowników.

Superkontroler:
* nadzoruje cały system,
* zarządza obiektami Pytanie, Blok, Instytucja, Użytkownik.

Kontroler:
* przygotowuje listy sprawdzające i przeprowadza kontrole poprzez wypełnianie list sprawdzających. 


## Technologie
Python:
* Django==3.0.2
* django-crispy-forms==1.8.1
* django-rest-knox==4.1.0
* djangorestframework==3.11.0

Javascript: jQuery

## Instalacja i uruchomienie

```
git clone https://github.com/jim-stone/control.git
python manage.py makemigrations
python manage.py migrate
(w przypadku problemów z migracją należy zakomentować kod w plikach *urls, views, forms*)
python manage.py runserver
```

## Licencja

Najbezpieczniejszym sposobem traktowania kodu, dla którego nie została określona licencja, jest traktowanie go jako własnościowy.
