from .attendance import attendance_bp
from .auth import auth_bp
from .students import students_bp
from .dashboard import dashboard_bp
from .statistics import statistics_bp
from .auth import create_teacher


blue_prints = [students_bp, dashboard_bp,statistics_bp,auth_bp,attendance_bp]