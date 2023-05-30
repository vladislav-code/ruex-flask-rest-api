let inputs = document.querySelectorAll('input[type="tel"]');
let im = new Inputmask('+7 (999) 999-99-99');
im.mask(inputs);

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form');
    form.addEventListener('submit', formSend);

    async function formSend(e) {
        e.preventDefault();

        let error = formValidate(form);

        let formData = new FormData(form); 
        
        const data = {};

        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        const jsonData = JSON.stringify(data);

        if (error === 0){
            form.classList.add('_sending');
            let response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonData
            });
            if (response.ok) {
                let result = await response.json();
                alert(result.message);
                form.reset();
                form.classList.remove('_sending');
            }else{
                alert("Ошибка");
                form.classList.remove('_sending');
                console.log(response);
            }
        }else{
            
        }

    }

    function formValidate(form) {
        let error = 0;
        let formReq = document.querySelectorAll('._req');

        for (let index = 0; index < formReq.length; index++) {
            const input = formReq[index];
            formRemoveError(input);

            if(input.classList.contains('_tel')){
                if(input.value.includes("_") || input.value.length < 3){
                    formAddError(input);
                    error++;
                }
            }else {
                if(input.value === '') {
                    formAddError(input);
                    error++;
                }
            }
        }
        return error;
    }

    function formAddError(input) {
        input.parentElement.classList.add('_error');
        input.classList.add('_error');
        let errorDiv = document.createElement('div');
        errorDiv.classList.add('error-message');
        errorDiv.innerText = 'Ошибка ввода';
        input.parentElement.appendChild(errorDiv);
    }

    function formRemoveError(input) {
        input.parentElement.classList.remove('_error');
        input.classList.remove('_error');
        let errorDivs = input.parentElement.querySelectorAll('.error-message');
        errorDivs.forEach(errorDiv => {
            input.parentElement.removeChild(errorDiv)
        })
    }
})