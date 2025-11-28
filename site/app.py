from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def verify_password(email, password):
    """Проверяет логин и пароль в базе данных и возвращает данные пользователя"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(user_import)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📊 Столбцы таблицы: {columns}")
        
        email_column = columns[2]  
        password_column = columns[3]  
        name_column = columns[1]  
        
        print(f"👤 Столбец имени: {name_column}")
        print(f"📧 Столбец email: {email_column}")
        print(f"🔑 Столбец password: {password_column}")
        
        # Ищем пользователя и возвращаем его имя
        cursor.execute(f'''
            SELECT "{name_column}" FROM user_import 
            WHERE "{email_column}" = ? AND "{password_column}" = ?
        ''', (email, password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_name = result[0]
            print(f"Успешный вход для {email}, имя: {user_name}")
            return True, user_name
        else:
            print(f"Неверные данные для {email}")
            return False, None
            
    except Exception as e:
        print(f"Ошибка базы {e}")
        return False, None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    print(f"🚀 Попытка входа: {email}")
    
    if not email or not password:
        return "Заполните все поля", 400
    
    success, user_name = verify_password(email, password)
    
    if success:
        session['user_email'] = email
        session['user_name'] = user_name  # Сохраняем имя в сессии
        session['logged_in'] = True
        return redirect(url_for('main_page'))
    else:
        return '''
        <script>
            alert("Неверный email или пароль");
            window.location.href = "/";
        </script>
        '''

@app.route('/main')
def main_page():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('main.html', 
                         user_name=session.get('user_name'),  # Передаем имя
                         user_email=session.get('user_email'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)