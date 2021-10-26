from provenance.main import app

if __name__ == "__main__":
    import uvicorn
    import logging

    log_format = "%(asctime)-15s %(levelname)-8s %(message)s - %(pathname)s:%(lineno)d (%(funcName)s)"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
