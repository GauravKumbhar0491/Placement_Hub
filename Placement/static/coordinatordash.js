function sendData() {
    const formData = new FormData(document.getElementById("delete-job-offer"));
    const url = "http://localhost:5000/coordinatordash";

    console.log(Object.fromEntries(formData))
    fetch(url, {
        method: "DELETE", // Change the method according to your API
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(
        response => {
            if (response.headers.get('Location'))
                window.location.href = response.url
            else
                console.log(response.json())
        }
    )
    .catch(error => {
    console.error('Error:', error);
    });
}
