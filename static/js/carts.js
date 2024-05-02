console.log("Hello")

var updateBtns = document.getElementsByClassName("update-cart")

for (let index = 0; index < updateBtns.length; index++) {
    updateBtns[index].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("Id ", productId, "action", action);
        
        console.log("User :", user);
    })
}