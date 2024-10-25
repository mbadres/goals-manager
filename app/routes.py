from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from sqlalchemy import text

from . import db
from .models import Goal, History

main = Blueprint('main', __name__)


@main.route('/')
def index():
    goals = Goal.query.all()
    return render_template('pages/index.html', goals=goals)


@main.route('/goals/new')
def new_goal():
    return render_template('pages/goal_form.html')


@main.route('/goals', methods=['POST'])
def create_goal():
    data = request.form

    new_goal = Goal(
        department=data['department'],
        statement=data['statement'],
        criteria=data['criteria']
    )
    db.session.add(new_goal)
    db.session.commit()

    # Create initial history
    initial_history = History(
        goal_id=new_goal.id,
        score=int(data['score']),
        state=data['state'],
        comment=data['comment'],
        modified_by=data['modified_by']
    )
    db.session.add(initial_history)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/goals/<int:goal_id>/edit')
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return render_template('pages/goal_form.html', goal=goal)


@main.route('/goals/<int:goal_id>', methods=['POST'])
def save_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    data = request.form

    goal.department = data['department']
    goal.statement = data['statement']
    goal.criteria = data['criteria']

    # Add new history entry
    new_history = History(
        goal_id=goal.id,
        score=int(data['score']),
        state=data['state'],
        comment=data['comment'],
        modified_by=data['modified_by']
    )
    db.session.add(new_history)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/goals/<int:goal_id>/delete', methods=['POST'])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    # Delete all related histories first
    History.query.filter_by(goal_id=goal_id).delete()
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/goals/<int:goal_id>')
def view_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    histories = History.query.filter_by(goal_id=goal_id).order_by(History.modified_at.desc()).all()
    return render_template('pages/details.html', goal=goal, histories=histories)


@main.route('/api/average-scores')
def get_average_scores():
    # Get daily average scores per department
    sql = text("""
        SELECT 
            DATE(h.modified_at) as date,
            g.department,
            ROUND(AVG(h.score), 1) as avg_score
        FROM histories h
        JOIN goals g ON h.goal_id = g.id
        GROUP BY DATE(h.modified_at), g.department
        ORDER BY date, department
    """)

    results = db.session.execute(sql)

    # Organize data by department
    departments_data = {}

    for row in results:
        date = row[0].strftime('%Y-%m-%d')
        department = row[1]
        score = float(row[2])

        if department not in departments_data:
            departments_data[department] = {
                'label': department,
                'data': [],
                'borderColor': None,  # Will be set based on department
                'tension': 0.1
            }

        departments_data[department]['data'].append({
            'x': date,
            'y': score
        })

    datasets = []
    for department, data in departments_data.items():
        datasets.append(data)

    return jsonify(datasets)
