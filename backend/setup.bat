@echo off
echo [1/5] 가상환경 생성 중...
python -m venv venv
call venv\Scripts\activate

echo [2/5] 패키지 설치 중...
pip install -r requirements.txt

echo [3/5] 마이그레이션 실행 중...
python manage.py makemigrations accounts
python manage.py makemigrations cards
python manage.py makemigrations surveys
python manage.py migrate

echo [4/5] 샘플 데이터 로드 중...
python manage.py loaddata fixtures/cards.json
python manage.py loaddata fixtures/card_benefits.json

echo [5/5] 완료!
echo.
echo 슈퍼유저 생성: python manage.py createsuperuser
echo 서버 실행:     python manage.py runserver
pause
