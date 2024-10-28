from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db
from models import Task, Project
from datetime import datetime

bp = Blueprint('tasks', __name__)

@bp.route('/projects/<int:project_id>/kanban')
def kanban_board(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('tasks/kanban.html', project=project, tasks=tasks)

@bp.route('/projects/<int:project_id>/tasks/new', methods=['GET', 'POST'])
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        task = Task()
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.project_id = project_id
        task.estimated_time = int(request.form.get('estimated_time', 0))
        
        if request.form.get('due_date'):
            task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.kanban_board', project_id=project_id))
    
    return render_template('tasks/form.html', project_id=project_id)

@bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.estimated_time = int(request.form.get('estimated_time', 0))
        task.time_spent = int(request.form.get('time_spent', 0))
        
        if request.form.get('due_date'):
            task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        
        task.completion_percentage = min(100.0, (task.time_spent / task.estimated_time * 100) if task.estimated_time > 0 else 0)
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.kanban_board', project_id=task.project_id))
    
    return render_template('tasks/form.html', task=task, project_id=task.project_id)

@bp.route('/tasks/<int:task_id>/update-status', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    new_status = request.form['status']
    task.status = new_status
    
    if new_status == 'in_progress' and not task.start_datetime:
        task.start_datetime = datetime.utcnow()
    elif new_status == 'done' and not task.end_datetime:
        task.end_datetime = datetime.utcnow()
        
        # Update project statistics
        project = task.project
        if project.statistics:
            project.statistics.total_tasks_completed += 1
            project.statistics.total_time_spent += task.time_spent
            project.statistics.average_task_completion_time = (
                project.statistics.total_time_spent / project.statistics.total_tasks_completed
            )
        
        # Update project completion percentage
        total_tasks = Task.query.filter_by(project_id=task.project_id).count()
        completed_tasks = Task.query.filter_by(project_id=task.project_id, status='done').count()
        project.completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
    db.session.commit()
    return jsonify({'success': True})
