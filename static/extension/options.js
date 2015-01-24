var warninglist = document.getElementById('warning-list');
var blocklist =  document.getElementById('block-list');
var saveButton = document.getElementById('save');


saveButton.addEventListener('click', function() {
  chrome.storage.local.set({
    warninglist: warninglist.value,
    blocklist: blocklist.value
  }, function() {
    
  });
});


chrome.storage.local.get('warninglist', function(data) {
  if(data && data.warninglist) {
    warninglist.value = data.warninglist;
  }
});


chrome.storage.local.get('blocklist', function(data) {
  if(data && data.blocklist) {
    blocklist.value = data.blocklist;
  }
});


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