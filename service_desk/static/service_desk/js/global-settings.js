//Set timeout for all messages.
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        bootstrap.Alert.getOrCreateInstance(alert).close();
    });
}, 3000);