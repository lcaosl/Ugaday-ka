document.addEventListener('DOMContentLoaded', function() {
    const countdownElement = document.getElementById('countdown');
    if (countdownElement) {
        let timeParts = countdownElement.textContent.split(':');
        let totalSeconds = parseInt(timeParts[0]) * 60 + parseInt(timeParts[1]);

        function updateCountdown() {
            if (totalSeconds <= 0) {
                window.location.reload();
                return;
            }

            totalSeconds--;
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;
            countdownElement.textContent =
                `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
});