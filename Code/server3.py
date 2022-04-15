# Chris McDonald - 20009360

import json
from socket import *
import _thread
import sys
import requests

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[1])
# serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')


def get_header(message, header):
    if message.find(header) > -1:
        value = message.split(header)[1].split()[0]
    else:
        value = None

    return value


def get_authentication(message, header):
    if message.split(header)[1].split()[1] == "MjAwMDkzNjA6MjAwMDkzNjA=":
        return True
    else:
        return False


def get_file(filename):
    try:
        f = open(filename, "rb")
        body = f.read()
        header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    except IOError:
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>404 Not Found wtf</h1></body></html>\r\n".encode()

    return header, body


def portfolio():
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = ("""<html lang='en' dir='ltr'>
  <head>
    <link rel='stylesheet' href='portfolio.css'>
    <title>My Portfolio</title>
  </head>
  <body onload="load()">
    <h1>Portfolio</h1>
    <br>
    <table id='table'>
      <tr>
        <td><p><b>Stock</b></p></td>
        <td><p><b>Quantity</b></p></td>
        <td><p><b>Price</b></p></td>
        <td><p><b>Gain/Loss</b></p></td>
      </tr>
    </table>
<script>
    function load() {
    get_json_data();
    get_symbol_data();
    }
    function get_json_data(){
        var json_url = 'portfolio.json';
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.responseText); // convert the response to a json object
                // append_json(data);// pass the json object to the append_json function
                append_json(data);
            }
        }
        xmlhttp.open('GET', json_url, true);
        xmlhttp.send(); // when the request completes it will execute the code in onreadystatechange section
        

    }
    function get_symbol_data() {
        var json_url2 = 
        'https://sandbox.iexapis.com/stable/ref-data/symbols?token=Tpk_eea527e37c7e40a4b0447069e490b4cf';
        xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var symbolData = (JSON.parse(this.responseText));
                append_symbols(symbolData);
            }
        }
        xmlhttp2.open('GET', json_url2, true);
        xmlhttp2.send();
    }
    
    function append_symbols(data) {
        var x = document.getElementById('stocksymbol');
        data.forEach(function(object) {
            if (object.type == 'cs') {
                var option = document.createElement('option');
                option.value = object.symbol;
                x.appendChild(option);
                }
            });
        }
    function display_json(object,gainloss){
        var table = document.getElementById('table');
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + object.STOCK + '</td>' +
        '<td>' + object.QUANTITY + '</td>' +
        '<td>' + object.PRICE + '</td>' +
        '<td>' + gainloss + '</td>';
        table.appendChild(tr);
        }
        
    function get_gainloss_data(object){
        var symbol = object.STOCK;
        var json_url3 = 
        "https://sandbox.iexapis.com/stable/stock/"+symbol+"/quote?token=Tpk_eea527e37c7e40a4b0447069e490b4cf";
        xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var gainLossData = (JSON.parse(this.responseText));
                var gainlosslatest = gainLossData.latestPrice;
                var gainlossint = parseFloat(gainlosslatest);
                var price = object.PRICE;
                var price = price.replace('$','')
                var priceint = parseInt(price);
                var gainloss = (gainlossint - priceint)/(priceint * 100);
                var gainloss2 = gainloss.toFixed(2);
                var gainlossfinal = gainloss2+'%';
                display_json(object,gainlossfinal);
            }
        }
        xmlhttp2.open('GET', json_url3, true);
        xmlhttp2.send();
    }

    function append_json(data){
        var table = document.getElementById('table');
        data.forEach(function(object) {
            get_gainloss_data(object)
        });
    }
</script>
    <br>
    <div>
    <form id='portfolio' method=post action="portfolio">
      <label for='symbols'>Stock Symbol: </label><br>
      <input list="stocksymbol" id="symbols" name="symbols" />
      <datalist id='stocksymbol' name='stocksymbol' required='required'></datalist><br><br>
      <label for='quantity'>Quantity: </label><br>
      <input type='number' name='quantity' id='quantity' required='required'><br><br>
      <label for='price'>Price: </label><br>
      <span class="currencyinput">$<input type="number" name="price" id="price"></span><br>
      </div>
      <input type='reset' name='reset' value='Reset' form='portfolio'>
      <input type='submit' name='submit' value='Update' form='portfolio'>
    </form>
  </body>
</html>
""").encode()

    return header, body


