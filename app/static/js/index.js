document.addEventListener("DOMContentLoaded", function() {
    const message = document.getElementsByClassName('input-field')[0]
    const chat_message = document.getElementsByClassName('chat-messages')[0]
    const userInput = document.getElementsByClassName('another-field')[0]
    const popup = document.getElementsByClassName('popup-container')[0]
    const plus_button = document.getElementsByClassName('plus-button')[0]
    const cancel = document.getElementById('cancel-button')
    const submit = document.getElementById('submit-button')
    const calendarContainer = document.getElementById("calendar-container")

    message.addEventListener("keydown", function(event) {
        if (event.key === "Enter") { 
            const message_text = message.value
            const messageDiv = document.createElement("div")
            messageDiv.classList.add("message", "sent")
            messageDiv.textContent = message_text
            chat_message.appendChild(messageDiv)
            message.value = ''
        }
    });

    submit.addEventListener("click", function() {
        const hours = document.getElementById('hours').value
        const minutes = document.getElementById('minutes').value
        const timeMessage = `${hours} hours ${minutes} mins`

        const allMessages = document.querySelectorAll('.chat-messages .message')
        let collectedText = ''

        allMessages.forEach(messageElement => {
            collectedText += messageElement.textContent + '\n'
        });

        const data = { timeMessage: timeMessage, collectedText: collectedText }

        fetch("http://localhost:8000/submit-data/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data fetched successfully:", data)
            displayCalendar(data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });

        popup.style.display = "none";
        document.getElementById('hours').value = ''
        document.getElementById('minutes').value = ''
    });

    plus_button.addEventListener("click", function() {
        popup.style.display = "flex";
    });

    cancel.addEventListener("click", function() {
        popup.style.display = "none";
    });

    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") { 
            const message_text = userInput.value;
            const messageDiv = document.createElement("div")
            messageDiv.classList.add("message", "received")
            messageDiv.textContent = message_text;
            chat_message.appendChild(messageDiv);
            userInput.value = ''
        }
    });

    function displayCalendar(data) {
        const calendar = document.getElementById("calendar");
        calendar.innerHTML = "" // Clear previous entries
        calendarContainer.style.display = "flex" // Show the calendar container
    
        data.forEach((dayData, index) => {
            const dayElement = document.createElement("div")
            dayElement.classList.add("day")
            const daysOfWeek = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
            const dayName = daysOfWeek[index]
            // If there is no data for the day, mark it accordingly
            if (dayData[0] === -1) {
                dayElement.classList.add("no-data");
                dayElement.textContent = `Day ${dayName}: No Data`
            } else {
                dayElement.classList.add("has-data");
                dayElement.textContent = `Day ${dayName}: `
    
                // Iterate over each time range in dayData
                dayData.forEach((timeRange, rangeIndex) => {
                    const startMinutes = timeRange[0]
                    const endMinutes = timeRange[1]
    
                    // Calculate hours and minutes for start and end times
                    const startHour = Math.floor(startMinutes / 60)
                    const startMin = startMinutes % 60
                    const endHour = Math.floor(endMinutes / 60)
                    const endMin = endMinutes % 60;
                    // Add more days as needed
                    // Append the time range to the day's display
                    dayElement.textContent += `from ${startHour}:${startMin.toString().padStart(2, '0')} to ${endHour}:${endMin.toString().padStart(2, '0')}`
                    
                    // Add a comma if there are multiple ranges for the day
                    if (rangeIndex < dayData.length - 1) {
                        dayElement.textContent += `, `
                    }
                });
            }
    
            calendar.appendChild(dayElement);
    
            // Start a new week row after every 7 days
            if ((index + 1) % 7 === 0) {
                const weekBreak = document.createElement("div")
                weekBreak.style.gridColumn = "span 7"
                calendar.appendChild(weekBreak)
            }
        });
    }    
    calendarContainer.addEventListener('click',function() {
        calendarContainer.style.display = "none"
    })
});
