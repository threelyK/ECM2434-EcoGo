

var myDiv = document.getElementById('typewriter');

function printStringByLetter(element) {
    var myString = myDiv.textContent || myDiv.innerText;
    element.innerHTML = '';
    var index = 0;
    var intervalId = setInterval(function() {
        myDiv.innerHTML += myString.charAt(index);
        index++;
        if(index == myString.length) {
            clearInterval(intervalId);
        }
    }, 30);
}