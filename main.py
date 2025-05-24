# main.py
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.core.config import settings
from api.routers import (
    news_router,
    business_activity_router,
    companies_router,
    industries_router,
    languages_router,
    countries_router,
    sources_router,
    themes_router,
    topics_router,
    custom_topics_router,
    content_type_router,
    sentiments_router
)

description = """
# InsightWires News Analytics API

## Features
* Company Search and Information
* Business Activities Tracking
* Content Type Classification
* Industry Analysis
* Geographic Data

## Authentication
All endpoints require API key authentication using the `X-API-Key` header.

## Rate Limits
Standard tier: 100 requests per minute
"""

app = FastAPI(
    title="InsightWires API",
    description=description,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    terms_of_service="http://insightwires.com/terms/",
    contact={
        "name": "InsightWires API Support",
        "url": "http://insightwires.com/support",
        "email": "api@insightwires.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "http://insightwires.com/license",
    }
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link type="text/css" rel="stylesheet" href="/static/custom.css">
        <title>InsightWires API Documentation</title>
        <style>
            /* Hide version number and OAS link */
            .swagger-ui .info .title small,
            .swagger-ui .info .base-url,
            .swagger-ui .info .title span {{
                display: none;
            }}

            /* Hide the top download buttons */
            .swagger-ui .topbar .download-url-wrapper {{
                display: none;
            }}

            /* Hide the Swagger top bar completely */
            .swagger-ui .topbar {{
                display: none;
            }}

            /* Style the operation blocks */
            .swagger-ui .opblock {{
                margin: 0 0 15px;
                border: 1px solid #e8e8e8;
                border-radius: 4px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}

            .swagger-ui .opblock .opblock-summary {{
                padding: 8px;
                cursor: pointer;
            }}

            .swagger-ui .opblock .opblock-summary-method {{
                background: #2c5282;
                border-color: #2c5282;
                padding: 6px 10px;
                border-radius: 3px;
                color: white;
                font-weight: bold;
            }}

            /* Show the operation content by default */
            .swagger-ui .opblock .opblock-summary + div {{
                display: block !important;
                padding: 15px;
            }}

            /* Style the Execute button */
            .swagger-ui .execute-wrapper {{
                margin-top: 15px;
            }}

            .swagger-ui .execute-wrapper button {{
                background: #2c5282 !important;
                border-color: #2c5282 !important;
                color: white !important;
                padding: 8px 20px !important;
                border-radius: 4px !important;
                font-weight: bold !important;
            }}

            .swagger-ui .execute-wrapper button:hover {{
                background: #1a365d !important;
                border-color: #1a365d !important;
            }}

            /* Style the parameters section */
            .swagger-ui .parameters-container {{
                margin: 15px 0;
            }}

            .swagger-ui .parameters-container .parameters {{
                margin: 0;
                padding: 0;
            }}

            .swagger-ui .parameters-container .parameter {{
                margin: 0 0 10px;
                padding: 10px;
                border: 1px solid #e8e8e8;
                border-radius: 4px;
            }}

            /* Style the response section */
            .swagger-ui .responses-wrapper {{
                margin-top: 15px;
            }}

            .swagger-ui .responses-table {{
                margin: 0;
            }}

            .swagger-ui .responses-table .response {{
                padding: 10px;
                border: 1px solid #e8e8e8;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div id="custom-navbar">
            <h1>InsightWires API Documentation</h1>
        </div>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = function() {{
                window.ui = SwaggerUIBundle({{
                    url: '{app.openapi_url}',
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout",
                    deepLinking: true,
                    displayOperationId: false,
                    docExpansion: "list",
                    defaultModelsExpandDepth: -1,
                    defaultModelExpandDepth: 1,
                    showExtensions: false,
                    showCommonExtensions: false,
                    supportedSubmitMethods: ["get", "post", "put", "delete", "patch"],
                    tryItOutEnabled: true,
                    onComplete: function() {{
                        // Auto-expand all operations
                        document.querySelectorAll('.opblock').forEach(function(opblock) {{
                            opblock.classList.add('is-open');
                            // Enable try it out by default
                            const tryOutBtn = opblock.querySelector('.try-out');
                            if (tryOutBtn) {{
                                tryOutBtn.click();
                            }}
                        }});
                    }}
                }})
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news_router, prefix=settings.API_V1_STR)
app.include_router(business_activity_router, prefix=settings.API_V1_STR)
app.include_router(companies_router, prefix=settings.API_V1_STR)
app.include_router(industries_router, prefix=settings.API_V1_STR)
app.include_router(languages_router, prefix=settings.API_V1_STR)
app.include_router(countries_router, prefix=settings.API_V1_STR)
app.include_router(sources_router, prefix=settings.API_V1_STR)
app.include_router(themes_router, prefix=settings.API_V1_STR)
app.include_router(topics_router, prefix=settings.API_V1_STR)
app.include_router(custom_topics_router, prefix=settings.API_V1_STR)
app.include_router(content_type_router, prefix=settings.API_V1_STR)
app.include_router(sentiments_router, prefix=settings.API_V1_STR)

# Add a landing page
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>InsightWires API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background-color: #f7fafc;
                }
                .container {
                    text-align: center;
                    padding: 20px;
                }
                h1 {
                    color: #1a365d;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #2c5282;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin-top: 20px;
                }
                .button:hover {
                    background-color: #1a365d;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to InsightWires API</h1>
                <p>Access our comprehensive news and company data analytics.</p>
                <a href="/docs" class="button">View API Documentation</a>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)