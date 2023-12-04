cd /Users/alpakafred/Coding/KontenKlaerer
source venv/bin/activate
cd KontenKlaerer
python3 manage.py runserver &
sleep 5
open http://127.0.0.1:8000/
exit