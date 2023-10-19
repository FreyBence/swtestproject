import os.path

from flask import Flask
from views import views

app = Flask("SW test project")
app.register_blueprint(views, url_prfix="/views")
app.secret_key = "sw_test_project.com"

app.config["MAIL_SERVER"] = "localhost"  # default port is 25

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # allow Http traffic for local dev

# if __name__ == '__main__':
    #  app.run(debug=True)
  
# default port is 5000

app.run()
