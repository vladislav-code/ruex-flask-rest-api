document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-contact');

    form.addEventListener('submit', formSend);
    
    async function formSend(e) {
        e.preventDefault();

        let formData = new FormData(form);

        const data = {};

        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        const jsonData = JSON.stringify(data);
        
        form.classList.add('_sending');
        let response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        });
        if (response.ok) {
            form.reset();
            form.classList.remove('_sending');
        }else {
            form.classList.remove('_sending');
        }
    }
})