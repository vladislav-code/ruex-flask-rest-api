const SERVICES_PRICES = {
"Orders": [
    {
    "dir": "Оценка и экспертиза",
    "service": "Оценка рыночной стоимости объектов недвижимого имущества",
    "object": "квартира",
    "subject": "для нотариуса",
    "price": 2500,
    "time": "От 1 дней"
    },
    {
    "dir": "Оценка и экспертиза",
    "service": "Оценка рыночной стоимости объектов недвижимого имущества",
    "object": "загородный дом",
    "subject": "для органов опеки",
    "price": 2500,
    "time": "От 1 дней"
    }
],
"Orders2": [
    {
    "dir": "Страхование",
    "service": "оценка ущерба после залива, пожара, иных повреждений (квартиры, дома, ТМЦ, грузы, спецтехника, воздушный и водный транспорт и тд.)",
    "object": "грузовой авто или спецтехника",
    "subject": "",
    "price": 30000,
    "time": "От 3 дней"
    }
]
}

const firstSelect = document.getElementById('filter-direction');
const secondSelect = document.getElementById('filter-service');
const thirdSelect = document.getElementById('filter-object');
const fourthSelect = document.getElementById('filter-subject');
const selectPrice = document.getElementById('end_price');
const selectDate = document.getElementById('end_date');

let dirValues = [];

for (let key in SERVICES_PRICES) {
  SERVICES_PRICES[key].forEach(item => {
    if (item.dir && !dirValues.includes(item.dir)) {
      dirValues.push(item.dir);
    }
  });
}

let select = document.getElementById('filter-direction');
dirValues.forEach(value => {
  let option = document.createElement('option');
  option.value = value;
  option.text = value;
  select.appendChild(option);
});

firstSelect.addEventListener('change', () => {
    selectPrice.value = "Ожидаем фильтров";
    selectDate.value = "Ожидаем фильтров";
    secondSelect.innerHTML = '<option value="">Не выбрано</option>';
    thirdSelect.innerHTML = '<option value="">Не выбрано</option>'; 
    fourthSelect.innerHTML = '<option value="">Не выбрано</option>';
    thirdSelect.disabled = true;
    fourthSelect.disabled = true;
    const selectedDir = firstSelect.value;

    let serviceValues = [];

    for (let key in SERVICES_PRICES){
        SERVICES_PRICES[key].forEach(item => {
            if (item.dir === selectedDir && item.service && !serviceValues.includes(item.service)) {
                serviceValues.push(item.service);
            }
        })
    }

    let select = document.getElementById('filter-service');
    serviceValues.forEach(value => {
        let option = document.createElement('option');
        option.value = value;
        option.text = value;
        select.appendChild(option);
    });
    secondSelect.disabled = false;

    if (firstSelect.value === "Не выбрано") {
        secondSelect.disabled = true;
        thirdSelect.disabled = true;
        fourthSelect.disabled = true;
    }
})

secondSelect.addEventListener('change', () => {
    selectPrice.value = "Ожидаем фильтров";
    selectDate.value = "Ожидаем фильтров";
    thirdSelect.innerHTML = '<option value="">Не выбрано</option>'; 
    fourthSelect.innerHTML = '<option value="">Не выбрано</option>';
    fourthSelect.disabled = true;
    const selectedDir = firstSelect.value;
    const selectedService = secondSelect.value;

    let objectValues = [];

    for (let key in SERVICES_PRICES){
        SERVICES_PRICES[key].forEach(item => {
            if(item.dir === selectedDir && item.service === selectedService && item.object && !objectValues.includes(item.object)) {
                objectValues.push(item.object);
            }
        })
    }

    let select = document.getElementById('filter-object');
    objectValues.forEach(value => {
        let option = document.createElement('option');
        option.value = value;
        option.text = value;
        select.appendChild(option);
    });
    thirdSelect.disabled = false;

    if (secondSelect.value === "") {
        thirdSelect.disabled = true;
        fourthSelect.disabled = true;
    }
})

thirdSelect.addEventListener('change', () => {
    selectPrice.value = "Ожидаем фильтров";
    selectDate.value = "Ожидаем фильтров";
    fourthSelect.innerHTML = '<option value="">Не выбрано</option>';
    const selectedDir = firstSelect.value;
    const selectedService = secondSelect.value;
    const selectedObject = thirdSelect.value;

    let subjectValues = [];

    for (let key in SERVICES_PRICES){
        SERVICES_PRICES[key].forEach(item => {
            if(item.dir === selectedDir && item.service === selectedService && 
                item.object === selectedObject && item.subject != "" && !subjectValues.includes(item.subject)) {
                subjectValues.push(item.subject);
            }
        })
    }

    let select = document.getElementById('filter-subject');
    subjectValues.forEach(value => {
        let option = document.createElement('option');
        option.value = value;
        option.text = value;
        select.appendChild(option);
    });
    fourthSelect.disabled = false;

    if (thirdSelect.value === "") {
        fourthSelect.disabled = true;
        let selectPrice = document.getElementById('end_price');
        let selectDate = document.getElementById('end_date');
        selectPrice.value = "Ожидаем фильтров";
        selectDate.value = "Ожидаем фильтров";
    }

    if (subjectValues.length === 0) {
        fourthSelect.disabled = true;
        let selectPrice = document.getElementById('end_price');
        let selectDate = document.getElementById('end_date');
        for (let key in SERVICES_PRICES){
            SERVICES_PRICES[key].forEach(item => {
                if(item.dir === selectedDir && item.service === selectedService && 
                    item.object === selectedObject) {
                    selectPrice.value = item.price;
                    selectDate.value = item.time;
                }
            })
        }
        selectPrice.disabled = true;
        selectDate.disabled = true;
    }
})

