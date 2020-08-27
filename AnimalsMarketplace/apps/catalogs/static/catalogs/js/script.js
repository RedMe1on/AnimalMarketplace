// Add rating
const rating = document.querySelector('form[name=add-rating]')

rating.addEventListener("change", function (e) {
    // Get data from form
    let data = new FormData(this);
    console.log(data)
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
});
