from application.routes.auth import create_teacher
def register_commands(app):
    app.cli.add_command(create_teacher)