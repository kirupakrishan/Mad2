from routes import create_app
from service.scheduler import Scheduled
import threading

if __name__ == '__main__':
    t1 = threading.Thread(target=Scheduled)
    t1.start()
    app = create_app()
    app.run(debug=True)
    t1.join()
    