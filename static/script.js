document.addEventListener("DOMContentLoaded", function () {
    const dropdownButton = document.getElementById("breedDropdownButton");
    const dropdownMenu = document.getElementById("breedDropdown");
    const otherBreedInput = document.getElementById("otherBreedInput");

    // Toggle dropdown visibility
    dropdownButton.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation(); 
        dropdownMenu.classList.toggle("hidden");
    });

    // Select a breed from dropdown
    function selectBreed(breed) {
        dropdownButton.innerText = breed;
        dropdownMenu.classList.add("hidden");
        otherBreedInput.classList.add("hidden");
    }

    function showOtherInput() {
        dropdownButton.innerText = "Other";
        dropdownMenu.classList.add("hidden");
        otherBreedInput.classList.remove("hidden");
        otherBreedInput.value = "";
        otherBreedInput.placeholder = "Press Enter to insert a new breed";
        otherBreedInput.focus();
    }

    otherBreedInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && otherBreedInput.value.trim() !== "") {
            event.preventDefault();
            selectBreed(otherBreedInput.value.trim());
        }
    });

    document.addEventListener("click", function (event) {
        if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.add("hidden");
        }
    });

    window.selectBreed = selectBreed;
    window.showOtherInput = showOtherInput;
});

// Age & Weight Button Handling
document.addEventListener("DOMContentLoaded", function () {
    ["AgeButton", "WeightButton"].forEach(id => {
        const button = document.getElementById(id);
        const input = document.getElementById(id === "AgeButton" ? "ageInput" : "WeightInput");

        button.addEventListener("click", function () {
            input.classList.toggle("hidden");
            input.focus();
        });

        input.addEventListener("keypress", function (event) {
            if (event.key === "Enter" && input.value.trim() !== "") {
                event.preventDefault();
                button.innerText = input.value + (id === "AgeButton" ? " years" : " kg");
                input.classList.add("hidden");
            }
        });
    });
});

// Health Conditions Handling
document.addEventListener("DOMContentLoaded", function () {
    const healthDropdownButton = document.getElementById("healthDropdownButton");
    const healthDropdown = document.getElementById("healthDropdown");
    const healthCheckboxes = document.querySelectorAll(".health-checkbox");
    const selectedHealthConditions = document.getElementById("selectedHealthConditions");
    const healthConditionList = document.getElementById("healthConditionList");
    const otherHealthCheckbox = document.getElementById("otherHealthCheckbox");
    const otherHealthInput = document.getElementById("otherHealthInput");

    healthDropdownButton.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        healthDropdown.classList.toggle("hidden");
    });

    document.addEventListener("click", function (event) {
        if (!healthDropdown.contains(event.target) && event.target !== healthDropdownButton) {
            healthDropdown.classList.add("hidden");
        }
    });

    healthCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", updateSelectedConditions);
    });

    function updateSelectedConditions() {
        let selectedConditions = [];

        healthCheckboxes.forEach(checkbox => {
            if (checkbox.checked && checkbox !== otherHealthCheckbox) {
                selectedConditions.push(checkbox.value);
            }
        });

        if (otherHealthCheckbox.checked) {
            otherHealthInput.classList.remove("hidden");
            healthDropdown.classList.add("hidden");
            otherHealthInput.focus();
        } else {
            otherHealthInput.classList.add("hidden");
            otherHealthInput.value = "";
        }

        if (otherHealthCheckbox.checked && otherHealthInput.value.trim()) {
            selectedConditions.push(otherHealthInput.value.trim());
        }

        if (selectedConditions.length > 0) {
            selectedHealthConditions.classList.remove("hidden");
            healthConditionList.textContent = selectedConditions.join(", ");
        } else {
            selectedHealthConditions.classList.add("hidden");
        }
    }

    otherHealthInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            updateSelectedConditions();
            otherHealthInput.classList.add("hidden");
            otherHealthCheckbox.checked = false;
        }
    });
});

// File Upload Handling
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-upload");
    const fileNameDisplay = document.getElementById("file-name");

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Selected File: ${fileInput.files[0].name}`;
            fileNameDisplay.classList.remove("hidden");
        }
    });
});

// Form Submission
function CurrentDietAnalysis(event) {
    event.preventDefault();
    showLoader()
    
    const breed = document.getElementById("breedDropdownButton").innerText;
    const age = document.getElementById("AgeButton").innerText;
    const weight = document.getElementById("WeightButton").innerText;
    const health = document.getElementById("healthConditionList").textContent;
    const uploadedFile = document.getElementById("file-upload").files[0];

    if (!uploadedFile || !health || !weight || !age || !breed) {
        alert("Please fill out the necessary details.");
        hideLoader(); 
        return;
    }

    const formData = new FormData();
    formData.append("breed", breed);
    formData.append("age", age);
    formData.append("weight", weight);
    formData.append("health", health);
    formData.append("file", uploadedFile);

    fetch('/currentdiet', {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response_text").innerHTML = formatAIResponse(data.response);
    })
    .catch(error => console.error("Error:", error))
    .finally(() => hideLoader());
}

function formatAIResponse(responseText) {
    return responseText
        .replace(/<h1>/g, '<h1 class="text-2xl font-bold text-orange-700 mt-2">')
        .replace(/<h2>/g, '<h2 class="text-xl font-semibold text-orange-600 mt-2">')
        .replace(/<h3>/g, '<h3 class="text-lg font-medium text-orange-500 mt-2">')
        .replace(/<p>/g, '<p class="text-md text-orange-900 mt-1">');
}

// Form Submission
function PlanYourDiet(event) {
    event.preventDefault();
    showLoader();
    
    const breed = document.getElementById("breedDropdownButton").innerText;
    const age = document.getElementById("AgeButton").innerText;
    const weight = document.getElementById("WeightButton").innerText;
    const health = document.getElementById("healthConditionList").textContent;
    const uploadedFile = document.getElementById("file-upload").files[0];

    if (!uploadedFile || !health || !weight || !age || !breed) {
        alert("Please fill out the necessary details.");
        hideLoader();  
        return;
    }

    const formData = new FormData();
    formData.append("breed", breed);
    formData.append("age", age);
    formData.append("weight", weight);
    formData.append("health", health);
    formData.append("file", uploadedFile);

    fetch('/plandiet', {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response_text").innerHTML = formatAIResponse(data.response);
    })
    .catch(error => console.error("Error:", error))
    .finally(() => hideLoader());  
}


function showLoader() {
    document.getElementById("loading").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loading").classList.add("hidden");
}