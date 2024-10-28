document.addEventListener('DOMContentLoaded', function() {
    const columns = document.querySelectorAll('.kanban-column');
    
    // Enable drag and drop for tasks
    document.querySelectorAll('.task-card').forEach(task => {
        task.setAttribute('draggable', true);
        task.addEventListener('dragstart', handleDragStart);
        task.addEventListener('dragend', handleDragEnd);
    });

    columns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
    });

    function handleDragStart(e) {
        e.target.classList.add('dragging');
        e.dataTransfer.setData('text/plain', e.target.id);
    }

    function handleDragEnd(e) {
        e.target.classList.remove('dragging');
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        const taskId = e.dataTransfer.getData('text/plain');
        const task = document.getElementById(taskId);
        const column = e.target.closest('.kanban-column');
        const status = column.dataset.status;

        // Update task status in backend
        fetch(`/tasks/${taskId}/update-status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${status}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                column.querySelector('.tasks-container').appendChild(task);
            }
        });
    }
});
