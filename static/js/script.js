document.addEventListener('DOMContentLoaded', function () {
    const promptInput = document.getElementById('prompt');
    const generateBtn = document.getElementById('generateBtn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const generatedImage = document.getElementById('generatedImage');
    const errorDiv = document.getElementById('error');

    generateBtn.addEventListener('click', generateImage);

    async function generateImage(event) {
        event.preventDefault(); // prevent form reload

        const prompt = promptInput.value.trim();
        if (!prompt) {
            showError('⚠️ Please enter a prompt.');
            return;
        }

        // UI loading state
        loadingDiv.classList.remove('d-none');
        resultDiv.classList.add('d-none');
        errorDiv.classList.add('d-none');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/generate-image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate image.');
            }

            if (data.success && data.image_url) {
                generatedImage.src = data.image_url;
                resultDiv.classList.remove('d-none');
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            } else {
                throw new Error('No image was returned.');
            }
        } catch (err) {
            showError("❌ " + err.message);
        } finally {
            loadingDiv.classList.add('d-none');
            generateBtn.disabled = false;
        }
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }

    // UX: input field animation
    promptInput.addEventListener('focus', () => promptInput.classList.add('active'));
    promptInput.addEventListener('blur', () => {
        if (!promptInput.value) promptInput.classList.remove('active');
    });

    // Bootstrap tooltips (if used)
    if (typeof bootstrap !== 'undefined') {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
});

// 🔁 Reuse last prompt
function usePrompt(text) {
    document.getElementById('prompt').value = text;
    document.getElementById('prompt').focus();
}

// 🔁 Regenerate button
function regenerateImage() {
    document.getElementById('generateBtn').click();
}

// 💾 Download the generated image
function downloadImage() {
    const image = document.getElementById('generatedImage');
    fetch(image.src)
        .then(res => res.blob())
        .then(blob => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'generated.png';
            link.click();
            URL.revokeObjectURL(link.href);
        })
        .catch(err => {
            alert('❌ Failed to download image: ' + err.message);
        });
}
