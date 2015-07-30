# Entry point for all to avoid circular imports
from app import app
from auth import *
from views import *


if __name__ == "__main__":
    app.run(debug=True)
