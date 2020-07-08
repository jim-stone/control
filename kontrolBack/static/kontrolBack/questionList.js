const urlBlocks = '/api/blocks'
const urlQuestions = '/api/questions';
const blocksMenu = document.querySelector('#blocks_menu');
const resultPlace = document.querySelector('#result')

// przy odświeżaniu strony ładuje pustą opcję
// ze zwględu na event on change
blocksMenu.selectedIndex = 0
let p1 = fetch(urlBlocks);
let p2 = fetch(urlQuestions);


// pierwszy promise zwraca 2 promisy !
Promise.all([p1, p2])
    .then(responses => Promise.all(
        responses.map(resp => resp.json()
        )))

    .then(data => {
        const blocksArray = data[0];
        const questionsArray = data[1];

        // dropdown
        blocksArray.forEach(block => {
            let newOption = document.createElement('option');
            let newOptionText = document.createTextNode(block.name);
            newOption.appendChild(newOptionText);
            newOption.setAttribute('value', block.id);
            newOption.setAttribute('data-questions', block.questions);
            blocksMenu.appendChild(newOption);
        });


        // event na dropdown
        blocksMenu.addEventListener('change', function (event) {
            let newElement = document.createElement('div');
            let selectedOptionQuestions = blocksMenu[blocksMenu.selectedIndex]
                .dataset.questions.split(',');

            // filtrowanie listy pytań
            function filterQuestionsByBlocks(question) {
                console.log(selectedOptionQuestions);
                console.log(question.id, typeof (question.id));
                return selectedOptionQuestions.includes(String(question.id))
            };

            const filteredQuestions = questionsArray.filter(filterQuestionsByBlocks);
            console.log(filteredQuestions);

            // generowanie html
            try {
                let oldTable = resultPlace.getElementsByTagName('table')[0];
                oldTable.remove();
            }
            catch (error) {
                // pass
            }

            let resultElement = document.createElement('table');
            resultPlace.appendChild(resultElement);

            filteredQuestions.forEach(element => {
                let row = document.createElement('tr');
                let cellOne = document.createElement('td');
                let q = document.createTextNode(element.name);
                cellOne.appendChild(q);
                row.appendChild(cellOne);
                resultElement.appendChild(row);

            });
        });
    });
























