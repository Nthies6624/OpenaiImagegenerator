const imageForm = document.getElementById('image-form');
const imageContainer = document.getElementById('image-container');

imageForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const imageSize = imageForm.elements['image-size'].value;
    const bgColor = imageForm.elements['background-color'].value;
    const imageStyle = imageForm.elements['image-style'].value;

    const response = await fetch('/generate-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'image-size': imageSize,
            'background-color': bgColor,
            'image-style': imageStyle
        })
    });

    if (response.ok) {
        const imageUrl = await response.text();
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = 'Generated Image';
        imageContainer.innerHTML = '';
        imageContainer.appendChild(img);
    } else {
        console.error('Error generating image:', response);
    }
});

