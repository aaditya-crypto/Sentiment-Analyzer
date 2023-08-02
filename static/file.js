const uploadArea = document.querySelector('#uploadArea');
const dropZoon = document.querySelector('#dropZoon');
const loadingText = document.querySelector('#loadingText');
const fileInput = document.querySelector('#fileInput');
const previewImage = document.querySelector('#previewImage');
const fileDetails = document.querySelector('#fileDetails');
const uploadedFile = document.querySelector('#uploadedFile');
const uploadedFileInfo = document.querySelector('#uploadedFileInfo');
const uploadedFileName = document.querySelector('.uploaded-file__name');
const uploadedFileIconText = document.querySelector('.uploaded-file__icon-text');
const uploadedFileCounter = document.querySelector('.uploaded-file__counter');
const toolTipData = document.querySelector('.upload-area__tooltip-data');
const validFileTypes = [
  "image/jpeg",
  "image/png",
  "image/gif",
  "application/msword",
  "application/vnd.ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "text/csv",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // Corrected entry
];

const imagesTypes = [
  "doc",
  "xls",
  "xlsx",
  "csv"
];
toolTipData.innerHTML = [...imagesTypes].join(', .');
const docThumbnail = document.querySelector('#docThumbnail');
const excelThumbnail = document.querySelector('#excelThumbnail');

dropZoon.addEventListener('dragover', function (event) {
  event.preventDefault();
  dropZoon.classList.add('drop-zoon--over');
});

dropZoon.addEventListener('dragleave', function (event) {
  dropZoon.classList.remove('drop-zoon--over');
});

dropZoon.addEventListener('drop', function (event) {
  event.preventDefault();
  dropZoon.classList.remove('drop-zoon--over');

  const file = event.dataTransfer.files[0];
  uploadFile(file);
});

dropZoon.addEventListener('click', function (event) {
  fileInput.click();
});

fileInput.addEventListener('change', function (event) {
  const file = event.target.files[0];
  uploadFile(file);
});

function uploadFile(file) {
  const fileReader = new FileReader();
  const fileType = file.type;
  const fileSize = file.size;

  if (fileValidate(fileType, fileSize)) {
    dropZoon.classList.add('drop-zoon--Uploaded');
    loadingText.style.display = "block";
    previewImage.style.display = 'none';
    docThumbnail.style.display = 'none';
    excelThumbnail.style.display = 'none';

    uploadedFile.classList.remove('uploaded-file--open');
    uploadedFileInfo.classList.remove('uploaded-file__info--active');

    fileReader.addEventListener('load', function () {
      setTimeout(function () {
        uploadArea.classList.add('upload-area--open');
        loadingText.style.display = "none";
        if (fileType.startsWith('image/')) {
          previewImage.style.display = 'block';
          docThumbnail.style.display = 'none';
          excelThumbnail.style.display = 'none';
          previewImage.setAttribute('src', fileReader.result);
        } else if (fileType === 'application/msword' || fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
          docThumbnail.style.display = 'block';
          previewImage.style.display = 'none';
          excelThumbnail.style.display = 'none';
        } else if (fileType === 'application/vnd.ms-excel' || fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || fileType === 'text/csv') {
          excelThumbnail.style.display = 'block';
          previewImage.style.display = 'none';
          docThumbnail.style.display = 'none';
        }
        fileDetails.classList.add('file-details--open');
        uploadedFile.classList.add('uploaded-file--open');
        uploadedFileInfo.classList.add('uploaded-file__info--active');
      }, 500);
      previewImage.setAttribute('src', fileReader.result);
      uploadedFileName.innerHTML = file.name;
      progressMove();
    });

    fileReader.readAsDataURL(file);
  }
}

function progressMove() {
  let counter = 0;
  setTimeout(() => {
    let counterIncrease = setInterval(() => {
      if (counter === 100) {
        clearInterval(counterIncrease);
        document.getElementById('analyzeEmotionsBtn').style.display = 'block';
      } else {
        counter = counter + 10;
        uploadedFileCounter.innerHTML = `${counter}%`;
      }
    }, 100);
  }, 600);
}

