const boxes = document.querySelectorAll('.servicesAll-container .box-container .box');
    
const domElements = {
    filters: {
    direction: document.getElementById('filter-direction'),
    date: document.getElementById('filter-date'),
    price: document.getElementById('filter-price'),
    }
}

{
    domElements.filters.direction.onchange = (event) => {
    filterBoxesTags();
    }
    domElements.filters.date.onchange = (event) => {
    filterBoxesTags();
    }
    domElements.filters.price.onchange = (event) => {
    filterBoxesTags();
    }
}

function filterBoxesTags(){
    const filterDirection = document.getElementById('filter-direction').value;

    const filterDate = document.getElementById('filter-date').value;
    
    const filterPrice = document.getElementById('filter-price').value;
    
    

    if(filterDirection === "Все"){
    if(filterDate === "Все"){
        if(filterPrice === "Все"){
        boxes.forEach(showingAll => {
            showingAll.style.display = 'block';
        })
        }else{
        
        boxes.forEach(showingByOne => {
            const tagname = showingByOne.querySelectorAll('.tags p span');
            let matchedprice = false;
            tagname.forEach(tago => {
            if(tago.textContent === filterPrice) {
                matchedprice = true;
            }
            })
            if(matchedprice === true){
            showingByOne.style.display = 'block';
            }else {
            showingByOne.style.display = 'none';
            }
        })
        }
    }else if(filterPrice === "Все"){
        
        boxes.forEach(showingByOne => {
        tagname = showingByOne.querySelectorAll('.tags p span');
        let matcheddate = false;
        tagname.forEach(tag => {
            if(tag.textContent === filterDate){
                matcheddate = true;
            }
            })
            if(matcheddate === true){
            showingByOne.style.display = 'block';
            }else{
            showingByOne.style.display = 'none';
            }
        })
    }else{
        boxes.forEach(showingByTwo => {
        tagname = showingByTwo.querySelectorAll('.tags p span');
        let matchedprice = false;
        let matcheddate = false;
        tagname.forEach(tag => {
            
            if(tag.textContent === filterPrice){
            matchedprice = true;
            }
            if(tag.textContent === filterDate){
            matcheddate = true;
            }
        })
        if(matchedprice === true && matcheddate === true){
            showingByTwo.style.display = 'block';
        }else{
            showingByTwo.style.display = 'none';
        }
        })
    }
    }else if(filterDate === "Все"){
    if(filterPrice === "Все"){
        
        boxes.forEach(showingByOne => {
        let matcheddirection = false;
        tagname = showingByOne.querySelectorAll('.tags p span');
        tagname.forEach(tag => {
            if(tag.textContent === filterDirection){
                matcheddirection = true;
            }
            })
        if(matcheddirection === true){
        showingByOne.style.display = 'block';
        }else{
        showingByOne.style.display = 'none';
        }
    })
    }else{
    boxes.forEach(showingByTwo => {
        tagname = showingByTwo.querySelectorAll('.tags p span');
        let matchedprice = false;
        let matcheddirection = false;
        tagname.forEach(tag => {
            
        if(tag.textContent === filterPrice){
            matchedprice = true;
        }
        if(tag.textContent === filterDirection){
            matcheddirection = true;
        }
        })
        if(matchedprice === true && matcheddirection === true){
        showingByTwo.style.display = 'block';
        }else{
        showingByTwo.style.display = 'none';
        }
    })
    }
    }else if(filterPrice === "Все"){
    boxes.forEach(showingByTwo => {
        tagname = showingByTwo.querySelectorAll('.tags p span');
        let matcheddate = false;
        let matcheddirection = false;
        tagname.forEach(tag => {
            
        if(tag.textContent === filterDate){
            matcheddate = true;
        }
        if(tag.textContent === filterDirection){
            matcheddirection = true;
        }
        })
        if(matcheddate === true && matcheddirection === true){
        showingByTwo.style.display = 'block';
        }else{
        showingByTwo.style.display = 'none';
        }
    })
    }else{
    boxes.forEach(showingByThree => {
        tagname = showingByThree.querySelectorAll('.tags p span');
        let matcheddate = false;
        let matcheddirection = false;
        let matchedprice = false;
        tagname.forEach(tag => {
            
        if(tag.textContent === filterDate){
            matcheddate = true;
        }
        if(tag.textContent === filterDirection){
            matcheddirection = true;
        }
        if(tag.textContent === filterPrice){
            matchedprice = true;
        }
        })
        if(matcheddate === true && matcheddirection === true && matchedprice === true){
        showingByThree.style.display = 'block';
        }else{
        showingByThree.style.display = 'none';
        }
    })
    }
}

const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', filterBoxes);

function filterBoxes(){
    const selectedMessage = this.value.toLowerCase();
    boxes.forEach(box => {
    const serviceName = box.querySelector('.service-name h3').textContent.toLowerCase();
    if(serviceName.includes(selectedMessage)){
        box.style.display = 'block';
    }else {
        box.style.display = 'none';
    }
    })
}