function sell_button () {
    var card_name = document.getElementsByClassName('card-title');

    fetch("http://127.0.0.1:8000/user/inventory/sellCard", {
        
        method:"POST",
        body: JSON.stringify({"card_name": card_name }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => {
        return response.text();
      })
      .then((html) => {
        document.body.innerHTML = html
      });
}