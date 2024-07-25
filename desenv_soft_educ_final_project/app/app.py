from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from models import purchase_item, check_user_exists, create_player, validate_login, get_player_score, get_levels, check_level_unlocked, get_level_details, get_character_dialogs, get_questions, create_question_answer, get_time_setting, get_level_setting, get_score_setting, mark_level_completed, create_score_record, check_answer_correct, get_num_correct_answers, create_level_session, get_latest_level_session_id, unlock_level, get_customization_items, get_player_inventory
import datetime
from config import Config

app = Flask(__name__)
app.config.from_object('config.Config')

DIFFICULTY_MAP = {
    'easy': 'Fácil',
    'medium': 'Médio',
    'hard': 'Difícil'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    valid, message, player_id = validate_login(username, password)
    
    if not valid:
        flash(message)
        return redirect(url_for('home'))
    
    session['player_id'] = player_id
    return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if check_user_exists(username):
            flash("Erro: Nome de usuário já existe.")
            return redirect(url_for('register'))
        
        try:
            create_player(name, username, password, email)
            flash("Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Erro ao conectar ao Salesforce: {e}")
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/main')
def main():
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))
    
    total_score = int(get_player_score(player_id))  # Converte para inteiro
    return render_template('main.html', total_score=total_score)

@app.route('/niveis')
def niveis():
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))

    levels = get_levels()
    for level in levels:
        level['unlocked'] = check_level_unlocked(player_id, level['Id'])
        level['Difficulty__c'] = DIFFICULTY_MAP.get(level['Difficulty__c'].lower(), level['Difficulty__c'])
    
    total_score = get_player_score(player_id)
    return render_template('niveis.html', levels=levels, total_score=total_score)

@app.route('/level/<level_id>')
def load_level(level_id):
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))
    
    level_details = get_level_details(level_id)
    character_dialogs = get_character_dialogs(level_details['Character__c'])
    total_score = get_player_score(player_id)
    
    character_image = ""
    if level_details and 'Character__r' in level_details and 'ImageURL__c' in level_details['Character__r']:
        character_image = level_details['Character__r']['ImageURL__c']
    
    background_image = level_details.get('ImageURL__c', '')

    return render_template('level.html', level=level_details, dialogs=character_dialogs, total_score=total_score, character_image=character_image, background_image=background_image)

@app.route('/start_level/<level_id>')
def start_level(level_id):
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))
    
    questions = get_questions(level_id)
    time_setting = get_time_setting(level_id)
    total_score = get_player_score(player_id)
    level_details = get_level_details(level_id)
    
    create_level_session(level_id, player_id)
    level_session_id = get_latest_level_session_id(level_id, player_id)

    session['questions'] = questions
    session['current_question'] = 0
    session['start_time'] = datetime.datetime.now(datetime.timezone.utc)
    session['level_session_id'] = level_session_id

    return render_template('game.html', level=level_details, current_question=questions[0], time_setting=time_setting, total_score=total_score, start_time=session['start_time'].isoformat())

@app.route('/process_question/<level_id>', methods=['POST'])
def process_question(level_id):
    player_id = session.get('player_id')
    current_question = session.get('current_question', 0)
    questions = session.get('questions', [])
    question_option_id = request.form['question_option_id']
    start_time = request.form['start_time']
    end_time = datetime.datetime.now(datetime.timezone.utc)
    level_session_id = session.get('level_session_id')

    if current_question < len(questions):
        question_id = questions[current_question]['Id']
        create_question_answer(player_id, question_id, question_option_id, start_time, end_time, level_session_id)
        
        if check_answer_correct(question_option_id):
            score_setting = get_score_setting('Answer Question Correct', level_id)
            create_score_record(player_id, score_setting)

    session['current_question'] += 1

    if session['current_question'] >= len(questions):
        return redirect(url_for('finish_level', level_id=level_id))

    return render_template('game.html', level=get_level_details(level_id), current_question=questions[session['current_question']], time_setting=get_time_setting(level_id), total_score=get_player_score(player_id), start_time=end_time.isoformat())

@app.route('/finish_level/<level_id>')
def finish_level(level_id):
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))

    level_setting = get_level_setting(level_id)
    level_session_id = session.get('level_session_id')
    num_correct_answers = get_num_correct_answers(player_id, level_id, level_session_id)
    time_setting = get_time_setting(level_id)
    start_time = session.get('start_time')
    
    if isinstance(start_time, str):
        start_time = datetime.datetime.fromisoformat(start_time)

    elapsed_time = (datetime.datetime.now(datetime.timezone.utc) - start_time).total_seconds()

    total_score = get_player_score(player_id)

    if elapsed_time > time_setting:
        return render_template('end_game.html', result="time_over", total_score=total_score)
    
    if num_correct_answers >= level_setting:
        mark_level_completed(player_id, level_id)
        score_setting = get_score_setting('Level Up', level_id)
        create_score_record(player_id, score_setting)
        return render_template('end_game.html', result="win", total_score=total_score)
    else:
        return render_template('end_game.html', result="fail", total_score=total_score)

@app.route('/customizacao')
def customizacao():
    player_id = session.get('player_id')
    if not player_id:
        return redirect(url_for('home'))

    customization_items = get_customization_items()
    player_inventory = get_player_inventory(player_id)
    total_score = get_player_score(player_id)
    
    return render_template('customizacao.html', customization_items=customization_items, player_inventory=player_inventory, total_score=total_score)

@app.route('/unlock_level', methods=['POST'])
def unlock_level_endpoint():
    player_id = session.get('player_id')
    if not player_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    level_id = request.form['level_id']
    unlock_score = int(float(request.form['unlock_score']))

    success, message, player_level = unlock_level(player_id, level_id, unlock_score)
    if success:
        flash(message)
    else:
        flash(message)

    return redirect(url_for('niveis'))

@app.route('/purchase_item', methods=['POST'])
def purchase_item_endpoint():
    player_id = session.get('player_id')
    if not player_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    item_id = request.form['item_id']
    price = int(float(request.form['price']))

    success, message = purchase_item(player_id, item_id, price)
    if success:
        flash(message)
    else:
        flash(message)

    return redirect(url_for('customizacao'))

if __name__ == '__main__':
    app.run(debug=True)

