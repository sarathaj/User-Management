// Profile management functions

function loadProfile() {
    $.ajax({
        url: `${API_BASE_URL}/auth/profile/`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        success: function(profile) {
            $('#profileEmail').val(profile.email);
            $('#profileFullName').val(profile.full_name);
            $('#profileDob').val(profile.date_of_birth);
            $('#profileAddress').val(profile.address);
            $('#profileGender').val(profile.gender);
            $('#profileMobile').val(profile.mobile_number);
        },
        error: function(xhr) {
            console.error('Error loading profile:', xhr.responseText);
            if (xhr.status === 401) {
                logout();
            }
        }
    });
}

function handleProfileUpdate(event) {
    event.preventDefault();
    const profileErrorDiv = $('#profile-error');
    profileErrorDiv.hide().empty();

    const profileData = {
        email: $('#profileEmail').val(),
        full_name: $('#profileFullName').val(),
        date_of_birth: $('#profileDob').val() || null, // Send null if empty
        address: $('#profileAddress').val(),
        gender: $('#profileGender').val(),
        mobile_number: $('#profileMobile').val()
    };

    $.ajax({
        url: `${API_BASE_URL}/auth/profile/`,
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(profileData),
        success: function() {
            showToast('Profile updated successfully!');
            loadProfile(); // Reload to confirm changes
        },
        error: function(xhr) {
            const errors = xhr.responseJSON;
            let errorMessages = [];
            if (typeof errors === 'object' && errors !== null) {
                for (const field in errors) {
                    const fieldName = field.charAt(0).toUpperCase() + field.slice(1).replace('_', ' ');
                    errorMessages.push(`<strong>${fieldName}:</strong> ${errors[field].join(', ')}`);
                }
            } else {
                errorMessages.push('An unexpected error occurred. Please try again.');
            }
            profileErrorDiv.html(errorMessages.join('<br>')).show();
        }
    });
}

function handlePasswordReset(event) {
    event.preventDefault();
    const errorDiv = $('#password-reset-error');
    errorDiv.hide().empty();

    const oldPassword = $('#oldPassword').val();
    const newPassword = $('#newPassword').val();
    const newPasswordConfirm = $('#newPasswordConfirm').val();

    if (newPassword !== newPasswordConfirm) {
        errorDiv.text("New passwords do not match.").show();
        return;
    }

    $.ajax({
        url: `${API_BASE_URL}/auth/password/reset/`,
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword,
            new_password_confirm: newPasswordConfirm
        }),
        success: function() {
            showToast('Password reset successfully!');
            $('#passwordResetForm')[0].reset();
        },
        error: function(xhr) {
            const errors = xhr.responseJSON;
            let errorMessages = [];
            if (typeof errors === 'object' && errors !== null) {
                for (const field in errors) {
                    if (field === 'detail') {
                        errorMessages.push(errors[field]);
                    } else {
                        const fieldName = field.charAt(0).toUpperCase() + field.slice(1).replace(/_/g, ' ');
                        errorMessages.push(`<strong>${fieldName}:</strong> ${errors[field].join(', ')}`);
                    }
                }
            } else {
                errorMessages.push('An unexpected error occurred. Please try again.');
            }
            errorDiv.html(errorMessages.join('<br>')).show();
        }
    });
}