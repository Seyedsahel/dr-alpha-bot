
### Bot

```
GET    /api/reminders/<user_id>

POST   /api/reminders
```

چون کاربر فقط Reminderهای خودش را می‌بیند و فقط می‌تواند Reminder جدید بسازد.

---

### Admin

```
GET    /api/admin/reminders

PATCH  /api/admin/reminders/<id>
```

PATCH هم فقط برای زمانی است که بعداً Scheduler پیام را ارسال کرد و خواست `sent=True` کند (یا اگر ادمین بخواهد دستی تغییر دهد).

---

## سناریوی POST

ربات این را ارسال می‌کند:

```json
{
    "user_id": 1,
    "service_id": 2,
    "procedure_date": "2026-06-26"
}
```

سرور این کارها را انجام می‌دهد:

1. بررسی کند user وجود دارد.
    
2. بررسی کند service وجود دارد.
    
3. `recovery_days` سرویس را بخواند.
    
4. محاسبه کند:
    

```
repair_date = procedure_date + recovery_days
```

5. محاسبه کند:
    

```
reminder_date = repair_date - 3 days
```

6. Reminder را ذخیره کند.
    
7. خروجی برگرداند.
    

به نظرم خروجی بهتر است این باشد:

```json
{
    "message": "reminder created",
    "reminder_id": 1,
    "repair_date": "2026-12-23",
    "reminder_date": "2026-12-20"
}
```

چون ربات بلافاصله می‌تواند به کاربر نمایش دهد:

> زمان تقریبی ترمیم شما: ۲۳ آذر  
> سه روز قبل از آن برایتان یادآوری ارسال خواهد شد.

---

## سناریوی GET

```
GET /api/reminders/<user_id>
```

خروجی:

```json
[
    {
        "id": 1,
        "service_id": 2,
        "service_name": "بوتاکس کامل صورت",
        "procedure_date": "2026-06-26",
        "reminder_date": "2026-12-20",
        "sent": false
    }
]
```

اینجا از Relationship استفاده می‌کنیم:

```python
reminder.service.name
```

---

### ترتیب پیاده‌سازی

پیشنهاد می‌کنم دقیقاً به این ترتیب جلو برویم:

1. `POST /api/reminders` (اصلی‌ترین بخش و شامل منطق محاسبه)
    
2. تست با `curl`
    
3. `GET /api/reminders/<user_id>`
    
4. تست با `curl`
    
5. بعد برویم سراغ APIهای ادمین (`GET` و `PATCH`).
    

این ترتیب باعث می‌شود هر مرحله را مستقل تست کنیم و اگر مشکلی بود، سریع محل آن را پیدا کنیم.


---
عالی. از آنجایی که تا الان همه Routeهایت یک سبک مشخص دارند، همان سبک را حفظ می‌کنیم.

قبل از کدنویسی، منطق Endpoint را مشخص کنیم.

---

## POST /api/reminders

### Request

```json
{
    "user_id": 1,
    "service_id": 2,
    "procedure_date": "2026-06-26"
}
```

---

## مراحل داخل API

### ۱. دریافت داده‌ها

```python
data = request.get_json()
```

---

### ۲. اعتبارسنجی

وجود این سه فیلد:

- user_id
    
- service_id
    
- procedure_date
    

اگر یکی نبود:

```json
{
    "error": "user_id, service_id and procedure_date are required"
}
```

---

### ۳. بررسی وجود User

```python
User.query.get(user_id)
```

اگر نبود:

```json
{
    "error": "user not found"
}
```

---

### ۴. بررسی وجود Service

```python
Service.query.get(service_id)
```

اگر نبود:

```json
{
    "error": "service not found"
}
```

---

### ۵. بررسی recovery_days

اگر سرویس recovery_days نداشت:

```json
{
    "error": "service recovery days not set"
}
```

---

### ۶. تبدیل تاریخ

از

```text
2026-06-26
```

به

```python
datetime.date
```

اگر فرمت اشتباه بود:

```json
{
    "error": "invalid date format"
}
```

---

### ۷. محاسبه

```
repair_date
=
procedure_date
+
recovery_days
```

بعد

```
reminder_date
=
repair_date
-
3 روز
```

---

### ۸. ساخت Reminder

```
user_id
service_id
procedure_date
reminder_date
```

---

### ۹. Commit

---

### ۱۰. Response

من این خروجی را پیشنهاد می‌کنم:

```json
{
    "message": "reminder created",
    "reminder_id": 1,
    "repair_date": "2026-12-23",
    "reminder_date": "2026-12-20"
}
```

---

## فقط یک پیشنهاد برای جلوگیری از باگ آینده

الان هر کاربر می‌تواند برای یک سرویس، بی‌نهایت Reminder ثبت کند.

مثلاً:

```
بوتاکس
۱۴۰۵/۰۱/۰۱

بوتاکس
۱۴۰۵/۰۱/۰۲

بوتاکس
۱۴۰۵/۰۱/۰۳
```

اگر این رفتار را نمی‌خواهی، قبل از ساخت Reminder این را چک کن:

```python
Reminder.query.filter_by(
    user_id=user_id,
    service_id=service_id,
    sent=False
).first()
```

اگر پیدا شد:

```json
{
    "error": "active reminder already exists"
}
```

این باعث می‌شود هر کاربر فقط یک یادآوری فعال برای هر سرویس داشته باشد و تجربه کاربری هم منطقی‌تر باشد.

---
