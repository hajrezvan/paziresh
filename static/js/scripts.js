let timer;
let iRunning = false;
let timeElapsed = 0;
let buttonTimers = {};  // Store the timer start time for each button
let greenTimes = {};  // Store the total green time for each button

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

        // Start timing for any buttons that are green (active) when the meeting starts
        document.querySelectorAll('.employee-btn.active').forEach(button => {
            const userId = button.getAttribute('data-id');
            if (!buttonTimers[userId]) {
                buttonTimers[userId] = timeElapsed;
            }
        });

    } else {
        clearInterval(timer);
        isRunning = false;
        startStopButton.textContent = "شروع جلسه";
        startStopButton.classList.remove('end-session');  // Revert back to green color

        // Stop timing for all green buttons when meeting is paused
        calculateGreenTimes();
    }
}

function resetTimer() {
    clearInterval(timer);
    timeElapsed = 0;
    isRunning = false;
    document.getElementById('timer').textContent = formatTime(timeElapsed);
    document.getElementById('start-stop').textContent = "شروع جلسه";
    document.getElementById('start-stop').classList.remove('end-session'); // Revert to green

    // Reset all button timing data
    buttonTimers = {};
    greenTimes = {};
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function changeColor(button) {
    const userId = button.getAttribute('data-id');

    if (!isRunning) return;  // Do nothing if the meeting isn't running

    button.classList.toggle('active');  // Toggle green color
    
    if (button.classList.contains('active')) {
        // Button turned green, start tracking its time
        if (!buttonTimers[userId]) {
            buttonTimers[userId] = timeElapsed;  // Store the time when button turned green
        }
    } else {
        // Button turned red, stop tracking its time
        if (buttonTimers[userId]) {
            const greenTime = timeElapsed - buttonTimers[userId];
            greenTimes[userId] = (greenTimes[userId] || 0) + greenTime;
            buttonTimers[userId] = null;  // Reset timer for this button
        }
    }
}

// Calculate the total time each button stayed green after the meeting stops
function calculateGreenTimes() {
    for (const userId in buttonTimers) {
        if (buttonTimers[userId]) {
            const greenTime = timeElapsed - buttonTimers[userId];
            greenTimes[userId] = (greenTimes[userId] || 0) + greenTime;
        }
    }

    console.log('Green times for each user:', greenTimes);

    // Display or send the results to the server
    displayGreenTimes();
}

function displayGreenTimes() {
    // This function will display the green times in a table or on the report page
    const reportPage = document.getElementById('report');  // Assuming there's an element with ID 'report'
    if (!reportPage) return;

    // Create table rows for each user
    let tableHTML = '<table><tr><th>کاربر</th><th>زمان سبز</th></tr>';
    for (const userId in greenTimes) {
        const timeInMinutes = (greenTimes[userId] / 60).toFixed(2);  // Convert to minutes
        tableHTML += `<tr><td>${userId}</td><td>${timeInMinutes} دقیقه</td></tr>`;
    }
    tableHTML += '</table>';

    reportPage.innerHTML = tableHTML;  // Insert the table into the report page
}

function openNewMeetingModal() {
    document.getElementById('new-meeting-modal').style.display = "block";
}

function closeNewMeetingModal() {
    document.getElementById('new-meeting-modal').style.display = "none";
}

// Close modal if clicked outside
window.onclick = function(event) {
    const modal = document.getElementById('new-meeting-modal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const alertBox = document.getElementById('success-alert');
    
    if (alertBox) {
        setTimeout(() => {
            alertBox.classList.add('hidden');
        }, 3000);  // Hide after 3 seconds
    }
});

function showModal() {
    document.getElementById('new-meeting-modal').style.display = 'block';
}

// Attach this function to the "جلسه جدید" button
document.getElementById('new-meeting-button').onclick = showModal;