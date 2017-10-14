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

function makeCORSRequest(url) {
    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        alert('CORS not supported');
        return;
    }
    xhr.onload = function() {
        var text = xhr.responseText;
        json = JSON.parse(text);
        var total = json['All Orders']['Transactions'];
        var x = 0;
        var data = [
            {label: 'Frozen',               value: json['Frozen']['Transactions']/total},
            {label: 'Health',               value: json['Health']['Transactions']/total},
            {label: 'Grains',               value: json['Grains']['Transactions']/total},
            {label: 'Fruits & Veggies',     value: json['Fruits & Veggies']['Transactions']/total},
            {label: 'Alcohol',              value: json['Alcohol']['Transactions']/total},
            {label: 'Foreign',              value: json['Foreign']['Transactions']/total},
            {label: 'Beverages',            value: json['Beverages']['Transactions']/total},
            {label: 'Pet Food',             value: json['Pet Food']['Transactions']/total},
            {label: 'Pasta & Rice',         value: json['Pasta & Rice']['Transactions']/total},
            {label: 'Toiletries',           value: json['Toiletries']['Transactions']/total},
            {label: 'Meats',                value: json['Meats']['Transactions']/total},
            {label: 'Condiments',           value: json['Condiments']['Transactions']/total},
            {label: 'Breakfast',            value: json['Breakfast']['Transactions']/total},
            {label: 'Canned Foods',         value: json['Canned Foods']['Transactions']/total},
            {label: 'Dairy',                value: json['Dairy']['Transactions']/total},
            {label: 'Cleaning Supplies',    value: json['Cleaning Supplies']['Transactions']/total},
            {label: 'Baby Food',            value: json['Baby Food']['Transactions']/total},
            {label: 'Snacks',               value: json['Snacks']['Transactions']/total},
            {label: 'Deli',                 value: json['Deli']['Transactions']/total}
        ];
        change(data);
    };
    xhr.onerror = function() {
        alert('Error making the request.');
    };
    xhr.send();
}

function getCity(city) {
    makeCORSRequest("http://localhost:5000/city/" + city);
}

function getTotal(city) {
    makeCORSRequest("http://localhost:5000/totals");
}

