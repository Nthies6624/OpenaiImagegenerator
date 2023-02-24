const form = document.getElementById('image-form');
const imageContainer = document.getElementById('image-container');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const imageSize = form.elements['image-size'].value;
    const bgColor = form.elements['background-color'].value;
    const imageStyle = form.elements['image-style'].value;

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
        imageContainer.innerHTML = `<img src="${imageUrl}" alt="Generated Image">`;
    } else {
        console.error('Error generating image:', response);
    }
});
