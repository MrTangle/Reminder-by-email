import sanic
import logging
from sanic.log import logger
from keys import credentials
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader
from email_sender import send_confirmation_email


logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


app = sanic.Sanic("ReminderFasturApp")


# Establecer conexión con mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['reminder_app']
collection = db['reminders']


# Configurar Jinja2
env = Environment(loader=FileSystemLoader("templates"))


@app.route("/")
async def index(request):
    with open("templates/index.html", encoding="UTF-8") as file:
        html_content = file.read()
    return sanic.response.html(html_content)


@app.route("/login", methods=["POST"])
async def login(request):
    username = request.form.get("username")
    password = request.form.get("password")

    if username in credentials and credentials[username] == password:
        logger.info("Inicio de sesión exitoso con el usuario: {}".format(username))
        return sanic.response.redirect("/reminder")
    else:
        logger.warning("Inicio de sesión fallido con el usuario: {}".format(username))
        return sanic.response.html("<h2>Usuario o contraseña incorrectos.</h2>")


@app.route("/reminder", methods=["GET", "POST"])
async def calendar(request):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")

        reminder = {
            "title": title,
            "description": description,
            "date": date
        }

        try:
            collection.insert_one(reminder)
            logger.info("Nuevo recordatorio agregado: {}".format(title))
        except Exception as e:
            logger.error("Error al guardar el documento en MongoDB: {}".format(str(e)))

        await send_confirmation_email(title, description, date)

        return sanic.response.redirect("/reminder")

    reminders = collection.find()

    template = env.get_template("reminder.html")
    html_content = template.render(reminders=reminders)

    return sanic.response.html(html_content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
