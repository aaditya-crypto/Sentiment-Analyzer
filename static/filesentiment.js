function analyzeSentiment() {
    // const textInput = document.getElementById('inputText');
    const fileInput = document.getElementById('fileInput');
    const columnNameInput = document.getElementById('columnName');

    if (!fileInput.files.length) {
        alert('Please enter text or select a file to analyze.');
        return;
    }

    loader.style.display = 'block';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    // formData.append('text', textInput.value.trim());

    // Check if the file is CSV or Excel, then include the column_name
    if (fileInput.files[0] && (fileInput.files[0].name.endsWith('.csv') || fileInput.files[0].name.endsWith('.xls') || fileInput.files[0].name.endsWith('.xlsx'))) {
        const colName = columnNameInput.value.trim();
        if (!colName) {
            alert('Please enter the column name for CSV/Excel analysis.');
            return;
        }
        formData.append('column_name', colName);
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/predictsentimentfile', true);
    xhr.onload = function () {
        loader.style.display = 'none';

        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            displayResult(response);
        } else {
            alert('Error occurred. Please try again later.');
        }
    };
    xhr.send(formData);
}

function displayResult(response) {
    const modal = document.getElementById('myModal');
    const modalText = document.getElementById('modalText');
    const modalScore = document.getElementById('modalScore');
    const modalSentiment = document.getElementById('modalSentiment');
    const modalMessage = document.getElementById('modalMessage');

    modalText.textContent = response.FILE_TYPE === "CSV/EXCEL" ? "CSV/Excel Analysis" : "Word Analysis";
    modalScore.textContent = response.SENTIMENT_SCORE || "";
    modalSentiment.textContent = response.SENTIMENT_RESPONSE || "";
    modalMessage.innerHTML = "";

    if (response.FILE_TYPE === "CSV/EXCEL") {
        let dataTable = "<table>";
        dataTable += "<tr><th>Comment</th><th>Sentiment</th></tr>";

        response.data.forEach(row => {
            dataTable += `<tr><td>${row[0]}</td><td>${row[1]}</td></tr>`;
        });

        dataTable += "</table>";
        modalMessage.innerHTML = dataTable;
    } else if (response.FILE_TYPE === "WORD") {
        modalMessage.textContent = `Word Cloud: ${response.WORDCLOUD || ""}`;
    }

    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}
