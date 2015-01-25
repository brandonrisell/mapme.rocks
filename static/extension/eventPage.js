
// I need to register an event listener for page loads.
chrome.webNavigation.onCompleted.addListener(
  function(info) {

  	var parser = document.createElement('a');
  	parser.href = mm;

	var url = "http://www.mapme.rocks/geoip/" + parser.hostname;

	// Callback to Map Me to get the lookup informaion
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status==200) {
			var jsonObj = JSON.parse(xhr.responseText);
			alert(jsonObj["Country Code"]);
		}
	};
	xhr.open("GET", url, true);
	xhr.send();
    //alert(info.url);
    chrome.browserAction.setBadgeText({text:"BR"});
  });

// I'll then submit the url and grab the object and data

// I'll pull out the country code and put it in the badge

// The rest of the work will be handled by the popup