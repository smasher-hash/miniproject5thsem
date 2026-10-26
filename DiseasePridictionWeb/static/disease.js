// const imageInput = document.getElementById("imageInput");
// const imagePreview = document.getElementById("imagePreview");
// const previewContainer = document.getElementById("previewContainer");

// imageInput.addEventListener("change", function () {

//     const file = this.files[0];

//     if (!file) {
//         previewContainer.style.display = "none";
//         return;
//     }

//     const allowedTypes = [
//         "image/jpeg",
//         "image/jpg",
//         "image/png"
//     ];

//     if (!allowedTypes.includes(file.type)) {

//         alert("Please select a JPG, JPEG or PNG image.");

//         imageInput.value = "";

//         previewContainer.style.display = "none";

//         return;
//     }

//     const imageURL = URL.createObjectURL(file);

//     imagePreview.src = imageURL;

//     previewContainer.style.display = "block";
// });


// const form = document.getElementById("predictionForm");

// form.addEventListener("submit", function () {

//     const button = document.getElementById("detectBtn");

//     button.innerHTML = "🔄 Detecting...";

//     button.disabled = true;

// });


const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");
const fileName = document.getElementById("fileName");


// ==============================
// IMAGE PREVIEW
// ==============================

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {

        previewContainer.style.display = "none";

        return;
    }


    // Allowed file types

    const allowedTypes = [
        "image/jpeg",
        "image/png"
    ];


    if (!allowedTypes.includes(file.type)) {

        alert("Please select a JPG, JPEG or PNG image.");

        imageInput.value = "";

        previewContainer.style.display = "none";

        return;
    }


    // Create preview

    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;

    fileName.textContent = file.name;

    previewContainer.style.display = "block";

});


// ==============================
// FORM SUBMISSION
// ==============================

const form = document.getElementById("predictionForm");

form.addEventListener("submit", function () {

    const button = document.getElementById("detectBtn");

    button.innerHTML = "🔄 Analyzing Leaf...";

    button.disabled = true;

});


// ==============================
// CHECK ANOTHER IMAGE
// ==============================

function resetDetection() {

    window.location.href = "/";

}