import uvicorn
from pyasic_api.app import app
import pyasic_api.get
import pyasic_api.post

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4028)
