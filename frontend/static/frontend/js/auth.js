// Authentication functions
const API_BASE_URL = 'http://127.0.0.1:8000/api';

function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (token) {
        $('#navLinks').hide();
        $('#userMenu').show();
        const user = JSON.parse(localStorage.getItem('user'));
        $('#username').text(user.username);
    } else {
        $('#navLinks').show();
        $('#userMenu').hide();
    }
}

function login(username, password) {
    $.ajax({
        url: `${API_BASE_URL}/accounts/login/`,
        method: 'POST',
        data: {
            username: username,
            password: password
        },
        success: function(response) {
            localStorage.setItem('access_token', response.access);
            localStorage.setItem('refresh_token', response.refresh);
            localStorage.setItem('user', JSON.stringify(response.user));
            window.location.href = 'tasks.html';
        },
        error: function(xhr) {
            alert('Login failed: ' + xhr.responseJSON.error);
        }
    });
}

function register(userData) {
    $.ajax({
        url: `${API_BASE_URL}/accounts/register/`,
        method: 'POST',
        data: userData,
        success: function(response) {
            alert('Registration successful! Please login.');
            window.location.href = 'login.html';
        },
        error: function(xhr) {
            let errors = '';
            for (let field in xhr.responseJSON) {
                errors += field + ': ' + xhr.responseJSON[field].join(', ') + '\n';
            }
            alert('Registration failed:\n' + errors);
        }
    });
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Check authentication on page load
$(document).ready(function() {
    checkAuth();
});