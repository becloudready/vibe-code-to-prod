

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user collection
users = []
next_id = 1

from flask import Flask
from controllers.user_controller import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


