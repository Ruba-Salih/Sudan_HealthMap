// Function to change button styles dynamically
function changeButtonColor(color, hoverColor, textColor) {
    document.documentElement.style.setProperty('--button-color', color);
    document.documentElement.style.setProperty('--button-hover-color', hoverColor);
    document.documentElement.style.setProperty('--button-text-color', textColor);
}

// Example: Change buttons to green
// Call this function dynamically as needed
// changeButtonColor('#28a745', '#218838', 'white');
