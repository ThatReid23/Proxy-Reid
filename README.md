# BrowserProxy

A simple and lightweight web proxy that allows you to browse the web through a proxy server. It's designed to be easy to set up and use, and it comes with a clean web interface to get you started.

## Features

*   **Web Interface**: A modern web interface to start browsing.
*   **URL Rewriting**: Rewrites all URLs to keep you within the proxy.
*   **HTTP and HTTPS Support**: Proxies both HTTP and HTTPS traffic.
*   **JavaScript Rendering**: Optional support for JavaScript-heavy websites using Playwright.
*   **Lightweight**: Minimal resource footprint by default.
*   **Deployable**: Includes a configuration for deploying to Vercel.

## Getting Started

Follow these instructions to get the proxy server up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3**: Download and install from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer (usually comes with Python).

### Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/ryyReid/Reidproxy.git
    cd ReidProxy
    ```

2.  **Install dependencies**:
    The project relies on several Python libraries. Install them using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

### Verifying the Installation

To ensure that all dependencies are installed correctly, you can use the `requirements_install.py` script. This tool will scan your environment and report the status of the required packages.

To run the checker, use the following command:

```bash
python requirements_install.py
```

If any packages are missing, the script will offer to install them for you. This is the recommended way to install the dependencies after the initial setup.

### Running the Application

To start the web proxy server, execute the `app.py` script:

```bash
python app.py
```

This will start two services:

*   A **web interface** running on `http://127.0.0.1:8080`.
*   A **TCP proxy server** running on `http://127.0.0.1:6767`.

You can also use a production-ready WSGI server like `gunicorn`:

```bash
gunicorn app:app
```

## Usage

### Web Interface

Navigate to `http://127.0.0.1:8080` in your web browser. You will see a search bar where you can enter a URL or a search query. The proxy will handle the rest.

### Browser Configuration

To use the proxy directly with your browser (without the web interface), you need to configure your browser's proxy settings.

1.  Open your browser's **Settings**.
2.  Search for **"Proxy"** and open the proxy settings.
3.  Select **"Manual proxy configuration"**.
4.  Enter the following:
    *   **HTTP Proxy**: `127.0.0.1`
    *   **Port**: `6767`
5.  Save your changes.

**Note**: Remember to disable the proxy settings in your browser when you are finished, or you may have trouble connecting to the internet.

## Advanced Usage: JavaScript Rendering with Playwright

For websites that rely heavily on JavaScript, you can enable Playwright for better rendering.

1.  **Install Playwright**:
    ```bash
    pip install playwright
    playwright install
    ```

2.  **Enable Playwright in `app.py`**:
    *   Uncomment the Playwright-related lines in `app.py`.
    *   In the `proxy` function, replace `fetch_with_requests` with `fetch_with_playwright`.

## Deployment

This project is configured for deployment on [Vercel](https://vercel.com/). The `vercel.json` file in the root of the repository contains the necessary configuration.

## Contributing

Contributions are welcome! If you have a suggestion or a bug fix, please open an issue or submit a pull request.

1.  **Fork the repository**.
2.  **Create a new branch**: `git checkout -b feature/YourFeature`.
3.  **Make your changes**.
4.  **Commit your changes**: `git commit -m 'Add some feature'`.
5.  **Push to the branch**: `git push origin feature/YourFeature`.
6.  **Open a pull request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