function fileTypeValidation(fileType) {
  return validFileTypes.includes(fileType);
}

function fileValidate(fileType, fileSize) {
  if (fileTypeValidation(fileType)) {
    if (fileSize <= 2000000) {
      return true;
    } else {
      alert('Please make sure your file size is 2 Megabytes or less.');
      return false;
    }
  } else {
    alert('Please make sure to upload a valid file type (JPEG, PNG, GIF, DOC, XLS, XLSX, CSV).');
    return false;
  }
}

const analyzeButton = document.querySelector('#analyzeEmotionsBtn');
analyzeButton.addEventListener('click', function () {
  const uploadedFileData = fileInput.files[0];

  if (!uploadedFileData) {
    alert('Please select a file before analyzing.');
    return;
  }

  const fileExtension = uploadedFileData.name.split('.').pop().toLowerCase();
  let colName;
  if (['csv', 'xls', 'xlsx'].includes(fileExtension)) {
    colName = prompt('Please enter the column name for analysis:');
    if (!colName) {
      alert('Column name cannot be empty. Please enter a valid column name.');
      return;
    }
  }

  const formData = new FormData();
  formData.append('file', uploadedFileData);
  if (colName) {
    formData.append('column_name', colName);
  }

  fetch('/predictsentimentfile', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to analyze the file. Please try again.');
      }
      return response.json();
    })
    .then((data) => {
      console.log('API Response:', data);
      displaySentimentResult(data);
      modal.style.display = 'block';
    })
    .catch((error) => {
      alert('Error:', error.message);
    });
});

const modal = document.getElementById('modal');
const closeButton = document.querySelector('.close');
analyzeButton.addEventListener('click', () => {
  modal.style.display = 'block';
});

closeButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});

function displaySentimentResult(data) {
  const sentimentResult = document.getElementById('sentimentResult');
  if (data.FILE_TYPE === "CSV/EXCEL") {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th><strong>Category</strong></th>
        <th><strong>Count</strong></th>
      </tr>
      <tr>
        <td><strong>Total Comments</strong></td>
        <td>${data.TOTAL_COMMENTS}</td>
      </tr>
      <tr>
        <td><strong>Positive Comments</strong></td>
        <td>${data.POSITIVE_COMMENTS} (${data.SENTIMENT_SCORE.Positive}%)</td>
      </tr>
      <tr>
        <td><strong>Negative Comments</strong></td>
        <td>${data.NEGATIVE_COMMENTS} (${data.SENTIMENT_SCORE.Negative}%)</td>
      </tr>
      <tr>
        <td><strong>Neutral Comments</strong></td>
        <td>${data.NEUTRAL_COMMENTS} (${data.SENTIMENT_SCORE.Neutral}%)</td>
      </tr>
      <tr>
        <td><strong>Overall Sentiment</strong></td>
        <td>${data.SENTIMENT_RESPONSE}</td>
      </tr>
      <tr>
        <td><strong>Result Generated On</strong></td>
        <td>${data.SENTIMENT_DATETIME}</td>
      </tr>
    `;
    sentimentResult.innerHTML = '';
    sentimentResult.appendChild(table);
    // const downloadLink = document.createElement('a');
    // downloadLink.href = "?export=1";
    // downloadLink.textContent = "Download CSV";
    // downloadLink.setAttribute("download", "SentimentFile.csv");
    // sentimentResult.appendChild(downloadLink);
    
  } else if (data.FILE_TYPE === "WORD") {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>Category</th>
        <th>Value</th>
      </tr>
      <tr>
        <td><strong>Sentiment Score</strong></td>
        <td>${data.SENTIMENT_SCORE}</td>
      </tr>
      <tr>
        <td><strong>Overall Sentiment</strong></td>
        <td>${data.SENTIMENT_RESPONSE}</td>
      </tr>
      <tr>
        <td><strong>Result Generated On</strong></td>
        <td>${data.SENTIMENT_DATETIME}</td>
      </tr>
    `;
    sentimentResult.innerHTML = '';
    sentimentResult.appendChild(table);
  } else {
    sentimentResult.innerHTML = "Unsupported file format.";
  }
}

