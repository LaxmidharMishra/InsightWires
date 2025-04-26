import os

def setup_directories():
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

def create_custom_css():
    css_content = """
    /* Custom theme colors */
    :root {
        --primary-color: #1a365d;
        --secondary-color: #2c5282;
        --success-color: #38a169;
    }

    /* Header styling */
    .swagger-ui .topbar {
        background-color: var(--primary-color);
        padding: 15px;
    }

    .swagger-ui .info .title {
        color: var(--primary-color);
        font-size: 36px;
    }

    /* Endpoint styling */
    .swagger-ui .opblock.opblock-get {
        border-color: var(--secondary-color);
    }

    .swagger-ui .opblock.opblock-get .opblock-summary-method {
        background-color: var(--secondary-color);
    }

    .swagger-ui .opblock.opblock-post {
        border-color: var(--success-color);
    }

    .swagger-ui .opblock.opblock-post .opblock-summary-method {
        background-color: var(--success-color);
    }

    /* Button styling */
    .swagger-ui .btn.execute {
        background-color: var(--secondary-color);
        border-color: var(--secondary-color);
    }

    .swagger-ui .btn.execute:hover {
        background-color: var(--primary-color);
    }

    /* Custom navbar */
    #custom-navbar {
        background-color: var(--primary-color);
        color: white;
        padding: 1rem;
        margin-bottom: 20px;
    }

    #custom-navbar h1 {
        margin: 0;
        font-size: 24px;
    }

    /* Documentation sections */
    .swagger-ui .opblock-tag {
        color: var(--primary-color);
        font-size: 24px;
    }

    /* Response sections */
    .swagger-ui table tbody tr td {
        padding: 10px;
    }

    /* Schema styling */
    .swagger-ui .model-box {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 4px;
    }

    /* Authentication section */
    .swagger-ui .auth-wrapper {
        display: flex;
        padding: 10px;
        background-color: #e2e8f0;
        border-radius: 4px;
        margin: 10px 0;
    }

    /* Description styling */
    .swagger-ui .info .description {
        font-size: 16px;
        line-height: 1.6;
        margin: 20px 0;
    }

    /* Try it out section */
    .swagger-ui .try-out {
        margin-top: 10px;
    }

    .swagger-ui .try-out__btn {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 4px;
    }

    /* Parameters section */
    .swagger-ui .parameters-col_description {
        margin: 5px 0;
    }

    .swagger-ui .parameters-col_description input {
        padding: 5px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    /* Response section */
    .swagger-ui .responses-inner {
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 4px;
    }

    .swagger-ui .response-col_status {
        color: var(--primary-color);
        font-weight: bold;
    }
    """
    
    with open('static/custom.css', 'w') as f:
        f.write(css_content)

def setup_static_files():
    setup_directories()
    create_custom_css()
    print("Documentation setup completed successfully!")

# Run the setup
if __name__ == "__main__":
    setup_static_files()