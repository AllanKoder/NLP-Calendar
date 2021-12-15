const date = new Date();
const dateToday = new Date();

var cookieName = "index";
var index = 0;

let indexTab = getCookie(cookieName);
if (indexTab != "") {
    index = parseInt(document.cookie.substring(cookieName.length+1));
}

function getCookie(cookiename) {
    let name = cookiename + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');

    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

const renderCalendar = () => {
    const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ];
    
    const dayofweek = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
    ];

    date.setMonth(dateToday.getMonth() + index);
    date.setFullYear(dateToday.getFullYear() + Math.floor((dateToday.getMonth() + index) / 12));
    date.setDate(1);

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    const firstDay = date.getDay();
    const nextDays = 7 - lastDayIndex - 1;
    const year = date.getFullYear();
    console.log(year);
    const month = date.getMonth();
    const day = date.getDate();     

    const monthDays = document.querySelector('.days');
    
    document.querySelector('.calendar-header h1').innerHTML = `${months[date.getMonth()]} ${date.getFullYear()}`;
    document.querySelector('.calendar-header p').innerHTML = dateToday.toDateString();
    
    let days = "";
    
    const maxDays = 37;

    for (let i = firstDay; i > 1; i--) {
        var cday  = prevLastDay - i;
        var cmonth = date.getMonth() - 1;
        var cyear = date.getFullYear();
        if(cmonth <= -1)
        {
            cyear--;
            cmonth = 11;
        }

        days += `
        <div class="date-content">
        <form method="POST">
            <input class = "calendar-button-value" type = "text" name = "date" value = "${cmonth}-${cday}-${cyear}"> 
            <input class = "prev-date" type = "submit" value ="${cday}" name = "calendarButton-${prevLastDay - i}" class = "date-content">
        </form>                 
        </div>`;
    }

    for (let i = 1; i <= lastDay; i++) {
        if(firstDay + i < maxDays) {
        var cday = i;
        var cmonth = date.getMonth();
        var cyear = date.getFullYear();
        days += `
        <div class="date-content">
        <form method="POST" class = "calendar-form">
            <input class = "calendar-button-value" type = "text" name = "date" value = "${cmonth}-${cday}-${cyear}">
            <input type = "submit" value ="${cday}" name = "calendarButton-${i}" class = "date-content"></input>
        </form>                 
        </div>`;
        }
    }
    for (let i = 1; i <= nextDays; i++) {
        if(firstDay + lastDay + i < maxDays) {
            var cday = i;
            var cmonth = date.getMonth() + 1;
            var cyear = date.getFullYear();
            if(cmonth >= 12)
            {
                cyear++;
                cmonth = 0;
            }
            
            days += `
            <div class="date-content">
            <form method="POST">
                <input class = "calendar-button-value" type = "text" name = "date" value = "${cmonth}-${cday}-${cyear}"> 
                <input class = "next-date" type = "submit" value ="${cday}" name = "calendarButton-${i}">
            </form>
            </div>`;
        }
    }
    monthDays.innerHTML = days;
    
}

document.querySelector(".prev").addEventListener("click", function(){
    index -= 1;
    refreshPageSaveCookies();
});

document.querySelector(".next").addEventListener("click", function(){
    index += 1;
    refreshPageSaveCookies();
});

const refreshPageSaveCookies= () => {
    console.log(index);
    document.cookie = `index=${index};`;
    renderCalendar();
}
renderCalendar();