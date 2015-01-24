window.onload = function() {
    document.getElementById("URL").tabIndex = "1";
};

// Grab the Url that the user queried
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {

  // Grab the URL and put it in the input
  var mm = tabs[0].url;

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
      var title1 = "";
      if (jsonObj.City != null && jsonObj.City != "") {
        title1 = jsonObj.City;
      }
      if (jsonObj.Subdivision != null && jsonObj.Subdivision != "") {
        if(title1 != "") {
          title1 += " / " + jsonObj.Subdivision;
        }
        else {
          title1 = jsonObj.Subdivision;
        }

      }
      var title2 = jsonObj.Country;
      var ip_addr = jsonObj['IP Address'];
      
      document.getElementById('title1').innerHTML = title1;
      document.getElementById('title2').innerHTML = title2;
      document.getElementById('ip_addr').innerHTML = ip_addr;

      var a = document.getElementById('mapit'); //or grab it by tagname etc
      a.href = "http://www.mapme.rocks/dest/" + ip_addr;

      document.getElementById('flag').innerHTML = '<img id="myImage" src="http://geotree.geonames.org/img/flags18/' + jsonObj['Country Code'] + '.png" />';

    }
  }

  xhr.send();



});

document.getElementById("URLSubmit").onclick = function(e){ 
  e.preventDefault();

  var ip_addr = document.getElementById('URL').value;
  chrome.tabs.create({ url: "http://www.mapme.rocks/dest/" + ip_addr });
};

document.getElementById("mapit").onclick = function(e){ 
  e.preventDefault();

  var ip_addr = document.getElementById('ip_addr').innerHTML;
  chrome.tabs.create({ url: "http://www.mapme.rocks/dest/" + ip_addr });
};

var warningCheckbox = document.getElementById("warning-checkbox")
warningCheckbox.addEventListener('change', function() {
  chrome.storage.local.set({
    warningListEnabled: warningCheckbox.checked
  }, function() {
  });
});
chrome.storage.local.get('warningListEnabled', function(data) {
  if(data && data.warningListEnabled) {
    warningCheckbox.checked = data.warningListEnabled;
  }
});


var blockCheckbox = document.getElementById("block-checkbox")
blockCheckbox.addEventListener('change', function() {
  chrome.storage.local.set({
    blockListEnabled: blockCheckbox.checked
  }, function() {
  });
});
chrome.storage.local.get('blockListEnabled', function(data) {
  if(data && data.blockListEnabled) {
    blockCheckbox.checked = data.blockListEnabled;
  }
});