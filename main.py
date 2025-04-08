from fastapi import FastAPI

# TODO: Import router modules from the riders, drivers, rides, and payments packages
# Example:
# from riders import router as riders_router
# from drivers import router as drivers_router
# from rides import router as rides_router
# from payments import router as payments_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application for the Uber_lite service.

    This function initializes the FastAPI instance and includes router modules
    from riders, drivers, rides, and payments.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(title="Uber_lite")

    # TODO: Include the imported routers
    # Example:
    # app.include_router(riders_router, prefix="/riders", tags=["Riders"])
    # app.include_router(drivers_router, prefix="/drivers", tags=["Drivers"])
    # app.include_router(rides_router, prefix="/rides", tags=["Rides"])
    # app.include_router(payments_router, prefix="/payments", tags=["Payments"])

    return app


def run_app(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    """
    Run the application using uvicorn.

    Args:
        host (str): The host interface to bind to.
        port (int): The port on which to run the application.
        reload (bool): Enable auto-reload for development.

    Returns:
        None
    """
    try:
        import uvicorn
        uvicorn.run("main:create_app", host=host, port=port, reload=reload)
    except ImportError as exc:
        print(f"Uvicorn is not installed. Please install it and try again. Error: {exc}")
    except Exception as exc:
        print(f"An error occurred while starting the server: {exc}")