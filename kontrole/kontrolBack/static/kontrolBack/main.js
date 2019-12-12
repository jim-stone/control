

// let allQuestions;

// function getQBs () {

//     fetch('/api/blocks')
//         .then(function(response) {return response.json()})
//         .then(function(data) {console.log (data);})
// };

// let selectBlock = document.querySelector('#id_block');
// selectBlock.classList.add('custom-select');

let block = document.querySelector('#id_block')
document.onload = function (ev) {
    block.value = '';
    console.log ('loaded...');
}


// get all questions
function getQuestions () {
    fetch('/api/questions')
        .then(response => response.json())
        .then(data => {
            let block = document.querySelector('#id_block');

            block.onchange = function() {
                let selectedBlock = block.options[block.selectedIndex].value;
                
                let allOptions = document.getElementsByClassName('form-check-input');
                // console.log(allOptions);
                
                let k;
                for (k = 0; k < allOptions.length; k++) {
                    allOptions[k].checked = false;
                };
                
                let relevantQuestions = data
                    .filter(question => {return question.block == selectedBlock})
                    .map(question => String(question.id))
 
                let inputs = document.querySelectorAll('[name="questions"]');
                let i;
                for (i = 0; i < inputs.length; i++) {

                    if (relevantQuestions.includes(inputs[i].getAttribute('value'))) {
                        inputs[i].parentElement.style.display = 'block'
                    } else {
                        inputs[i].parentElement.style.display = 'none'; 
                    }
                }
            }
        })
}
getQuestions()
