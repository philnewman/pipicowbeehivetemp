var SS_TITLE = ""
var SHEETNAME = ""

function doGet(e) {

// Please fill in the link of your Google Sheet here!	
  var ss = SpreadsheetApp.openByUrl("");
  var cell = ss.getRange('A2');
  ss.setCurrentCell(cell);

  sheet = ss.getSheetByName(SHEETNAME);

  var date = e.parameter.datetime;
  var time = e.parameter.time;
  var tempF = e.parameter.tempF
  var tempC = e.parameter.tempC
  
  sheet.appendRow([date, time, tempF, tempC]);
}
