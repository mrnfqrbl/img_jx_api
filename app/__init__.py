from fastapi import FastAPI

def create_app():
    app = FastAPI()

    # 导入并注册路由
    from app.api_router.router import router
    app.include_router(router)

    return app