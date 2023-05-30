document.addEventListener('DOMContentLoaded', function () {

    let navbar = document.querySelector('.header .flex .navbar');

    document.querySelector('#menu-btn').onclick = () =>{
        navbar.classList.toggle('active');
    }

    window.onscroll = () =>{
        navbar.classList.remove('active');
    }

    document.querySelectorAll('input[type="number"]').forEach(inputNumber => {
        inputNumber.oninput = () =>{
            if(inputNumber.ariaValueMax.length > inputNumber.maxLength) inputNumber.value
            = inputNumber.value.slice(0, inputNumber.maxLength);
        };
    })

    const btnheader = document.querySelectorAll('.header .flex .btn');

    const modalOverlay = document.querySelector('.modal-overlay');

    const modals = document.querySelectorAll('.modal');

    btnheader.forEach((el) => {
        el.addEventListener('click', (e) =>{
            let path = e.currentTarget.getAttribute('data-path');

            modals.forEach((el) => {
                el.classList.remove('modal--visible');
            })

            document.querySelector(`[data-target="${path}"]`).classList.add('modal--visible')
            modalOverlay.classList.add('modal-overlay--visible');
        })
    })

    modalOverlay.addEventListener('click', (e) =>{

        if(e.target == modalOverlay){
            modalOverlay.classList.remove('modal-overlay--visible');
            modals.forEach((el) => {
                el.classList.remove('modal--visible');
            })
        }
    })

    async function checkToken() {
        const token = localStorage.getItem('token');
        if (!token) {
            return false;
        }

        const response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            return true;
        } else {
            return false;
        }
    }
    
    window.addEventListener('load', async () => {
        const isAuthorized = await checkToken();
      
        if (isAuthorized) {
            const loginBtn = document.querySelector('#login-btn');
            const registerBtn = document.querySelector('#register-btn');
            loginBtn.style.display = 'none';
            registerBtn.style.display = 'none';
        }else{
            const myOrdersBtn = document.querySelector('#myorders-btn');
            myOrdersBtn.style.display = 'none';
            myOrdersBtn.disabled = true;
        }
    });
})