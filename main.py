"""
Payroll System - Main Entry Point
Run the Flask web application.
"""
from src import create_app

app = create_app()


def main():
    """Run the Flask development server."""
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()
