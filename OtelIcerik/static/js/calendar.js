document.addEventListener("DOMContentLoaded", function () {
    const calendarContainer = document.getElementById("full-year-calendar");
    const prevMonthButton = document.getElementById("prevMonth");
    const nextMonthButton = document.getElementById("nextMonth");

    const days = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"];
    const months = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ];

    let currentYear = new Date().getFullYear();
    let currentMonth = new Date().getMonth();
    let currentDay = new Date().getDate();
    let currentView = "month";
    

    let checkStatusData = [];

    fetch('http://localhost:8000/api/v1/checkstatus?format=json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text();  
    })
    .then(text => {
        console.log("Raw response:", text);
        return JSON.parse(text); 
    })
    .then(data => {
        checkStatusData = data;
        displayView("month");  
    })
    .catch(error => console.error('Error fetching check status:', error));


    function displayView(viewType) {
        calendarContainer.innerHTML = ''; 
        currentView = viewType;
        switch(viewType) {
            case "month":
                createMonth(currentYear, currentMonth);
                break;
            case "week":
                createWeek(currentYear, currentMonth, currentDay);
                break;
            case "day":
                createDay(currentYear, currentMonth, currentDay);
                break;
            default:
                createMonth(currentYear, currentMonth);
        }
    }
    
    function createMonth(year, monthIndex) {
        calendarContainer.innerHTML = ''; 

        let date = new Date(year, monthIndex, 1);
        let daysInMonth = new Date(year, monthIndex + 1, 0).getDate();

        let monthDiv = document.createElement("div");
        monthDiv.className = "calendar-month";

        let monthTitle = document.createElement("h6");
        monthTitle.className = "text-center";
        monthTitle.innerText = `${months[monthIndex]} ${year}`;
        monthDiv.appendChild(monthTitle);

        let calendar = document.createElement("div");
        calendar.className = "calendar";

        let headerRow = document.createElement("div");
        headerRow.className = "row";
        days.forEach(day => {
            let dayCol = document.createElement("div");
            dayCol.className = "col";
            dayCol.innerText = day;
            headerRow.appendChild(dayCol);
        });
        calendar.appendChild(headerRow);

        let day = 1;
        while(day <= daysInMonth) {
            let weekRow = document.createElement("div");
            weekRow.className = "row";
            for(let i = 0; i < 7; i++) {
                let dayCol = document.createElement("div");
                dayCol.className = "col";
                if ((day === 1 && i === date.getDay()) || (day > 1 && day <= daysInMonth)) {
                    dayCol.innerText = day;
                    if (isDateInCheckStatusRange(new Date(year, monthIndex, day))) {
                        dayCol.style.backgroundColor = "red";
                    }
                    (function(currentDayValue) {
                    dayCol.addEventListener('click', function() {
                    currentDay = currentDayValue;
                    displayView("day");
                    });
                    })(day);
                    day++;
                }
                weekRow.appendChild(dayCol);
            }
            calendar.appendChild(weekRow);
        }
        monthDiv.appendChild(calendar);
        calendarContainer.appendChild(monthDiv);
    }
    function createWeek(year, monthIndex, day) {
        calendarContainer.innerHTML = ''; 
    
        let date = new Date(year, monthIndex, day);
        let startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - date.getDay());
    
        let weekDiv = document.createElement("div");
        weekDiv.className = "calendar-week";
    
        let endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6); 
    
        let weekTitle = document.createElement("h6");
        weekTitle.className = "text-center";
        weekTitle.innerText = `${months[startOfWeek.getMonth()]} ${startOfWeek.getDate()} - ${months[endOfWeek.getMonth()]} ${endOfWeek.getDate()} ${year}`;
        weekDiv.appendChild(weekTitle);
    
        let calendar = document.createElement("div");
        calendar.className = "calendar";
    
        let headerRow = document.createElement("div");
        headerRow.className = "row";
        days.forEach(day => {
            let dayCol = document.createElement("div");
            dayCol.className = "col";
            dayCol.innerText = day;
            headerRow.appendChild(dayCol);
        });
        calendar.appendChild(headerRow);
        let weekRow = document.createElement("div");
        weekRow.className = "row";
    
        for(let i = 0; i < 7; i++) {
            let dayCol = document.createElement("div");
            dayCol.className = "col";
            
            let clickableDay = startOfWeek.getDate();
            
            if (isDateInCheckStatusRange(new Date(year, monthIndex, clickableDay))) {
                dayCol.style.backgroundColor = "red";
            }
    
            dayCol.innerText = clickableDay;
            dayCol.addEventListener('click', function() {
                currentDay = clickableDay;
                displayView("day");
            });
            weekRow.appendChild(dayCol);
            startOfWeek.setDate(startOfWeek.getDate() + 1);
        }
        calendar.appendChild(weekRow);
        
        weekDiv.appendChild(calendar);
        calendarContainer.appendChild(weekDiv);
    }
    

    function createDay(year, monthIndex, day) {
        calendarContainer.innerHTML = ''; 

        let date = new Date(year, monthIndex, day);

        let dayDiv = document.createElement("div");
        dayDiv.className = "calendar-day";

        let dayTitle = document.createElement("h6");
        dayTitle.className = "text-center";
        dayTitle.innerText = `${days[date.getDay()]}, ${months[monthIndex]} ${day} ${year}`;
        dayDiv.appendChild(dayTitle);

        let calendar = document.createElement("div");
        calendar.className = "calendar";

        for(let hour = 0; hour < 24; hour++) {
        let row = document.createElement("div");
        row.className = "row";
        
        let hourCol = document.createElement("div");
        hourCol.className = "col";
        hourCol.innerText = (hour < 10 ? '0' + hour : hour) + ":00";
        row.appendChild(hourCol);
        let roomsForHour = getRoomsForDate(new Date(year, monthIndex, day, hour));
        if (isDateInCheckStatusRange(new Date(year, monthIndex, day, hour))) {
            hourCol.style.backgroundColor = "red";
        }
        let hourText = (hour < 10 ? '0' + hour : hour) + ":00";
        if(roomsForHour.length > 0){
            hourText += " - Rooms: ";
            roomsForHour.forEach(room => {
                let roomButton = document.createElement("button");
                roomButton.innerText = room;
                roomButton.className = "room-btn";
                hourCol.appendChild(roomButton);
            });
        } else {
            hourCol.innerText = hourText;
        }
        calendar.appendChild(row);
        }
        dayDiv.appendChild(calendar);
        calendarContainer.appendChild(dayDiv);
    }

    function isDateInCheckStatusRange(date) {
        for (let status of checkStatusData) {
            let checkInDate = new Date(status.checkIn);
            let checkOutDate = new Date(status.checkOut);
            
            if (date >= checkInDate && date <= checkOutDate) {
                return true;
            }
        }
        return false;
    }

    function getRoomsForDate(date) {
        let rooms = [];
        for (let status of checkStatusData) {
            let checkInDate = new Date(status.checkIn);
            let checkOutDate = new Date(status.checkOut);
            
            if (date >= checkInDate && date <= checkOutDate) {
                rooms.push(status.oda);  
            }
        }
        return rooms;
    }
    

    prevMonthButton.addEventListener('click', function() {
    if (currentView === "month") {
        currentMonth--;
        if(currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        createMonth(currentYear, currentMonth);
    } else if (currentView === "week") {
        currentDay -= 7;  
        if (currentDay <= 0) {
            currentMonth--;
            if(currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            let daysInPrevMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
            currentDay += daysInPrevMonth;  
        }
        createWeek(currentYear, currentMonth, currentDay);
    }
    else if (currentView === "day") {
        currentDay--;  
        if (currentDay <= 0) {
            currentMonth--;
            if(currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            let daysInPrevMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
            currentDay = daysInPrevMonth; 
        }
        createDay(currentYear, currentMonth, currentDay);
    }
});

    nextMonthButton.addEventListener('click', function() {
    if (currentView === "month") {
        currentMonth++;
        if(currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        createMonth(currentYear, currentMonth);
    } else if (currentView === "week") {
        currentDay += 7;  
        let daysInCurrentMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        if (currentDay > daysInCurrentMonth) {
            currentDay -= daysInCurrentMonth; 
            currentMonth++;
            if(currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
        }
        createWeek(currentYear, currentMonth, currentDay);
    } 
    else if (currentView === "day") {
        currentDay++;  
        let daysInCurrentMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        if (currentDay > daysInCurrentMonth) {
            currentDay = 1; 
            currentMonth++;
            if(currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
        }
        createDay(currentYear, currentMonth, currentDay);
    }
});

    document.getElementById("viewMonth").addEventListener('click', function() {
        displayView("month");
    });

    document.getElementById("viewWeek").addEventListener('click', function() {
        displayView("week");
    });

    document.getElementById("viewDay").addEventListener('click', function() {
        displayView("day");
    });

    displayView("month");
});
