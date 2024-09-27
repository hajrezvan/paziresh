let timer;
let isRunning = false;
let timeElapsed = 0;
let userTimes = {}; // Object to store time for each user

function startTimer() {
    const startStopButton = document.getElementById('start-stop');
    
    if (!isRunning) {
        isRunning = true;
        startStopButton.textContent = "اتمام جلسه";
        startStopButton.classList.add('end-session');
        
        timer = setInterval(() => {
            timeElapsed++;
            document.getElementById('timer').textContent = formatTime(timeElapsed);
            
            // Update time for each active user (whose button is green)
            document.querySelectorAll('.active').forEach(button => {
                let userId = button.getAttribute('data-userid');
                if (!userTimes[userId]) {
                    userTimes[userId] = 0;
                }
                userTimes[userId] += 1;  // Increment time in seconds for active users
            });
        }, 1000);
    } else {
        clearInterval(timer);
        isRunning = false;
        startStopButton.textContent = "شروع جلسه";
        startStopButton.classList.remove('end-session');
    }
}

function resetTimer() {
    clearInterval(timer);
    timeElapsed = 0;
    isRunning = false;
    document.getElementById('timer').textContent = formatTime(timeElapsed);
    document.getElementById('start-stop').textContent = "شروع جلسه";
    document.getElementById('start-stop').classList.remove('end-session');
    
    // Reset times for all users
    userTimes = {};
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function changeColor(button) {
    button.classList.toggle('active'); // Toggle green color
}

function submitMeeting() {
    const eventId = document.getElementById('event-select').value;
    
    // Send user times and eventId to the server
    fetch('/submit_meeting', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventId: eventId,
            userTimes: userTimes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("اطلاعات جلسه با موفقیت ثبت شد!");
        } else {
            alert("خطایی رخ داد: " + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}


function openNewMeetingModal() {
    document.getElementById('new-meeting-modal').style.display = 'block';
}

function closeNewMeetingModal() {
    document.getElementById('new-meeting-modal').style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    var modal = document.getElementById('new-meeting-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};