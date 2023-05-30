document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('account');
    form.addEventListener('submit', formSend);
    
    async function formSend(e) {
        e.preventDefault();
        let error = formValidate(form);

        const name = document.querySelector('#name').value;
        const email = document.querySelector('#email').value;
        const phone = document.querySelector('#phone').value;
        const password = document.querySelector('#password').value;

        const formData = {
            username: name,
            password: password,
            email: email,
            phone_number: phone
        };

        if (error === 0){
            form.classList.add('_sending');
            let response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
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
        let formReq = document.querySelectorAll('._reqAcc');

        for (let index = 0; index < formReq.length; index++) {
            const input = formReq[index];
            formRemoveError(input);

            if(input.classList.contains('_tel')){
                if(input.value.includes("_") || input.value.length < 3){
                    formAddError(input);
                    error++;
                }
            }else if (input.classList.contains('_pass')) {
                if(passwordTest(input)) {
                    formAddError(input);
                    error++;
                    return;
                }
            }
        }
        return error;
    }

    function passwordTest(input) {
        return !/(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/.test(input.value);
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