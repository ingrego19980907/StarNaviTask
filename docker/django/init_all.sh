while !</dev/tcp/db_star_navi/5432; do sleep 1; done;
sleep 3;

python manage.py migrate;
python manage.py migrate --noinput;
