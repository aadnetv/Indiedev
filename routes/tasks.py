from flask import Blueprint, render_template, request, jsonify
from app import db
from models import Task, Project

bp = Blueprint('tasks', __name__)

@bp.route('/projects/<int:project_id>/kanban')
def kanban_board(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('tasks/kanban.html', project=project, tasks=tasks)

@bp.route('/tasks/create', methods=['POST'])
def create_task():
    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        priority=request.form['priority'],
        due_date=request.form.get('due_date'),
        project_id=request.form['project_id']
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'success': True, 'task': {
        'id': task.id,
        'title': task.title,
        'status': task.status
    }})

@bp.route('/tasks/<int:task_id>/update-status', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form['status']
    db.session.commit()
    return jsonify({'success': True})
