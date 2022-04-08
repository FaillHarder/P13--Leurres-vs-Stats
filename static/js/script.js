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
const resultDiv = document.getElementById('result');
const tableClassList = ["table", "table-dark", "table-striped"];
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
    let formData = new FormData();
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let skystate = document.getElementById("id_skystate");
    let waterstate = document.getElementById("id_waterstate");

    formData.append("skystate", skystate.value);
    formData.append("waterstate", waterstate.value);
    clearResultDiv();
    displayLoader();
    await delay(20);

    let result = await ajaxRequest("search", formData, csrfToken);
    if (result["lures"].length > 0) {
        displayTableLure(columnLureList, result["lures"])
        displayTableColor(columnColorList, result["colors"])
    } else {
        displayNoResult(noResultClassList);
    };
    top3Submit.disabled = false;
})

function displayNoResult(noResultClassList) {
    let newDiv = createElement("div", noResultClassList)
    newDiv.innerHTML += "Aucun résultat"
    resultDiv.appendChild(newDiv);
}

function displayTableLure(columnList, lureList) {
    const table = createElement("table", tableClassList)
    const thead = createThead(columnList);
    const tbBody = createTrLure(lureList);
    table.append(thead, tbBody);
    resultDiv.appendChild(table);
}

function displayTableColor(columnList, colorlist) {
    const table = createElement("table", tableClassList)
    const thead = createThead(columnList);
    const tbBody = createTrColor(colorlist);
    table.append(thead, tbBody);
    resultDiv.appendChild(table);
}

function createTrLure(elementlist) {
    const tbody = createElement("tbody");
    elementlist.forEach(element => {
        const tr = createElement("tr");
        const th = createElement("th");
        const td = createElement("td");
        th.setAttribute("scope", "row");
        th.textContent = (elementlist.indexOf(element) + 1);
        td.textContent = element;
        tr.append(th, td);
        tbody.appendChild(tr);
    });
    return tbody
}

function createTrColor(elementlist) {
    const tbody = createElement("tbody");
    elementlist.forEach(element => {
        const tr = createElement("tr");
        const th = createElement("th");
        const td = createElement("td");
        const td2 = createElement("td");
        const img = createElement("img");
        img.setAttribute("src", "media/".concat(element[1]));
        img.setAttribute("alt", element[0]);
        th.setAttribute("scope", "row");
        th.textContent = (elementlist.indexOf(element) + 1);
        td.textContent = element[0];
        td2.appendChild(img);
        tr.append(th, td, td2);
        tbody.appendChild(tr);
    });
    return tbody
}

function createThead(thList) {
    const thClassList = ["text-primary"]
    const thead = createElement("thead");
    const tr = createElement("tr");
    thList.forEach(element => {
        const th = createElement("th", thClassList)
        th.setAttribute("scope", "col")
        th.textContent = element
        tr.appendChild(th)
    });
    thead.appendChild(tr)
    return thead
}

function createElement(type, classlist) {
    let newElement = document.createElement(type);
    if (classlist) {
        newElement.classList.add(...classlist);
        return newElement;
    } else {
        return newElement;
    }
}

function displayLoader() {
    const loader = document.querySelector(".loader");
    if (loader.classList.contains('d-none')) {
        loader.classList.replace("d-none", "d-flex")
        setTimeout(displayLoader, 2000)
    } else if (loader.classList.contains('d-flex')){
        loader.classList.replace("d-flex", "d-none")
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
            resultDiv.removeChild(resultDiv.firstChild)
        }
    }
}

// end search