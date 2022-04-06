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
const top3Submit = document.getElementById('top3-submit')

// requete ajax
async function ajaxRequest(url, data, csrftoken) {
    let requestData = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    let jsonData = await requestData.json()
    return jsonData
}

top3Submit.addEventListener('click', async function(e) {
    e.preventDefault();
    let formData = new FormData();
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let skystate = document.getElementById("id_skystate");
    let waterstate = document.getElementById("id_waterstate");
    

    formData.append("skystate", skystate.value);
    formData.append("waterstate", waterstate.value);

    let result = await ajaxRequest("search", formData, csrfToken);
    console.log(result["result"][0])
    console.log(result["result"][1])

})
// end search