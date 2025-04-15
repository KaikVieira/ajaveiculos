function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');

    const dt = e.dataTransfer;
    const files = dt.files;

    addFilesToInput(files);
}

function previewFiles() {
    const preview = document.getElementById('file-preview');
    const files = document.getElementById('imagens').files;

    preview.innerHTML = '';
    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'preview-item';
            imgContainer.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <button type="button" onclick="removeImage(${index})">&times;</button>
            `;
            preview.appendChild(imgContainer);
        };
        reader.readAsDataURL(file);
    });
}


function addFilesToInput(newFiles) {
    const input = document.getElementById('imagens');
    let dataTransfer = new DataTransfer();

 
    Array.from(input.files).forEach(file => dataTransfer.items.add(file));


    Array.from(newFiles).forEach(file => dataTransfer.items.add(file));

    input.files = dataTransfer.files;
    previewFiles();
}

function removeImage(index) {
    const input = document.getElementById('imagens');
    let dataTransfer = new DataTransfer();

    Array.from(input.files).forEach((file, i) => {
        if (i !== index) dataTransfer.items.add(file);
    });

    input.files = dataTransfer.files;
    previewFiles();
}


function formatarNumero(input) {
    let valor = input.value;


    valor = valor.replace(/\D/g, '');


    valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    input.value = valor;
}
