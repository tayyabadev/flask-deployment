document.addEventListener('DOMContentLoaded', () => {
    const getHintBtn = document.getElementById('getHintBtn');
    const calculatorIcon = document.getElementById('calculatorIcon');
    const mathKeyboard = document.getElementById('mathKeyboard');
    const display = document.getElementById('display');
    const submitProblemBtn = document.getElementById('submitProblem');
    const problemTypeSelect = document.getElementById('problemType');
    const problemInput = document.getElementById('problemInput');

    function toggleCalculator() {
        mathKeyboard.style.display = mathKeyboard.style.display === 'none' ? 'block' : 'none';
    }

    function appendToDisplay(value) {
        if (display.textContent === 'Enter a problem...') {
            display.textContent = value;
        } else {
            display.textContent += value;
        }
        problemInput.value = display.textContent;
    }

    function clearDisplay() {
        display.textContent = 'Enter a problem...';
        problemInput.value = '';
    }

    function handleSubmit() {
        const problem = problemInput.value.trim();
        if (problem) {
            localStorage.setItem('currentProblem', problem);
            localStorage.setItem('problemType', problemTypeSelect.value);
            window.location.href = '/output';
        }
    }

    calculatorIcon.addEventListener('click', toggleCalculator);

    document.querySelectorAll('.keyboard button').forEach(button => {
        button.addEventListener('click', () => {
            const value = button.textContent;
            if (value === '⌫') {
                display.textContent = display.textContent.slice(0, -1);
                if (display.textContent === '') {
                    clearDisplay();
                }
            } else if (value === 'C') {
                clearDisplay();
            } else {
                appendToDisplay(value);
            }
        });
    });

    submitProblemBtn.addEventListener('click', handleSubmit);
    getHintBtn.addEventListener('click', handleSubmit);

    problemInput.addEventListener('input', () => {
        display.textContent = problemInput.value;
    });
});

// Make toggleCalculator function global
window.toggleCalculator = function() {
    const mathKeyboard = document.getElementById('mathKeyboard');
    mathKeyboard.style.display = mathKeyboard.style.display === 'none' ? 'block' : 'none';
};