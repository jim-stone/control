from django.contrib.auth.models import User
from .models import Question, QuestionBlock, InstitutionEmployee, Institution


def create_employees():

    # User.objects.all().delete()
    pois_institution = Institution.objects.filter(programme__icontains='pois')[0]
    powr_institution = Institution.objects.filter(programme__icontains='powr')[0]
    u1 = User.objects.create_user(username='robert', password='M@r@don@')
    u2 = User.objects.create_user(username='diego', password='M@r@don@')
    InstitutionEmployee.objects.create(user=u1, institution=pois_institution)
    InstitutionEmployee.objects.create(user=u2, institution=powr_institution)


def create_questions():

    # Question.objects.all().delete()
    project_block = 1
    project_questions = [
        'Czy stan zaawansowania projektu przedstawiany we wnioskach o płatność jest zgodny z faktycznie wykonanymi działaniami?',
        'Czy wykonane działania zrealizowano w zakresie zgodnym z założeniami zawartymi we wniosku o dofinansowanie?',
        'Czy dokumenty przedkładane przy wnioskach o płatność są zgodne z oryginalną dokumentacją projektu?',
        'Czy oryginały dokumentów księgowych są opisane w sposób wskazujący, że nie zostały sfinansowane z różnych źródeł?'
    ]

    contract_block = 2
    contract_questions = [
        'Czy w okresie objętym kontrolą beneficjent dokonywał zamówień na podstawie ustawy Prawo Zamówień Publicznych?',
        'Czy w okresie objętym kontrolą beneficjent dokonywał zamówień w oparciu o zasadę konkurencyjności?',
        'Czy beneficjent przekazał umowę z wykonawcą?',
        'Czy beneficjent przekazał protokół odbioru robót lub zawarł stosowną adnotację na fakturze?',
        'Czy zakres wykonanych robót jest zgodny z umową z wykonawcą i wnioskiem o dofinansowanie?',
        'Czy zakres wykonanych robót został wykonany za cenę uzgodnioną w umowie z wykonawcą?',
        'Czy zakres został wykonany w terminie wskazanym w umowie z wykonawcą?',
        'Czy w przypadku nabycia nieruchomości zostały zachowane limity programowe?',
        'Czy w przypadku gdy beneficjent zrezygnował z przeprowadzenia postępowania zgodnie z zasadą konkurencyjności, czy zrobił to w sposób uprawiony?',
        'Czy przypadku gdy beneficjent wprowadzał zmiany do zawartych umów/podpisywał aneksy, czy było to zgodne z przepisami i zawartą umową z wykonawcą?'
    ]

    indicator_block = 5
    indicator_questions = [
        'Czy został osiągnięty stan zaplanowanych wskaźników, adekwatny do poziomu zaawansowania projektu?',
        'Czy informacja dotycząca wskaźników potwierdzona podczas kontroli jest zgodna z danymi wprowadzonymi do systemu informatycznego?',
    ]

    bookkeeping_blok = 3
    bookkeeping_questions = [
        'Czy jest prowadzona odrębna ewidencja księgowa dla wszystkich operacji dotyczących realizacji projektu?',
        'Czy wydatki przedstawione przez beneficjenta we wnioskach o płatność zostały ujęte w księgach rachunkowych?',
    ]

    personnel_block = 4
    personnel_questions = [
        'Czy pracownik ma w swoim zakresie obowiązków zadania dotyczące projektu?',
        'Jeżeli pracownik wykonuje także inne zadania niż dotyczące projektu czy został określony sposób obliczania kosztu jego wynagrodzenia?',
        'Czy dla osób pracujących w projekcie na niepełnym etacie i bez określenia stałej liczby godzin przedstawiono ewidencję czasu pracy?',
        'Czy zgodnie z zasadami programu obliczono stawkę godzinową dla osób pracujących w niepełnym wymiarze czasu pracy z elastyczną liczbą godzin pracy w miesiącu?',
        'Czy rzetelnie i zgodnie z zasadami programu udokumentowano koszty personelu?',
        'Jeśli przedstawiono do refundacji koszty nagród/premii/dodatków – czy spełniono zasady ich kwalifikowalności wskazane w dokumentach programowych?',
        'Jeśli beneficjent otrzymał ryczałt na koszty bezpośrednie personelu, czy w zestawieniu wydatków rzeczywistych nie przedstawił tych kosztów?'
    ]

    infopromo_block = 6
    infopromo_questions = [
        'Czy koszty poniesione na działania informacyjno-promocyjne są adekwatne i niezbędne dla osiągnięcia celów?',
        'Czy działania i materiały informacyjno-promocyjne zawierały niezbędne informacje, loga i symbole?',
        'Czy środki trwałe, pomieszczenie, w którym odbyło się wydarzenie (np. konferencja, szkolenie) zostało oznakowane zgodnie z zasadami programu?',
        'Czy Beneficjent informował opinię publiczną o otrzymanej pomocy poprzez zamieszczenie na swej stronie internetowej [jeżeli istnieje] krótkiego opisu operacji, proporcjonalnego do poziomu pomocy',
        'Czy Beneficjent umieścił przynajmniej jeden plakat (minimalny rozmiar A3) z informacjami na temat projektu oraz otrzymanego wsparcia finansowego z UE, w miejscu łatwo widocznym dla ogółu społeczeństwa, takim jak wejście do budynku?'
    ]

    concluding_block = 8
    concluding_questions = [
        '''Czy wydatki przedstawione w dotychczas złożonych wnioskach o płatność są zgodne
        z zasadami kwalifikowalności obowiązującymi w Programie, zgodnie z zapisami
        Podręcznika Programu?''',
        '''Czy dokumentacja dotycząca projektu jest przechowywana w sposób zapewniający
        dostępność, poufność i bezpieczeństwo oraz właściwą ścieżkę audytu?''',
        'Czy podczas kontroli stwierdzono wydatki niekwalifikowalne?',
        'Czy zidentyfikowano zagrożenia dla prawidłowej realizacji projektu?',
        'Czy istnieje konieczność korekty przez beneficjenta dotychczas złożonych wnioskówo płatność?',
        '''Czy istnieje konieczność wszczęcia procedury odzyskiwania nieprawidłowo wypłaconych środków?''',
        'Czy wyniku kontroli zachodzi podejrzenie wystąpienia nieprawidłowości o charakterze systemowym?',
        'Czy zostały zrealizowane zalecenia z poprzednich kontroli projektu? /jeżeli dotyczy/?',
        'Czy w wyniku kontroli stwierdzono nieprawidłowości kwalifikujące się do raportowania do KE (OLAF)?',
        'Czy w wyniku kontroli konieczne jest sformułowanie zaleceń pokontrolnych?'
    ]
    concluding_questions = [q.replace('\n', '').replace('  ', ' ') for q in concluding_questions]

    blocks = [project_block, contract_block, indicator_block, 
    bookkeeping_blok, personnel_block, infopromo_block, concluding_block]
    
    questions = [project_questions, contract_questions, indicator_questions,
    bookkeeping_questions, personnel_questions, infopromo_questions, concluding_questions]

    for q in project_questions:
        b = QuestionBlock.objects.get(pk=project_block)
        question = Question(name=q, block=b)
        question.save()
        
    for q in contract_questions:
        b = QuestionBlock.objects.get(pk=contract_block)
        question = Question(name=q, block=b)
        question.save()

    for q in indicator_questions:
        b = QuestionBlock.objects.get(pk=indicator_block)
        question = Question(name=q, block=b)
        question.save()

    for q in bookkeeping_questions:
        b = QuestionBlock.objects.get(pk=bookkeeping_blok)
        question = Question(name=q, block=b)
        question.save()

    for q in infopromo_questions:
        b = QuestionBlock.objects.get(pk=infopromo_block)
        question = Question(name=q, block=b)
        question.save()

    for q in personnel_questions:
        b = QuestionBlock.objects.get(pk=personnel_block)
        question = Question(name=q, block=b)
        question.save()

    for q in concluding_questions:
        b = QuestionBlock.objects.get(pk=concluding_block)
        question = Question(name=q, block=b)
        question.save()

        
create_employees()
create_questions()






















