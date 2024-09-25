// scripts.js

let timer;
let isRunning = false;
let timeElapsed = 0;

function startTimer() {
    const startStopButton = document.getElementById('start-stop');
    
    if (!isRunning) {
        isRunning = true;
        startStopButton.textContent = "اتمام جلسه";
        startStopButton.classList.add('end-session');  // Add yellow color class
        
        timer = setInterval(() => {
            timeElapsed++;
            document.getElementById('timer').textContent = formatTime(timeElapsed);
        }, 1000);
    } else {
        clearInterval(timer);
        isRunning = false;
        startStopButton.textContent = "شروع جلسه";
        startStopButton.classList.remove('end-session');  // Revert back to green color
    }
}

function resetTimer() {
    clearInterval(timer);
    timeElapsed = 0;
    isRunning = false;
    document.getElementById('timer').textContent = formatTime(timeElapsed);
    document.getElementById('start-stop').textContent = "شروع جلسه";
    document.getElementById('start-stop').classList.remove('end-session'); // Revert to green
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function changeColor(button) {
    button.classList.toggle('active');
}