def research():
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = ("""<html lang='en' dir='ltr'>
  <head>
    <title>Research</title>
  </head>
  <body onload='load()'>
    <h1>Research</h1>
    <br>
    <form action='' id='stockform'>
        <p>Stock Symbol: <input list="stocksymbol" id="symbols" name="symbols" /></p>
    <datalist id='stocksymbol' name='stocksymbol' required='required'></datalist>
    </form>
    <p><button onclick='check()'>Check Stock</button></p>
    <span id="error"></span><br>        
    <table>
      <tr>
        <td>Symbol: </td>
        <td id='symbol'></td>
      </tr>
      <tr>
        <td>Company Name: </td>
        <td id='companyname'></td>
      </tr>
      <tr>
        <td>PE Ratio: </td>
        <td id='peratio'></td>
      </tr>
      <tr>
        <td>Market Capitalization: </td>
        <td id='marketcap'></td>
      </tr>
      <tr>
        <td>52 Week High: </td>
        <td id='52high'></td>
      </tr>
      <tr>
        <td>52 Week Low: </td>
        <td id='52low'></td>
      </tr>
    </table>
    <div id="chartContainer" style="height: 370px; width: 100%;"></div>
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js"> </script>  
    <script>
      function load(){
        get_symbol_data();
      }

      function get_symbol_data() {
        var json_url2 = 
        'https://sandbox.iexapis.com/stable/ref-data/symbols?token=Tpk_eea527e37c7e40a4b0447069e490b4cf';
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var symbolData = (JSON.parse(this.responseText));
                append_symbols(symbolData);
            }
        }
        xmlhttp.open('GET', json_url2, true);
        xmlhttp.send();
    }

    function append_symbols(data) {
        var x = document.getElementById('stocksymbol');
        data.forEach(function(object) {
            if (object.type == 'cs') {
                var option = document.createElement('option');
                option.value = object.symbol;
                x.appendChild(option);
                }
            });
        }
        
    function check() {
        var error = document.getElementById("error");
        var symbol = document.getElementById('symbols').value;
        var isempty = document.getElementById("symbols").value.length;
        var isempty = isempty.toString()
        if (isempty == 0)
        {
            error.textContent = "Please enter a stock symbol";
            error.style.color = "red";
        } else {
            get_json(symbol);
        }
    }
    
    function get_json(symbol){
        var json_url = 
        'https://sandbox.iexapis.com/stable/stock/'+symbol+'/stats?token=Tpk_eea527e37c7e40a4b0447069e490b4cf';
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.status == 404){
                var error = document.getElementById("error");
                error.textContent = "Please enter a valid stock symbol";
                error.style.color = "red";
                }
            else if (this.readyState == 4 && this.status == 200) {
                var symbolData = (JSON.parse(this.responseText));
                document.getElementById('symbol').innerHTML = symbol;
                document.getElementById('companyname').innerHTML = symbolData.companyName;
                document.getElementById('peratio').innerHTML = symbolData.peRatio;
                document.getElementById('marketcap').innerHTML = symbolData.marketcap;
                document.getElementById('52high').innerHTML = symbolData.week52high;
                document.getElementById('52low').innerHTML = symbolData.week52low;
                get_chart_data(symbol);
            }
        }
        xmlhttp.open('GET', json_url, true);
        xmlhttp.send();
    }
    
    function get_chart_data(symbol){
        var charturl = 
        'https://sandbox.iexapis.com/stable/stock/'+symbol+'/chart/5y?chartCloseOnly=true&token=Tpk_eea527e37c7e40a4b0447069e490b4cf';
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {//when a good response is given do this
                var chartData = (JSON.parse(this.responseText));
                console.log(chartData);
                var dataPoints = [];
                for (var i = 0; i < chartData.length; i++) {
		            dataPoints.push({
			            x: new Date(chartData[i].date),
			            y: chartData[i].close
		        });
		        }
                var chart = new CanvasJS.Chart("chartContainer", {
	            theme: "light1", // "light2", "dark1", "dark2"
	            animationEnabled: false, // change to true		
	            title:{
		            text: "Chart"
	            },
	            data: [
	            {
		            type: "line",
		            dataPoints: dataPoints
	            }
	            ]
                });
        chart.render();
        }
        }
        xmlhttp.open('GET', charturl, true);
        xmlhttp.send();
    }
    </script>
  </body>
</html>""").encode()

    return header, body


