document.addEventListener('DOMContentLoaded', function() {
    const columns = document.querySelectorAll('.kanban-column');
    let activeTimers = {};
    
    // Initialize drag and drop for tasks
    document.querySelectorAll('.task-card').forEach(task => {
        task.setAttribute('draggable', true);
        task.addEventListener('dragstart', handleDragStart);
        task.addEventListener('dragend', handleDragEnd);
    });

    columns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('dragenter', handleDragEnter);
        column.addEventListener('dragleave', handleDragLeave);
        column.addEventListener('drop', handleDrop);
    });

    // Quick add task buttons
    document.querySelectorAll('.quick-add-task').forEach(button => {
        button.addEventListener('click', () => {
            const status = button.dataset.status;
            window.location.href = `/projects/${getProjectId()}/tasks/new?status=${status}`;
        });
    });

    // Timer controls
    document.querySelectorAll('.start-timer').forEach(btn => {
        btn.addEventListener('click', handleStartTimer);
    });

    document.querySelectorAll('.pause-timer').forEach(btn => {
        btn.addEventListener('click', handlePauseTimer);
    });

    document.querySelectorAll('.stop-timer').forEach(btn => {
        btn.addEventListener('click', handleStopTimer);
    });

    // Quick edit functionality
    document.querySelectorAll('.quick-edit').forEach(btn => {
        btn.addEventListener('click', handleQuickEdit);
    });

    // Initialize Modal
    const quickEditModal = new bootstrap.Modal(document.getElementById('quickEditModal'));
    const progressSlider = document.getElementById('progressSlider');
    const progressValue = document.getElementById('progressValue');
    const saveQuickEditBtn = document.getElementById('saveQuickEdit');

    // Drag and Drop Functions
    function handleDragStart(e) {
        e.target.classList.add('dragging');
        e.dataTransfer.setData('text/plain', e.target.id);
        e.dataTransfer.effectAllowed = 'move';
    }

    function handleDragEnd(e) {
        e.target.classList.remove('dragging');
        document.querySelectorAll('.tasks-container').forEach(container => {
            container.classList.remove('drag-over');
        });
    }

    function handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    function handleDragEnter(e) {
        const container = e.target.closest('.tasks-container');
        if (container) {
            container.classList.add('drag-over');
        }
    }

    function handleDragLeave(e) {
        const container = e.target.closest('.tasks-container');
        if (container && !container.contains(e.relatedTarget)) {
            container.classList.remove('drag-over');
        }
    }

    function handleDrop(e) {
        e.preventDefault();
        const taskId = e.dataTransfer.getData('text/plain');
        const task = document.getElementById(taskId);
        const column = e.target.closest('.kanban-column');
        const container = column.querySelector('.tasks-container');
        const status = column.dataset.status;

        // Update task status in backend
        fetch(`/tasks/${taskId.split('-')[1]}/update-status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${status}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                container.appendChild(task);
                if (status === 'in_progress') {
                    task.querySelector('.start-timer')?.removeAttribute('disabled');
                } else {
                    task.querySelector('.start-timer')?.setAttribute('disabled', 'disabled');
                }
            }
        });

        container.classList.remove('drag-over');
    }

    // Timer Functions
    function handleStartTimer(e) {
        const taskId = e.target.closest('button').dataset.taskId;
        if (!activeTimers[taskId]) {
            activeTimers[taskId] = {
                interval: setInterval(() => updateTimer(taskId), 60000),
                startTime: Date.now()
            };
            e.target.closest('.task-timer').querySelector('.pause-timer').removeAttribute('disabled');
            e.target.setAttribute('disabled', 'disabled');
        }
    }

    function handlePauseTimer(e) {
        const taskId = e.target.closest('button').dataset.taskId;
        if (activeTimers[taskId]) {
            clearInterval(activeTimers[taskId].interval);
            const elapsed = Math.floor((Date.now() - activeTimers[taskId].startTime) / 60000);
            updateTimeSpent(taskId, elapsed);
            delete activeTimers[taskId];
            e.target.setAttribute('disabled', 'disabled');
            e.target.closest('.task-timer').querySelector('.start-timer').removeAttribute('disabled');
        }
    }

    function handleStopTimer(e) {
        const taskId = e.target.closest('button').dataset.taskId;
        if (activeTimers[taskId]) {
            clearInterval(activeTimers[taskId].interval);
            const elapsed = Math.floor((Date.now() - activeTimers[taskId].startTime) / 60000);
            updateTimeSpent(taskId, elapsed);
            delete activeTimers[taskId];
        }
        e.target.closest('.task-timer').querySelector('.start-timer').removeAttribute('disabled');
        e.target.closest('.task-timer').querySelector('.pause-timer').setAttribute('disabled', 'disabled');
    }

    function updateTimer(taskId) {
        const timerDisplay = document.querySelector(`#task-${taskId} .timer-display`);
        const currentTime = parseInt(timerDisplay.textContent);
        timerDisplay.textContent = `${currentTime + 1} mins`;
    }

    // Quick Edit Functions
    function handleQuickEdit(e) {
        const taskId = e.target.closest('button').dataset.taskId;
        const task = document.getElementById(`task-${taskId}`);
        const progressBar = task.querySelector('.progress-bar');
        const currentProgress = progressBar.getAttribute('aria-valuenow');
        
        progressSlider.value = currentProgress;
        progressValue.textContent = `${currentProgress}%`;
        
        const timeSpentInput = document.getElementById('timeSpent');
        timeSpentInput.value = task.querySelector('.timer-display').textContent.split(' ')[0];
        
        saveQuickEditBtn.dataset.taskId = taskId;
        quickEditModal.show();
    }

    progressSlider.addEventListener('input', (e) => {
        progressValue.textContent = `${e.target.value}%`;
    });

    saveQuickEditBtn.addEventListener('click', () => {
        const taskId = saveQuickEditBtn.dataset.taskId;
        const progress = progressSlider.value;
        const timeSpent = document.getElementById('timeSpent').value;
        
        fetch(`/tasks/${taskId}/quick-update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `progress=${progress}&time_spent=${timeSpent}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const task = document.getElementById(`task-${taskId}`);
                const progressBar = task.querySelector('.progress-bar');
                progressBar.style.width = `${progress}%`;
                progressBar.setAttribute('aria-valuenow', progress);
                progressBar.textContent = `${progress}%`;
                task.querySelector('.timer-display').textContent = `${timeSpent} mins`;
                quickEditModal.hide();
            }
        });
    });

    // Helper Functions
    function getProjectId() {
        const path = window.location.pathname;
        return path.split('/')[2];
    }

    function updateTimeSpent(taskId, elapsed) {
        fetch(`/tasks/${taskId}/update-time`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `elapsed=${elapsed}`
        });
    }
});
