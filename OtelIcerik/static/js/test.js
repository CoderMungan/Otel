const apiTest = async () => {
    
    const request = await fetch('http://127.0.0.1:8000/api/v1/checkstatus')
    const response = await request.json()
    console.log("Gelen Data:",response)

    response.forEach(musteri => console.log("isimler", musteri.konuk))

}

apiTest()



