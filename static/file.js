
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
    "application/msword",  // doc
    "application/vnd.ms-excel", // xls
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // xlsx
    "text/csv", // csv
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // docx
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
          } else if (fileType === 'application/vnd.ms-excel' || fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
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
