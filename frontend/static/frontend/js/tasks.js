// Task management functions

function loadTasks(searchQuery = '') {
    let url = `${API_BASE_URL}/tasks/`;
    if (searchQuery) {
        url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    $.ajax({
        url: url,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        success: function(paginatedResponse) {
            // The response from DRF is a paginated object. We need the 'results' array.
            displayTasks(paginatedResponse.results);
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                logout();
            }
            console.error('Error loading tasks:', xhr.responseText);
        }
    });
}

function createTask(formData) {
    $.ajax({
        url: `${API_BASE_URL}/tasks/`,
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            loadTasks();
            $('#taskForm')[0].reset();
            showToast('Task created successfully!');
        },
        error: function(xhr) {
            console.error('Error creating task:', xhr.responseText);
            showToast('Error creating task. See console for details.', 'error');
        }
    });
}

function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        $.ajax({
            url: `${API_BASE_URL}/tasks/${taskId}/`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            success: function() {
                loadTasks();
                showToast('Task deleted successfully!');
            },
            error: function(xhr) {
                console.error('Error deleting task:', xhr.responseText);
                showToast('Error deleting task.', 'error');
            }
        });
    }
}

function deleteAllTasks() {
    if (confirm('Are you sure you want to delete ALL of your tasks? This action cannot be undone.')) {
        $.ajax({
            url: `${API_BASE_URL}/tasks/delete-all/`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            success: function() {
                loadTasks();
                showToast('All tasks have been deleted.');
            },
            error: function(xhr) {
                console.error('Error deleting all tasks:', xhr.responseText);
                showToast('Error deleting all tasks.', 'error');
            }
        });
    }
}

function editTask(taskId) {
    // Fetch the specific task details to populate the form
    $.ajax({
        url: `${API_BASE_URL}/tasks/${taskId}/`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        success: function(task) {
            // Populate the modal form
            $('#editTaskId').val(task.id);
            $('#editTaskTitle').val(task.title);
            $('#editTaskDescription').val(task.description || '');
            $('#editTaskAttachment').val(''); // Clear the file input
            
            const currentAttachment = $('#currentAttachment');
            if (task.attachment) {
                const fileName = task.attachment.split('/').pop();
                currentAttachment.html(`Current file: <a href="${task.attachment}" target="_blank">${fileName}</a>`);
            } else {
                currentAttachment.text('No attachment.');
            }
            
            // Show the modal
            $('#editTaskModal').show();
        },
        error: function(xhr) {
            console.error('Error fetching task details:', xhr.responseText);
            showToast('Could not load task details.', 'error');
        }
    });
}

function updateTask(taskId, formData) {
    $.ajax({
        url: `${API_BASE_URL}/tasks/${taskId}/`,
        method: 'PATCH', // PATCH is better for partial updates
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        data: formData,
        processData: false,
        contentType: false,
        success: function() {
            $('#editTaskModal').hide(); // Hide modal on success
            loadTasks();
            showToast('Task updated successfully!');
        },
        error: function(xhr) {
            console.error('Error updating task:', xhr.responseText);
            showToast('Error updating task.', 'error');
        }
    });
}

function displayTasks(tasks) {
    const tableBody = $('#tasks-table-body');
    const noTasksMessage = $('#no-tasks-message');
    const tasksTable = $('.tasks-table');
    tableBody.empty(); // Clear previous tasks

    if (tasks.length > 0) {
        tasksTable.show();
        noTasksMessage.hide();
        $('#bulk-actions').show();

        tasks.forEach(function(task) {
            const attachmentLink = task.attachment 
                ? `<a href="${task.attachment}" target="_blank" class="btn-link">View</a>` 
                : 'None';
            
            const row = `
                <tr>
                    <td data-label="Title">${task.title}</td>
                    <td data-label="Description">${task.description || ''}</td>
                    <td data-label="Created">${new Date(task.created_at).toLocaleDateString()}</td>
                    <td data-label="Attachment">${attachmentLink}</td>
                    <td data-label="Actions">
                        <div class="task-actions">
                            <button onclick="editTask(${task.id})" class="btn-edit">Edit</button>
                            <button onclick="deleteTask(${task.id})" class="btn-delete">Delete</button>
                        </div>
                    </td>
                </tr>
            `;
            tableBody.append(row);
        });
    } else {
        tasksTable.hide();
        noTasksMessage.html('You have no tasks yet. Create one above!').show();
        $('#bulk-actions').hide();
    }
}
