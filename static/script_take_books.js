elements = document.querySelectorAll("button");

elements.forEach(element => {
    element.addEventListener("click", (e) => {
        e.target.style.backgroundColor = "lightgray";
        elements.forEach(element => {
            if (element != e.target) {
                element.style.backgroundColor = "";
            }
        });

        fetch("http://127.0.0.1:5000/books", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ "category": e.target.innerHTML }) }).then(function (response) {
            return response.json();
        }).then(function (data) {
            if (document.getElementsByClassName("books").length == 1) {
                del_node = document.getElementsByClassName("books")[0];
                del_node.remove();
            }
            if (document.getElementsByClassName("not_avail").length == 1) {
                del_node = document.getElementsByClassName("not_avail")[0];
                del_node.remove()
            }
            if (document.getElementsByClassName("credentials").length==1) {
                del_node = document.getElementsByClassName("credentials")[0];
                del_node.remove()
            }
            if (data.length != 0) {
                let node = document.createElement("div");
                node.classList.add("books");
                html = "";
                data.forEach((element) => {
                    html += `<div class="book"><div class="name"><span>Book:</span>${element['Name']}</div><div class="author"><span>Author:</span>${element['Author']}</div><button class="take">Pick</button></div>`;
                });
                node.innerHTML = html;
                document.body.appendChild(node);
            }
            else {
                let node = document.createElement("div");
                node.classList.add("not_avail");
                node.innerHTML = `Books of this type are Not Available!`;
                document.body.appendChild(node);
            }
            takes = document.querySelectorAll(".take");
            takes.forEach(element => {
                element.addEventListener("click", (e) => {
                    
                    books = document.querySelectorAll(".book");
                    books.forEach(element => {
                        if (element != e.target.parentNode) {
                            element.remove();
                        }
                        element.getElementsByClassName('take')[0].remove();

                    });
                    let node = document.createElement("div");
                    console.log(document.getElementsByClassName("book")[0].getElementsByClassName("name")[0].innerText.slice(5,));
                    node.classList.add("credentials");
                    node.innerHTML = `    <p id="para">Credentials</p>
                    <form action="/issue" method="POST">
                    <div>
                        <label for="user">Username</label>
                        <input type="text" name="Username" id="user">
                    </div>
                    <div>
                        <label for="password">Password</label>
                        <input type="password" name="Password" id="password">
                        <input type="hidden" id="book" name="Book" value="${document.getElementsByClassName("book")[0].getElementsByClassName("name")[0].innerText.slice(5,)}">
                    </div>
                        <input type="submit" value="Issue" id="submit">
                    </form>`;
                    document.body.appendChild(node); 
                });
            });
        });
    });
});

