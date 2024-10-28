from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSONB

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime)  # Changed from target_completion_date
    status = db.Column(db.String(20), default='active')
    total_estimated_hours = db.Column(db.Float, default=0.0)
    actual_hours_spent = db.Column(db.Float, default=0.0)
    completion_percentage = db.Column(db.Float, default=0.0)
    team_velocity = db.Column(db.Float, default=0.0)
    risk_status = db.Column(db.String(20), default='low')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='project', lazy=True, cascade='all, delete-orphan')
    files = db.relationship('File', backref='project', lazy=True, cascade='all, delete-orphan')
    statistics = db.relationship('Statistics', backref='project', uselist=False, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, done
    priority = db.Column(db.String(20), default='medium')
    due_date = db.Column(db.DateTime)
    time_spent = db.Column(db.Integer, default=0)  # in minutes
    estimated_time = db.Column(db.Integer, default=0)  # in minutes
    completion_percentage = db.Column(db.Float, default=0.0)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    comments_history = db.Column(JSONB, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, unique=True)
    total_tasks_completed = db.Column(db.Integer, default=0)
    total_time_spent = db.Column(db.Integer, default=0)  # in minutes
    average_task_completion_time = db.Column(db.Float, default=0.0)  # in minutes
    burndown_data = db.Column(JSONB, default=dict)
    velocity_metrics = db.Column(JSONB, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    template_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(50))
    size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
