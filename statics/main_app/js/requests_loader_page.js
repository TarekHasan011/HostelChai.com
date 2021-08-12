radio = document.getElementsByName('customRadio');

for (let i=0; i<radio.length; i++){
    radio[i].addEventListener('change', function () {
        console.log(radio[i].value)
    });
}
