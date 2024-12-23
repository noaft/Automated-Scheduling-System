# Project Setup and Running Instructions

## Prerequisites

Ensure you have Python installed on your system and `pip` for managing packages. Follow these steps to set up and run the application.

## Installation

1. **Clone the repository** (if applicable) and navigate to the project directory.

2. **Install dependencies** using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
    ```
3. **Run with ubuntu**:
You need navigate to the application directory:
   ```bash
   cd path/to/your/app
   ```
Run the FastAPI application:
    ```bash
   python3 -m uvicorn main:app --reload
   ```

Make sure to replace `path/to/your/app` with the actual path to your application directory.
