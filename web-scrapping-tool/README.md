# Generate env file

```sh
    bash local-setup/generate_env.sh
```

# Local Setup

```
    docker-compose up --build
```

The application should be available at http://localhost:8000/api/1/swagger/index.html

To be able to setup run this app in debugger mode in VScode, the python interpretor needs to be setup correctly.

Use these steps to do so:

- Run `poetry install` to install packages
- Run `poetry env info --path` to get the path for the virtual environment created by poetry
- Set the intrepretor to the path outputted from above. To set this up, `View -> Command Pallete -> Python: Select Interpreter`.
- Run the project using debugger