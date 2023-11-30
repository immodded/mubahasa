function closeMessage(button) {
    var messageItem = button.parentNode;
    messageItem.style.display = "none";
}

window.onload = function() {
    var messageItem = document.getElementById('notifications');
    setTimeout(function() {
        messageItem.style.display = 'none';
    }, 4000);
};
