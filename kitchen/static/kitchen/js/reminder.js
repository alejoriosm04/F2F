// JavaScript code for displaying the modal
window.onload = function() {
    var modal = document.getElementById('miModal');
    var span = document.getElementsByClassName("close")[0];
    var reminderText = document.getElementById('updateReminder');
    var modal = document.getElementById('miModal');
    modal.style.display = 'flex'; // Esto activará flexbox y mostrará el modal
    // Cuando el usuario clickea en (x), cierra el modal
    span.onclick = function() {
        modal.style.display = "none";
    }
    // Cuando el usuario clickea fuera del modal, cierra el modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
};
