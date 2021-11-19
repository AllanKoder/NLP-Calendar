const date = new Date();

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

    date.setDate(1);

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    const firstDay = date.getDay();
    const nextDays = 7 - lastDayIndex - 1;
    console.log(nextDays);
    const year = date.getFullYear();
    const month = date.getMonth();
    const day = date.getDate();     

    const monthDays = document.querySelector('.days');
    
    document.querySelector('.calendar-header h1').innerHTML = `${months[month]}`;
    document.querySelector('.calendar-header p').innerHTML = new Date().toDateString();
    console.log(`${year}-${month+1}-${day}`); 
    
    let days = ""
    
    const maxDays = 37;

    for (let i = firstDay; i > 1; i--) {
        days += `<div class="date-content"><div class = "prev-date">${prevLastDay - i}</div></div>`;
    }
    for (let i = 1; i <= lastDay; i++) {
        if(firstDay + i < maxDays) {
        days += `<div class="date-content"><div>${i}</div></div>`;
        }
    }
    for (let i = 1; i <= nextDays; i++) {
        if(firstDay + lastDay + i < maxDays) {
            days += `<div class="date-content"><div class = "next-date">${i}</div></div>`;
        }
    }
    monthDays.innerHTML = days;
    
}

document.querySelector(".prev").addEventListener("click", function(){
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

document.querySelector(".next").addEventListener("click", function(){
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

renderCalendar();