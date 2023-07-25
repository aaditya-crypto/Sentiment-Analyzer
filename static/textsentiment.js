function analyzeSentiment() {
    const text = document.getElementById('inputText').value;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/predictsentimenttext', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            showModal(response);
        } else {
            alert('Error occurred. Please try again later.');
        }
    };
    xhr.send(`text=${encodeURIComponent(text)}`);
}

function showModal(response) {
    const modal = document.getElementById('myModal');
    const modalText = document.getElementById('modalText');
    const modalScore = document.getElementById('modalScore');
    const modalSentiment = document.getElementById('modalSentiment');
    const modalMessage = document.getElementById('modalMessage');

    modalText.textContent = response.Text;
    modalScore.textContent = response.Score;
    modalSentiment.textContent = response.Sentiment;
    modalMessage.textContent = response.message;

    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}