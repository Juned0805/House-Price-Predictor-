document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.getElementById('loading-spinner');
    
    const resultContainer = document.getElementById('result-container');
    const predictedPrice = document.getElementById('predicted-price');
    const predictedPriceUsd = document.getElementById('predicted-price-usd');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable UI
        submitBtn.disabled = true;
        btnText.textContent = 'Calculating Evaluation...';
        spinner.classList.remove('d-none');
        resultContainer.classList.add('d-none');
        errorContainer.classList.add('d-none');
        resultContainer.classList.remove('fade-enter');

        // Gather form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Manual override for checkboxes (FormData omits them if unchecked)
        data.HasParking = document.getElementById('HasParking').checked ? 1 : 0;
        data.HasElevator = document.getElementById('HasElevator').checked ? 1 : 0;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success) {
                // Populate primary INR value
                predictedPrice.textContent = result.formatted_inr;
                
                // Populate secondary USD value
                predictedPriceUsd.textContent = result.formatted_usd;
                
                // Show result container
                resultContainer.classList.remove('d-none');
                
                // Trigger animation
                void resultContainer.offsetWidth; // Force reflow
                resultContainer.classList.add('fade-enter');
                
                // Scroll to result smoothly
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                throw new Error(result.error || 'Server error occurred during prediction.');
            }
        } catch (error) {
            errorMessage.textContent = error.message;
            errorContainer.classList.remove('d-none');
        } finally {
            // Restore UI
            submitBtn.disabled = false;
            btnText.textContent = 'Predict Market Value';
            spinner.classList.add('d-none');
        }
    });
});
