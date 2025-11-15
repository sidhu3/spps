function confirmLogout() {
        if (confirm("Are you sure you want to logout?")) {
            window.location.href = "/logout"; // Navigate to logout route
        }
    }

// function confirmLogout() {
//         if (confirm("Are you sure you want to logout?")) {
//             document.getElementById('logoutForm').submit();
//         }
//     }