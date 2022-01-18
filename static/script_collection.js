return_book=document.querySelectorAll(".return");

return_book.forEach(element => {
    element.addEventListener("click",(e)=>{
        console.log("Hello");
        fetch("http://127.0.0.1:5000/return", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ "returned_book": e.target.parentNode.getElementsByClassName("name")[0].innerText.slice(5,),"username":document.getElementById("username").innerText})}).then(function (response) {
            return response.json();
        }).then(function (data) {
            e.target.parentNode.remove();
            if(document.getElementsByClassName('book')[0]==null){
                document.getElementById("head").remove();
                document.body.innerHTML+=`<div class="para">You have not taken any book from library!</div>`;
            }
            alert("You have successfully returned the book!");
        });
    });
});