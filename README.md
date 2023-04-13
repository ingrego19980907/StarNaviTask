# Принцип роботи API

## User AUTH
| Метод | Endpoint | Опис                      |
|:------|:---------|:--------------------------|
| POST    | /api/auth/signup/ | Створити аккаунт / SignUp |
| POST  | /api/auth/login/ | Login                        |

## Posts
| Метод  | Endpoint                    | Опис             |
|:-------|:----------------------------|:-----------------|
| POST   | /api/post/create/           | Строрити пост    |
| POST   | /api/post/{post_id}/like/   | Лайк   / Like     |
| POST     | /api/post/{post_id}/unlike/ | Анлайк /  Unlike |

## Analytics
| Метод | Endpoint                                                   | Опис                               |
|:------|:-----------------------------------------------------------|:-----------------------------------|
| GET    | /api/analytics/like_count_by_date/?date_from={}&date_to={} | Аналітика створених лайків по даті |
| GET   | /api/analytics/user_activity/                                  | Активність Юзера                   |