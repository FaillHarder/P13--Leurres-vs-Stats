// navbar ActiveClass
// let list = document.querySelectorAll('.list');

// function setActiveClass() {
//     list.forEach((item) =>
//         item.classList.remove('active'));
//     this.classList.add('active');
// }
// list.forEach((item) =>
//         item.addEventListener('click', setActiveClass))
    // end navbar


// statistique by choice (template stats)
let buttonList = document.querySelectorAll(".btn-display");
buttonList.forEach((item) =>
    item.addEventListener("click", function() {
        let table = item.nextElementSibling;
        let icon = item.firstChild.nextSibling;
        if (table.classList.contains("d-none")) {
            table.classList.remove("d-none");
            icon.setAttribute("name", "close-outline");
        } else {
            table.classList.add("d-none");
            icon.setAttribute("name", "arrow-down-outline");
        }
    })
)
// end statistique by choice

// search (template search)
const top3Submit = document.getElementById('top3-submit');
const searchForm = document.getElementById('search-form');
const resultDiv = document.getElementById('result');
const noResultClassList = ["title", "text-center", "text-white", "m-5"]
const columnLureList = ['Top', 'Leurre'];
const columnColorList = ['Top', 'Couleur', 'Image'];

// requete ajax
async function ajaxRequest(url, data, csrftoken) {
    let request = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    let jsonData = await request.json()
    return jsonData
}

top3Submit.addEventListener('click', async function(e) {
    e.preventDefault();
    top3Submit.disabled = true;
    let formData = new FormData(searchForm);
    let csrfToken = searchForm['csrfmiddlewaretoken'].value;
    // let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    clearResultDiv();
    displayLoader();
    await delay(20);

    let result = await ajaxRequest("search", formData, csrfToken);
    if (result["lures"].length > 0) {
        displayTableLure(resultDiv, result["lures"]);
        displayTableColor(resultDiv, result["colors"]);
    } else {
        displayNoResult(noResultClassList);
    };
    top3Submit.disabled = false;
})

function displayNoResult(noResultClassList) {
    let newDiv = document.createElement("div");
    newDiv.classList.add(...noResultClassList)
    newDiv.innerHTML += "Aucun résultat";
    resultDiv.appendChild(newDiv);
}

function displayLoader() {
    const loader = document.querySelector(".loader");
    if (loader.classList.contains('d-none')) {
        loader.classList.replace("d-none", "d-flex");
        setTimeout(displayLoader, 2000)
    } else if (loader.classList.contains('d-flex')){
        loader.classList.replace("d-flex", "d-none");
    }
}

function delay(n){
    return new Promise(function(resolve){
        setTimeout(resolve,n*100);
    });
}

function clearResultDiv() {
    if (resultDiv.hasChildNodes()) {
        while(resultDiv.firstChild) {
            resultDiv.removeChild(resultDiv.firstChild);
        }
    }
}

function displayTableLure(div, data) {
    const thead = createThead(columnLureList);
    const tbody = createTbodyLure(data);
    const table =  `
    <table class="table table-dark table-striped">
        ${thead}
        ${tbody}
    </table>
    `
    div.innerHTML += table
}

function displayTableColor(div, data) {
    const thead = createThead(columnColorList);
    const tbody = createTbodyColor(data);
    const table =  `
    <table class="table table-dark table-striped">
        ${thead}
        ${tbody}
    </table>
    `
    div.innerHTML += table
}

function createTbodyLure(trList) {
    let tr = "";
    for (let i = 0; i < trList.length; i++) {
        const newTr = `
            <tr>
                <th scope="row">${i+1}</th>
                <td>${trList[i]}</td>
            </tr>
        `
        tr += newTr
    }
    const tbody = `
        <tbody>
            ${tr}
        </tbody>
    `
    return tbody
}

function createTbodyColor(trList) {
    let tr = "";
    for (let i = 0; i < trList.length; i++) {
        const newTr = `
            <tr>
                <th scope="row">${i+1}</th>
                <td>${trList[i][0]}</td>
                <td>
                    <img src="media/${trList[i][1]}" alt="${trList[i][0]}">
                </td>
            </tr>
        `
        tr += newTr
    }
    const tbody = `
        <tbody>
            ${tr}
        </tbody>
    `
    return tbody
}

function createThead(thList) {
    let th = "";
    for (let i = 0; i < thList.length; i++) {
        const newTh = `
            <th class="text-primary" scope="col">${thList[i]}</th>
        `
        th += newTh
    }
    const thead = `
        <thead>
            <tr>
                ${th}
            </tr>
        </thead>
    `
    return thead
}

// end search