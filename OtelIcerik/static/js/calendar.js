document.addEventListener('DOMContentLoaded', function () {
    const tarih = new Date().toISOString()

    const randomHexColor = () => {
        const red = Math.floor(Math.random() * 256)
        const blue = Math.floor(Math.random() * 256)
        const green = Math.floor(Math.random() * 256)

        return `#${red.toString(16)}${green.toString(16)}${blue.toString(16)}`;
    }

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'tr',
        initialView: 'dayGridMonth',
        initialDate: tarih,
        themeSystem: 'standart',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth'
        },
        events: '/api/v1/checkstatus?format=json',
    });

    calendar.render();
});
