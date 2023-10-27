// Dark Mode - Light Mode
const toggle = document.getElementById('darkModeToggle')

if(toggle){
    toggle.addEventListener('click', function(){
        if(document.body.getAttribute('data-bs-theme') == 'dark'){
            document.body.setAttribute('data-bs-theme', 'light');
            localStorage.setItem("theme", "light");
        }else{
            document.body.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem("theme", "dark");
        }
    })
}

if(localStorage.getItem('theme') == 'dark'){
    document.body.setAttribute('data-bs-theme','dark')
}else{
    document.body.setAttribute('data-bs-theme','light')
}

// Form + api
const inputs = document.getElementsByTagName('input');
const labels = document.getElementsByTagName('label');
const select = document.getElementsByTagName('select');
const textarea = document.getElementById('id_roomproblemreason')
const countrySelect = document.getElementById('countrySelect')
const passaport = document.getElementById('passaport')
const textareaAll = document.getElementsByTagName('textarea')
const tckimlik = document.getElementById('tckimlik')

if (countrySelect) {
    const country = async () => {
        try {
            const request = await fetch('https://restcountries.com/v3.1/all')
            const response = await request.json();
            const cca2Array = response.map(country => country.cca2)
            cca2Array.sort()
            cca2Array.forEach(country => {
                let optionCountry = document.createElement("option");
                optionCountry.value = country;
                optionCountry.textContent = country;
                countrySelect.appendChild(optionCountry)
                // Reuqired Ver
                countrySelect.onchange = function (e) {
                    // Eğer ki TR Seçili İse Form
                    if (e.target.value == "TR") {
                        tckimlik.setAttribute('required', '')
                    } else {
                        tckimlik.removeAttribute('required')
                    }
                    // Eğer ki TR Seçili Değilse Form
                    if (e.target.value !== "TR") {
                        passaport.setAttribute('required', '')
                    } else {
                        passaport.removeAttribute('required')
                    }
                }
            })
        } catch (error) {
            console.log("apiden gelen hata", error);
        }
    }
    country()
}

if (textarea) {
    textarea.classList.add('form-control', 'mb-3')
    textarea.rows = 5
}


for (let i = 0; i < labels.length; i++) {
    const label = labels[i];
    label.classList.add('form-label');

    // Yeni div oluştur
    const div = document.createElement('div');
    div.classList.add("mb-3");

    // Labellerı divin içine taşı
    label.parentElement.insertBefore(div, label);
    div.appendChild(label);

    // İlgili inputu bul
    for (let j = 0; j < inputs.length; j++) {
        if (inputs[j].type == 'text' || inputs[j].type == 'number') {
            inputs[j].classList.add('form-control');

            // İlgili label ile inputu bir araya getir
            if (label.htmlFor === inputs[j].id) {
                label.parentElement.insertBefore(inputs[j], label.nextSibling);
            }
        } else if (inputs[j].type == 'checkbox') {
            inputs[j].classList.add('form-check-input', 'ms-2');

            // İlgili label ile inputu bir araya getir
            if (label.htmlFor === inputs[j].id) {
                label.parentElement.insertBefore(inputs[j], label.nextSibling);
            }
        }
        else if (inputs[j].type == 'date') {
            inputs[j].classList.add('form-control')
            if (label.htmlFor === inputs[j].id) {
                label.parentElement.insertBefore(inputs[j], label.nextSibling)
            }
        }
        else if (inputs[j].type == 'datetime-local') {
            inputs[j].classList.add('form-control')
            if(label.htmlFor === inputs[j].id){
                label.parentElement.insertBefore(inputs[j],label.nextSibling)
            }
        }
    }
    for (let k = 0; k < select.length; k++) {
        select[k].classList.add('form-select')
        if (label.htmlFor == select[k].id) {
            label.parentElement.insertBefore(select[k], label.nextSibling)
        }
    }
    for (let o = 0; o < textareaAll.length; o++) {
        textareaAll[o].classList.add('form-control')
        if (label.htmlFor == textareaAll[o].id) {
            label.parentElement.insertBefore(textareaAll[o], label.nextSibling)
        }
    }
}


// Message İçin Alert

const alertDiv = document.getElementById('alertDiv')

if(alertDiv){
    window.onload = function(){
        setTimeout(function(){
            alertDiv.style.display = 'none'
        }, 2000)
    }
}