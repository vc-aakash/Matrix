- Extract and navigate to directory
- Install dependencies:
    `pip install -r requirements.txt`

- Generate NASA Data api-key
- Add api-key to environment:
    - Windows:
        - `Win + S` and search "Environment Variables"
        - Select "Edit the system environment variables"
        - Select "Environment Variables -> "New" under "User variables"
        - Add new variable:
            Variable name: `NASA_API_KEY`
            Variable value: `<api-key>`
        - Restart terminal/IDE
    - macOS/Linux:
        - add to `~/.bashrc`
    ```
    > echo 'export YOUR_API_KEY="your_actual_key_here"' >> ~/.bashrc
    > source ~/.bashrc
    ```