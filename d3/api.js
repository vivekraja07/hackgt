

dept = {
  0 : 'All Orders',
  1 : 'Frozen',
  2 : 'Health',
  3 : 'Grains',
  4 : 'Fruits & Veggies',
  5 : 'Alcohol',
  6 : 'Foreign',
  7 : 'Beverages',
  8 : 'Pet Food',
  9 : 'Pasta & Rice',
  10: 'Fruits & Veggies',
  11: 'Toiletries',
  12: 'Meats',
  13: 'Condiments',
  14: 'Breakfast',
  15: 'Canned Foods',
  16: 'Dairy',
  17: 'Cleaning Supplies',
  18: 'Baby Food',
  19: 'Snacks',
  20: 'Deli',
  21: 'Misc'
}

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

function makeCORSRequest(url,city) {
    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        alert('CORS not supported');
        return;
    }
    xhr.onload = function() {
        var text = xhr.responseText;
        json = JSON.parse(text);
        
        var total_trans = json['All Orders']['Transactions'];
        var total_rev = json['All Orders']['Revenue'];
        var x = 0;
        var data = [
            {label: 'Frozen',               value: json['Frozen']['Transactions']/total_trans},
            {label: 'Health',               value: json['Health']['Transactions']/total_trans},
            {label: 'Grains',               value: json['Grains']['Transactions']/total_trans},
            {label: 'Fruits & Veggies',     value: json['Fruits & Veggies']['Transactions']/total_trans},
            {label: 'Alcohol',              value: json['Alcohol']['Transactions']/total_trans},
            {label: 'Foreign',              value: json['Foreign']['Transactions']/total_trans},
            {label: 'Beverages',            value: json['Beverages']['Transactions']/total_trans},
            {label: 'Pet Food',             value: json['Pet Food']['Transactions']/total_trans},
            {label: 'Pasta & Rice',         value: json['Pasta & Rice']['Transactions']/total_trans},
            {label: 'Toiletries',           value: json['Toiletries']['Transactions']/total_trans},
            {label: 'Meats',                value: json['Meats']['Transactions']/total_trans},
            {label: 'Condiments',           value: json['Condiments']['Transactions']/total_trans},
            {label: 'Breakfast',            value: json['Breakfast']['Transactions']/total_trans},
            {label: 'Canned Foods',         value: json['Canned Foods']['Transactions']/total_trans},
            {label: 'Dairy',                value: json['Dairy']['Transactions']/total_trans},
            {label: 'Cleaning Supplies',    value: json['Cleaning Supplies']['Transactions']/total_trans},
            {label: 'Baby Food',            value: json['Baby Food']['Transactions']/total_trans},
            {label: 'Snacks',               value: json['Snacks']['Transactions']/total_trans},
            {label: 'Deli',                 value: json['Deli']['Transactions']/total_trans}
        ];
        var info = [city,total_trans,total_rev];
        infoString = JSON.stringify(info)
        dataString = JSON.stringify(data)
        console.log("info = " + infoString)
        console.log("data = " + dataString)
        
        change(data,info);
    };
    xhr.onerror = function() {
        alert('Error making the request.');
    };
    xhr.send();
}


function makeCORSRequestDept(url) {
   console.log(url);
    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        alert('CORS not supported');
        return;
    }
    xhr.onload = function() {
        var text = xhr.responseText;
        // console.log(text);
        json = JSON.parse(text);
        console.log(json);
    };
    xhr.onerror = function() {
        alert('Error making the request.');
    };
    xhr.send();
}


function getDeptInfo(city,dept) {
  makeCORSRequestDept("http://localhost:5000/city/"+city+"/dept/"+dept);
}

function getCity(city,city_name) {
    console.log(city)
    makeCORSRequest("http://localhost:5000/city/" + city,city_name);
}

function getTotal(city) {
    makeCORSRequest("http://localhost:5000/totals","All Orders");
}


