// Sample profile data (replace this with actual user data)
var userProfile = {
    firstName: "Stud_name",
    lastName: "Surname",
    email: "email@example.com",
    // Add more profile information as needed
};

// Function to display user profile information on the dashboard
function displayProfile() {
    var profileInfo = document.getElementById('profileInfo');
    var profileHTML = "<p><strong>Name:</strong> " + userProfile.firstName + " " + userProfile.lastName + "</p>";
    profileHTML += "<p><strong>Email:</strong> " + userProfile.email + "</p>";
    // Add more profile information as needed

    profileInfo.innerHTML = profileHTML;
}

// Call the function to display the profile information when the dashboard loads
window.onload = function () {
    displayProfile();
    // Add more initialization logic if needed
}