def update_portfolio(message):
    req = requests.get('https://sandbox.iexapis.com/stable/ref-data/symbols?token=Tpk_eea527e37c7e40a4b0447069e490b4cf')
    reqjson = req.json()
    symbollist = []
    for x in reqjson:
        if x['type'] == "cs":
            symbollist.append(x['symbol'])
    x = get_form_data(message)
    if x[0] == '=':
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = """<html><head></head><body>
        <h1>Error. Stock Symbol not selected</h1><button onclick="location.href='http://localhost:8080/portfolio'">
        Back</button></body></html>\r\n""".encode()
        return header, body
    if x[0][1:] not in symbollist:
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = """<html><head></head><body>
        <h1>Error. Invalid Stock Symbol entered</h1><button onclick="location.href='http://localhost:8080/portfolio'">
        Back</button></body></html>\r\n""".encode()
        return header, body
    if x[1].split('=')[1] == '0':
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = """<html><head></head><body>
        <h1>Error. Quantity cannot be zero</h1><button onclick="location.href='http://localhost:8080/portfolio'">
        Back</button></body></html>\r\n""".encode()
        return header, body
    if x[2].split('=')[1] == '' and x[1].split('=')[1][0] != '-':
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = """<html><head></head><body>
        <h1>Error. Price not entered</h1><button onclick="location.href='http://localhost:8080/portfolio'">
        Back</button></body></html>\r\n""".encode()
        return header, body
    symbol = x[0][1:]
    quantity = x[1].split('=')[1]
    if quantity[0] == '-':
        price = '0'
    else:
        price = x[2].split('=')[1]
        formdata = {"STOCK": symbol, "QUANTITY": quantity, "PRICE": "$"+price}
    url = "portfolio.json"
    with open(url, "r") as file:
        data = json.load(file)
    if data == []:
        if quantity[0] == '-':
            header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            body = """<html><head></head><body>
            <h1>Error. Must enter positive quantity for new stock</h1>
            <button onclick="location.href='http://localhost:8080/portfolio'">
            Back</button></body></html>\r\n""".encode()
            return header, body
        formdata = {"STOCK": symbol, "QUANTITY": quantity, "PRICE": "$"+price}
        data.append(formdata)
    else:
        duplicate = False
        symlist = []
        for obj in data:
            symlist.append(obj['STOCK'])
        for i in range(len(data)):
            quantitydup = data[i]['QUANTITY']
            pricedup = data[i]['PRICE'][1:]
            quantitydup = int(quantitydup)
            pricedup = float(pricedup)
            symboldup = False
            for x in symlist:
                if x == data[i]['STOCK']:
                    symboldup = True
            if symboldup is False and quantity[0] == '-':
                header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                body = """<html><head></head><body>
                <h1>Error. Must enter positive quantity for new stock</h1>
                <button onclick="location.href='http://localhost:8080/portfolio'">
                Back</button></body></html>\r\n""".encode()
                return header, body

            if data[i]['STOCK'] == symbol:
                duplicate = True
                if quantity[0] != '-':
                    quantityint = int(quantity)
                    newquantity = quantitydup+quantityint
                    price = int(price)
                    newprice = "{:.2f}".format(((quantitydup*pricedup)+(quantityint*price))/newquantity)
                    newprice = str(newprice)
                    data[i]['QUANTITY'] = newquantity
                    data[i]['PRICE'] = '$'+newprice
                else:
                    num = int(data[i]['QUANTITY'])
                    num2 = int(quantity[1:])
                    data[i]['QUANTITY'] = num-num2
                    if num2 > num:
                        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                        body = """<html><head></head><body>
                        <h1>Error. Short selling not allowed</h1>
                        <button onclick="location.href='http://localhost:8080/portfolio'">
                        Back</button></body></html>\r\n""".encode()
                        return header, body
            if data[i]['QUANTITY'] == 0:
                data.pop(i)
                break
        if duplicate is False:
            data.append(formdata)
    with open(url, "w") as file:
        json.dump(data, file)

    header, body = portfolio()

    return header, body


def get_form_data(message):
    header = "symbols"
    if message.find(header) > -1:
        x = message.split(header)[1].split('&')
    else:
        x = None
    return x


def authentication():

    header = "HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm='20009360 only'\r\n".encode()
    body = "<html><head><title>401 Unauthorized</title></head><body><h1>Unauthorized</h1></body></html>\r\n".encode()

    return header, body


def home():

    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = "<html><head><title>Welcome</title></head><body><h1>YOU MADE IT!</h1></body></html>\r\n".encode()

    return header, body


def login_fail():
    header = "HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm='20009360 only'\r\n".encode()
    body = "<html><head><title>401 Unauthorized</title></head><body><h1>Unauthorized</h1></body></html>\r\n".encode()

    return header, body


def process(connectionSocket):
    global responseHeader, responseBody
    message = connectionSocket.recv(1024).decode()
    print(message)
    if len(message) > 1:
        resource = message.split()[1][1:]
        print(resource)
        x = get_header(message, "Authorization:")
        if x is None or x == ":":
            responseHeader, responseBody = authentication()
        elif x == "Basic":
            entry = get_authentication(message, "Authorization:")
            if entry is False:
                responseHeader, responseBody = login_fail()
            if entry is True and resource == "portfolio":
                if message.split()[0] == 'GET':
                    responseHeader, responseBody = portfolio()
                elif message.split()[0] == 'POST':
                    responseHeader, responseBody = update_portfolio(message)
            elif entry is True and resource == 'research':
                if message.split()[0] == 'GET':
                    responseHeader, responseBody = research()
            else:
                responseHeader, responseBody = get_file(resource)

    connectionSocket.send(responseHeader)
    connectionSocket.send(responseBody)
    connectionSocket.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.settimeout(60)
    _thread.start_new_thread(process, (connectionSocket,))