fourthSelect.addEventListener('change', () => {
    const selectedDir = firstSelect.value;
    const selectedService = secondSelect.value;
    const selectedObject = thirdSelect.value;
    const selectedSubject = fourthSelect.value;

    let selectPrice = document.getElementById('end_price');
    let selectDate = document.getElementById('end_date');
    for (let key in SERVICES_PRICES){
        SERVICES_PRICES[key].forEach(item => {
            if(item.dir === selectedDir && item.service === selectedService && 
                item.object === selectedObject && item.subject === selectedSubject) {
                selectPrice.value = item.price;
                selectDate.value = item.time;
            }
        })
    }
    selectPrice.disabled = true;
    selectDate.disabled = true;
    
    if (selectedSubject === "") {
        selectPrice.value = "Ожидаем фильтров";
        selectPrice.textContent = "Ожидаем фильтров";
        selectDate.value = "Ожидаем фильтров";
        selectDate.textContent = "Ожидаем фильтров";
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('onlineOrderForm');
    const formDocuments = document.getElementById('formDocuments');
    const formPreview = document.getElementById('formPreview');
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    form.addEventListener('submit', formSend);
    
    async function formSend(e) {
        e.preventDefault();

        let error = formValidate(form);

        let selectPrice = document.getElementById('end_price');
        let selectDate = document.getElementById('end_date');
        selectPrice.disabled = false;
        selectDate.disabled = false;

        let formData = new FormData(form);

        selectPrice.disabled = true;
        selectDate.disabled = true;
        
        let files = form.formDocuments.files;
        
        for (let i = 0; i < files.length - 1; i++) {
            formData.append(`documents${i+1}`, files[i]);
        }
        
        if (error === 0) {
            form.classList.add('_sending');
            let response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                body: formData
            });
            if (response.ok) {
                formPreview.innerHTML = '';
                form.reset();
                form.classList.remove('_sending');
            }else {
                form.classList.remove('_sending');
            }
        }
    }

    function formValidate(form) {
        let error = 0;
        let formReq = document.querySelectorAll('._reqPay');

        for (let index = 0; index < formReq.length; index++) {
            const input = formReq[index];
            formRemoveError(input);

            if(input.classList.contains('_price')) {
                if(input.value === '' || input.value === 'Ожидаем фильтров') {
                    formAddError(input);
                    error++;
                }
            }else if (input.classList.contains('_date')) {
                if(input.value === '' || input.value === 'Ожидаем фильтров') {
                    formAddError(input);
                    error++;
                }
            }else if (input.getAttribute("type") === "checkbox" && input.checked === false){
                formAddError(input);
                error++;
            }else if(input.classList.contains('_files')) {
                if (input.value === "") {
                    formAddError(input);
                    error++;
                }
            }
        }
        return error;
    }

    formDocuments.addEventListener('change', (event) => {
        let error = 0;
        formRemoveError(formDocuments);
        const maxSize = 15 * 1024 * 1024; // 15 MB
        let totalSize = 0;
        const files = event.target.files;
        for (let i = 0; i < files.length; i++) {
            const fileType = formDocuments.files[i].type;
            if (!allowedTypes.includes(formDocuments.files[i].type)){
                formDocuments.value = '';
                formAddError(formDocuments);
                error++;
                const imgElements = formPreview.querySelectorAll('div');
                imgElements.forEach((img) => {
                    formPreview.removeChild(img);
                });
                return;
            }
            const file = files[i];
            totalSize += file.size;
    
            if (totalSize > maxSize) {
                formDocuments.value = '';
                formAddError(formDocuments);
                error++;
                const imgElements = formPreview.querySelectorAll('div');
                imgElements.forEach((img) => {
                    formPreview.removeChild(img);
                });
                return;
            }

            var reader = new FileReader();
            reader.onload = function (e) {
                const fileElement = document.createElement('div');
                if (fileType.includes('image')){
                    fileElement.innerHTML = `<img src = "${e.target.result}" alt="Документ">`;
                    formPreview.appendChild(fileElement);
                }else if (fileType.includes('pdf')) {
                    fileElement.innerHTML = `<object data="${e.target.result}" type="application/pdf"></object>`;
                    formPreview.appendChild(fileElement);
                }else if (fileType.includes('word')) {
                    fileElement.innerHTML = `<iframe src="https://view.officeapps.live.com/op/view.aspx?src=${e.target.result}" sandbox="allow-scripts"></iframe>`;
                    formPreview.appendChild(fileElement);
                }
            }
            reader.onerror = function (e) {
                alert('Ошибка');
            }
            reader.readAsDataURL(formDocuments.files[i]);
        }
    })

    function formAddError(input) {
        input.parentElement.classList.add('_error');
        input.classList.add('_error');
        let errorDiv = document.createElement('div');
        errorDiv.classList.add('error-message');
        errorDiv.innerText = 'Заполните корректно';
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