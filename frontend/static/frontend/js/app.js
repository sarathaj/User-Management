$(document).ready(function() {
    // Check login status on page load
    updateUIForLoginStatus();

    // --- Auth Form Switching ---
    $('#showRegister').on('click', function(e) {
        e.preventDefault();
        $('#loginForm').hide();
        $('#registerForm').show();
    });

    $('#showLogin').on('click', function(e) {
        e.preventDefault();
        $('#registerForm').hide();
        $('#loginForm').show();
    });

    // --- Registration ---
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        const registerErrorDiv = $('#register-error');
        registerErrorDiv.hide().empty(); // Reset errors on new submission

        const fullName = $('#registerFullName').val();
        const email = $('#registerEmail').val();
        const password = $('#registerPassword').val();
        const passwordConfirm = $('#registerPasswordConfirm').val();

        // --- Client-side validation ---
        if (password !== passwordConfirm) {
            registerErrorDiv.text("Passwords do not match. Please try again.").show();
            return; // Stop the form submission
        }
        // --- End validation ---

        $.ajax({
            url: `${API_BASE_URL}/auth/register/`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: email,
                password: password,
                password_confirm: passwordConfirm,
                full_name: fullName
            }),
            success: function() {
                showToast('Registration successful! Please log in.');
                $('#registerForm').hide();
                $('#loginForm').show();
                $('#registerForm')[0].reset();
            },
            error: function(xhr) {
                // Improved error display
                const errors = xhr.responseJSON;
                let errorMessages = [];
                for (const field in errors) {
                    const fieldName = field.charAt(0).toUpperCase() + field.slice(1).replace('_', ' ');
                    errorMessages.push(`<strong>${fieldName}:</strong> ${errors[field].join(', ')}`);
                }
                registerErrorDiv.html(errorMessages.join('<br>')).show();
            }
        });
    });

    // --- Login ---
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        const email = $('#loginEmail').val();
        const password = $('#loginPassword').val();

        $.ajax({
            url: `${API_BASE_URL}/auth/login/`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: email,
                password: password
            }),
            success: function(response) {
                localStorage.setItem('access_token', response.access);
                localStorage.setItem('refresh_token', response.refresh);
                updateUIForLoginStatus();
            },
            error: function() {
                // Use the same error display pattern for consistency
                const loginErrorHtml = `<div id="login-error" class="form-error">Login failed. Please check your credentials.</div>`;
                if ($('#login-error').length === 0) {
                    $('#loginForm h2').after(loginErrorHtml);
                }
            }
        });
    });

    // --- Task Creation ---
    $('#taskForm').on('submit', function(e) {
        e.preventDefault();
        let formData = new FormData();
        formData.append('title', $('#taskTitle').val());
        formData.append('description', $('#taskDescription').val());
        
        let attachment = $('#taskAttachment')[0].files[0];
        if (attachment) {
            formData.append('attachment', attachment);
        }
        
        createTask(formData); // From tasks.js
    });

    // --- Profile Update ---
    $('#profileForm').on('submit', handleProfileUpdate); // from profile.js

    // --- Password Reset ---
    $('#passwordResetForm').on('submit', handlePasswordReset); // from profile.js

    // --- Toggle Password Reset Form ---
    $('#togglePasswordResetBtn').on('click', function() {
        $('#passwordResetContainer').slideToggle();
    });
    $('#deleteAllTasksBtn').on('click', function() {
        deleteAllTasks(); // from tasks.js
    });

    // --- Search Tasks ---
    $('#searchForm').on('submit', function(e) {
        e.preventDefault();
        const query = $('#searchInput').val();
        loadTasks(query); // from tasks.js
    });

    // --- Edit Task Modal Logic ---
    const editModal = $('#editTaskModal');

    // Close modal with the 'x' button
    $('.close-button').on('click', function() {
        editModal.hide();
    });

    // Close modal if user clicks outside of it
    $(window).on('click', function(event) {
        if ($(event.target).is(editModal)) {
            editModal.hide();
        }
    });

    // Handle Edit Task form submission
    $('#editTaskForm').on('submit', function(e) {
        e.preventDefault();
        const taskId = $('#editTaskId').val();
        
        let formData = new FormData();
        formData.append('title', $('#editTaskTitle').val());
        formData.append('description', $('#editTaskDescription').val());
        
        let attachment = $('#editTaskAttachment')[0].files[0];
        if (attachment) {
            formData.append('attachment', attachment);
        }
        updateTask(taskId, formData); // from tasks.js
    });

    // --- Navigation ---
    setupNavigation();
});

function updateUIForLoginStatus() {
    if (isLoggedIn()) {
        $('#auth-container').hide();
        $('#main-nav').show();
        showTaskManager(); // Show tasks by default
        $('#auth-links').html('<a href="#" id="logout-button">Logout</a>');

        $('#logout-button').on('click', function(e) {
            e.preventDefault();
            logout();
        });
    } else {
        $('#auth-container').show();
        $('#task-manager-container').hide();
        $('#profile-manager-container').hide();
        $('#main-nav').hide();
        $('#auth-links').html('');
        $('#loginForm')[0].reset();
        $('#registerForm')[0].reset();
    }
}

function isLoggedIn() {
    return localStorage.getItem('access_token') !== null;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    showToast('You have been logged out.');
    updateUIForLoginStatus();
}

function setupNavigation() {
    const nav = $('#main-nav');
    nav.html(`
        <a href="#" id="nav-tasks" class="active">My Tasks</a>
        <a href="#" id="nav-profile">My Profile</a>
    `);

    $('#nav-tasks').on('click', function(e) {
        e.preventDefault();
        showTaskManager();
    });

    $('#nav-profile').on('click', function(e) {
        e.preventDefault();
        showProfileManager();
    });
}

function showTaskManager() {
    $('#profile-manager-container').hide();
    $('#task-manager-container').show();
    $('#main-nav a').removeClass('active');
    $('#nav-tasks').addClass('active');
    loadTasks(); // from tasks.js
}

function showProfileManager() {
    $('#task-manager-container').hide();
    $('#profile-manager-container').show();
    $('#main-nav a').removeClass('active');
    $('#nav-profile').addClass('active');
    loadProfile(); // from profile.js
    // Ensure the password form is hidden and reset when switching to the profile view
    $('#passwordResetContainer').hide();
    $('#passwordResetForm')[0].reset();
    $('#password-reset-error').hide();
}

function showToast(message, type = 'success') {
    const toastContainer = $('#toast-container');
    const toast = $('<div class="toast"></div>').text(message);
    toast.addClass(type); // Add class for styling (e.g., 'success', 'error')
    toastContainer.append(toast);

    // Animate in
    setTimeout(() => {
        toast.addClass('show');
    }, 100);

    // Animate out and remove
    setTimeout(() => {
        toast.removeClass('show');
        // Remove the element after the transition is complete
        toast.on('transitionend', function() {
            $(this).remove();
        });
    }, 3000); // Display for 3 seconds
}