# NDC Lookup Tool (Web Version)

## For End Users

### How to Use
1. **Download** this folder to your computer.
2. **Double-click** the `run_app.bat` file (Windows) or `run_app.sh` (Mac) to start the app.
3. Your web browser will open automatically. If not, go to [http://localhost:8501](http://localhost:8501) in your browser.
4. **Upload** your `.out` file using the uploader.
5. **Enter** an NDC code and click **Search** to view results.

*No technical knowledge required!*

---

## For App Maintainers / Setup

### 1. Install Python (if not already installed)
- Download from [python.org](https://www.python.org/downloads/).
- During install, check "Add Python to PATH".

### 2. Install Streamlit and pandas
```sh
pip install streamlit pandas
```

### 3. Run the App
- On Windows:
  ```sh
  streamlit run app.py
  ```
- On Mac/Linux:
  ```sh
  streamlit run app.py
  ```

### 4. (Optional) Create a one-click launcher
- For Windows: see `run_app.bat`
- For Mac: see `run_app.sh`

---

## Troubleshooting
- If you see an error about missing packages, run `pip install streamlit pandas` again.
- If the app doesn't open, check your firewall or try a different browser.
- For help, contact the app maintainer. 