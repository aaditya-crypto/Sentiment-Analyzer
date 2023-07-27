    const inputTextElement = document.getElementById('inputText');
    const analyzeButton = document.querySelector('button');
    const modalLoader = document.getElementById('modalLoader'); // Get the loader element
    const modalResult = document.getElementById('modalResult'); // Get the modal result element

    function updateCharCount() {
        const charCountElement = document.getElementById('charCount');
        const charCount = inputTextElement.value.length;
        charCountElement.textContent = `Characters: ${charCount}/500`;
    }

    function analyzeSentiment() {
        const text = document.getElementById('inputText').value;

        // Show the loader and hide the modal result before making the API call
        modalLoader.style.display = 'block';
        modalResult.style.display = 'none';

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/predictsentimenttext', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            // Hide the loader and display the modal result once the API call is complete
            modalLoader.style.display = 'none';
            modalResult.style.display = 'block';

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
        // Get the modal element by its ID
        const modal = document.getElementById('myModal');

        // Clear existing contents in the modal before updating
        const modalText1 = document.getElementById('modalText1');
        const modalText = document.getElementById('modalText');
        const modalScore = document.getElementById('modalScore');
        const modalSentiment = document.getElementById('modalSentiment');
        const modalTime = document.getElementById('modalTime');

        modalText1.textContent = response.yourtext;
        modalText.textContent = response.Text;
        modalScore.textContent = response.Score;
        modalTime.textContent = response.Result_date_time;

        // Set Sentiment Response value
        const sentimentResponse = response.Sentiment;
        modalSentiment.textContent = sentimentResponse;
        modalSentiment.classList.add(sentimentResponse); // Add appropriate class for styling

        // Show the modal
        modal.style.display = 'block';
    }

    function closeModal() {
        const modal = document.getElementById('myModal');
        modal.style.display = 'none';
    }

    updateCharCount();
    inputTextElement.addEventListener('input', updateCharCount);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   