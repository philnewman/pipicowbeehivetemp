var SS_TITLE = ""
var SHEETNAME = ""

function doGet(e) {

// Please fill in the link of your Google Sheet here!	
  var ss = SpreadsheetApp.openByUrl("");
  var cell = ss.getRange('A2');
  ss.setCurrentCell(cell);

  sheet = ss.getSheetByName(SHEETNAME);

  var datetime = e.parameter.datetime;
  var temperature = e.parameter.temperature;
  
  sheet.appendRow([datetime, temperature]);
}
