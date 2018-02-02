function callAPI() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/bestPrice/MMM/Put", true);
        xhr.send();
        console.log("asdf"+xhr.responseText)
        $('h5').text(xhr.responseText);
    }