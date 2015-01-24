

// Grab the Url that the user queried
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {

  // Grab the URL and put it in the input
  var mm = tabs[0].url;
  document.getElementById('userURL').value = mm;

  // Parse the whole Url and grab only the hostname
  var parser = document.createElement('a');
  parser.href = mm;

  // Get the Url ready for the callback
  var finalUrl = "http://www.mapme.rocks/geoip/" + parser.hostname;

  // Callback to Map Me to get the lookup informaion
  var xhr = new XMLHttpRequest();
  xhr.open("GET", finalUrl, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {

      var jsonObj = JSON.parse(xhr.responseText);
      var output = "City: " + jsonObj.City + "<br>";
      output += "Country: " + jsonObj.Country + "<br>";
      output += "IP Address: " + jsonObj["IP Address"] + "<br>";
      output += "Latitude: " + jsonObj.Latitude + "<br>";
      output += "Longitude: " + jsonObj.Longitude + "<br>";
      document.getElementById('div1').innerHTML = output;
    }
  }
  xhr.send();

});
