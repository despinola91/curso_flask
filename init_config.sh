source venv/bin/activate

export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
export GOOGLE_CLOUD_PROJECT=lista-tareas-315321
flask run
