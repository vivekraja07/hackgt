function createCORSRequest(method, url) {
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
        xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined") {
        xhr = new XDomainRequest();
        xhr.open(method, url);
    } else {
        xhr = null;
    }
    return xhr;
}

function makeCORSRequest(url) {
    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        alert('CORS not supported');
        return;
    }
    xhr.onload = function() {
        var text = xhr.responseText;
        alert('Response from CORS request to ' + url + ': ' + text);
    };
    xhr.onerror = function() {
        alert('Error making the request.');
    };
    xhr.send();
}

function getCity(city) {
    makeCORSRequest("http://localhost:5000/city/" + city)
}

getCity("NewYork");