from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Project
from datetime import datetime

bp = Blueprint('projects', __name__)

@bp.route('/projects')
def list_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects/list.html', projects=projects)

@bp.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project = Project(
            name=request.form['name'],
            description=request.form['description'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            status='active'
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html')

@bp.route('/projects/<int:id>')
def view_project(id):
    project = Project.query.get_or_404(id)
    return render_template('projects/detail.html', project=project)

@bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        project.status = request.form['status']
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.view_project', id=project.id))
    return render_template('projects/form.html', project=project)

@bp.route('/projects/<int:id>/delete', methods=['POST'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list_projects'))
