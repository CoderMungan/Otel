document.addEventListener('DOMContentLoaded', function () {
    const tarih = new Date().toISOString()

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        initialDate: tarih,
        themeSystem: 'standart',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth'
        },
        events: '/api/v1/checkstatus?format=json',
        eventColor: '#366BE5'
    });

    calendar.render();
});
