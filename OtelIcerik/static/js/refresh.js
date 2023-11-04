// CheckOut Status
let deneme;

const checkStatusApi = async () => {
    const request = await fetch('http://127.0.0.1:8000/api/v1/checkstatus')
    const response = await request.json()
    if(JSON.stringify(response) !== JSON.stringify(deneme) && deneme !== undefined){
        window.location.reload()
    }
    deneme = response
}

setInterval(checkStatusApi, 60000)