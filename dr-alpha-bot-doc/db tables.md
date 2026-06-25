
### user:
|field|
|---|
|id|
|chat_id|
|first_name|
|last_name|
|phone|
|is_admin|
|created_at|
### appointments:
| field          |
| -------------- |
| id             |
| user_id        |
| service        |
| preferred_date |
| description    |
| status         |
| created_at     |
pending
confirmed
rejected

### consultations
|field|
|---|
|id|
|user_id|
|service|
|note|
|created_at|
### reminders
|field|
|---|
|id|
|user_id|
|service|
|procedure_date|
|reminder_date|
|sent|
|created_at|

### festivals
|field|
|---|
|id|
|title|
|description|
|is_active|
|created_at|

### services
|field|
|---|---|
|id||
|name|بوتاکس|
|price|2200000|
|description|توضیح|
|is_active|فعال|

### FAQ
|field|
|---|
|id|
|question|
|answer|
|is_active|
### aftercares
|field|
|---|
|id|
|service_name|
|content|