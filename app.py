import sanic
from keys import credentials

app = sanic.Sanic("Reminder")

app.static("/", "./templates/index.html")

'''
@app.route("/")
async def index(request):
    with open("templates/index.html") as file:
    html_content = file.read()
    return sanic.response.html(html_content)
'''


@app.route("/login", methods=["POST"])
async def login(request):
    username = request.form.get("username")
    password = request.form.get("password")

    if username in credentials and credentials[username] == password:
        return sanic.response.redirect("/reminder")
    else:
        return sanic.response.html("<h2>Usuario o contraseña incorrectos.</h2>")


@app.route("/reminder")
async def calendar(request):
    with open("templates/reminder.html", encoding="utf-8") as file:
        html_content = file.read()
    return sanic.response.html(html_content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)