from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse

from controllers.task_controller import task_router

app = FastAPI(
        title="Task API"
    ,   description="API para gerenciamento de tarefas"
    ,   version="0.1"
    ,   openapi_url="/openapi.json"
    ,   docs_url=None
    ,   redoc_url=None
    ,   contact={
        "name": "Matheus de Almeida Cantarutti",
        "email": "cantaruttim@outlook.com"
    },
    license_info=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server - API"
        }
    ],
)

app.include_router(task_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(requests, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"message": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"message":"An unexpected error occured"}
    )

@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )


@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Users API",
        version="1.0.0",
        description="API para gerenciamento de usuários",
        routes=app.routes,
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)