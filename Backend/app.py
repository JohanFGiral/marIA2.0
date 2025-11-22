import sys
import os

# Asegurarse de que el directorio actual esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.routes import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
