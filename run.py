from server import app
import uvicorn

def run_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    try:
        run_uvicorn()
    except KeyboardInterrupt:
        print("Server shutdown initiated by KeyboardInterrupt.")
    finally:
        print("Server stopped - resources released.")