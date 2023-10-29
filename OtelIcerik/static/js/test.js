const apiTest = async () => {
    const request = await fetch('http://127.0.0.1:8000/api/v1/checkstatus')
    const response = await request.json()
    console.log("Test-data: ",response)
}

apiTest()