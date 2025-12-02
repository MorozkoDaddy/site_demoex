from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def verify_password(email, password):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(user_import)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Столбцы таблицы user_import: {columns}")
        
        if len(columns) < 4:
            print("Таблица user_import имеет меньше 4 столбцов!")
            return False, None, None, None

        status_column = columns[0]   # Статус — 1-й столбец
        name_column = columns[1]     # Имя — 2-й
        email_column = columns[2]    # Email — 3-й
        password_column = columns[3] # Пароль — 4-й
        
        print(f" Столбец статуса: {status_column}")
        print(f" Столбец имени: {name_column}")
        print(f" Столбец email: {email_column}")
        print(f" Столбец password: {password_column}")
        
        cursor.execute(f'''
            SELECT "{status_column}", "{name_column}", "{email_column}" 
            FROM user_import 
            WHERE "{email_column}" = ? AND "{password_column}" = ?
        ''', (email, password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_status, user_name, user_email = result
            print(f"Успешный вход: {user_email}, имя: {user_name}, статус: {user_status}")
            return True, user_status, user_name, user_email
        else:
            print(f"Неверные данные для: {email}")
            return False, None, None, None
            
    except Exception as e:
        print(f"Ошибка базы: {e}")
        return False, None, None, None

def get_all_tovar():
    """Получает весь ассортимент обуви из таблицы 'Tovar'"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(Tovar)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Столбцы таблицы Tovar: {columns}")

        if len(columns) < 11:
            print("Таблица Tovar имеет меньше 11 столбцов!")
            return []

        cursor.execute("SELECT * FROM Tovar")
        rows = cursor.fetchall()
        conn.close()

        tovar_list = [dict(zip(columns, row)) for row in rows]
        return tovar_list

    except Exception as e:
        print(f"Ошибка при загрузке товаров из Tovar: {e}")
        return []

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    print(f"Попытка входа: {email}")
    
    if not email or not password:
        return "Заполните все поля", 400
    
    #распак значений 4х
    success, user_status, user_name, user_email = verify_password(email, password)
    
    if success:
        session['user_email'] = user_email
        session['user_name'] = user_name
        session['user_status'] = user_status  # сохр статуса //2
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
    
    tovar = get_all_tovar()  
    
    return render_template('main.html',
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'),
                         user_status=session.get('user_status'),
                         shoes=tovar) 

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)