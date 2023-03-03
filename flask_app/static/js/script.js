const bookForm = document.querySelector("#searchForm")

bookForm.addEventListener("submit", function(e) {
    e.preventDefault();
    let bookTitle = document.querySelector("#bookTitle").value
        fetchBook(bookTitle);
    this.reset();
})

function fetchBook (info) {
    fetch (`https://openlibrary.org/search.json?q=${info}`)
    .then(resp => resp.json())
    .then(data => {
        console.log("I am running 2nd")
        console.log( data )

        // let title = data.docs[0].title
        // let titleDiv = document.querySelector("#title")
        // titleDiv.innerHTML = title;

        let loopUl = document.querySelector("#bookName")
        loopUl.innerHTML = "";
        for (const item of data.docs) {
            let listElement = document.createElement("li")
            let listElement1 = document.createElement("p")
            let bookName = item.title
            let authorName = item.author_name
            listElement.textContent = bookName
            listElement1.textContent = authorName
            loopUl.appendChild(listElement)
        }
    })
}