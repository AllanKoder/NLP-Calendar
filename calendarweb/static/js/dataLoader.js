//get the text value of the div with the id of calendar-data
if (typeof(Storage) !== "undefined") {
    const dataObject = document.getElementById("calendar-data");
    var calendarData = JSON.parse(document.getElementById("calendar-data").value);
    //if the calendarData is empty, set it to an empty array
    if (localStorage.getItem("calendarData") === null) {
        localStorage.setItem("calendarData", calendarData);
    }
    //if the calendarData is not empty, set it to the calendarData
    else {
        dataObject.value = localStorage.getItem("calendarData");
        localStorage.removeItem("calendarData");
        localStorage.setItem("calendarData", calendarData);
    }
} else {
// Sorry! No Web Storage support..
}
