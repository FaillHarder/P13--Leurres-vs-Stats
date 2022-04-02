// navbar ActiveClass
let list = document.querySelectorAll('.list');

function setActiveClass() {
    list.forEach((item) =>
        item.classList.remove('active'));
    this.classList.add('active');
}
list.forEach((item) =>
        item.addEventListener('click', setActiveClass))
    // end navbar


// statistique by choice
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