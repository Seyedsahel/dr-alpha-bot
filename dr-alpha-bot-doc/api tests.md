

## 1. ساخت Slot

```http
POST /api/admin/slots
```

مثال:

```bash
curl -X POST \
http://127.0.0.1:5000/api/admin/slots \
-H "Content-Type: application/json" \
-d '{
  "start_time":"2026-07-10 10:00"
}'
```

باید:

```json
{
  "message":"slot created",
  "slot_id":1
}
```

برگرده.

---

## 2. مشاهده Slot های آزاد

```http
GET /api/slots
```

```bash
curl http://127.0.0.1:5000/api/slots
```

باید Slot ساخته شده را ببینی.

---

## 3. ساخت Appointment

```http
POST /api/appointments
```

```bash
curl -X POST \
http://127.0.0.1:5000/api/appointments \
-H "Content-Type: application/json" \
-d '{
  "user_id":1,
  "slot_id":1,
  "service":"بوتاکس",
  "description":"اولین مراجعه"
}'
```

باید:

```json
{
  "message":"appointment created",
  "appointment_id":1
}
```

برگرده.

---

## 4. بررسی رزرو شدن Slot

دوباره:

```bash
curl http://127.0.0.1:5000/api/slots
```

باید Slot شماره 1 دیگر در لیست نباشد.

---

## 5. مشاهده Appointment ها توسط ادمین

```http
GET /api/admin/appointments
```

```bash
curl http://127.0.0.1:5000/api/admin/appointments
```

باید چیزی شبیه:

```json
[
  {
    "id":1,
    "name":"علی محمدی",
    "phone":"0912...",
    "service":"بوتاکس",
    "status":"pending",
    "slot_time":"2026-07-10 10:00"
  }
]
```

برگردد.

---

## 6. تایید Appointment

```http
PATCH /api/admin/appointments/1
```

```bash
curl -X PATCH \
http://127.0.0.1:5000/api/admin/appointments/1 \
-H "Content-Type: application/json" \
-d '{
  "status":"confirmed"
}'
```

---

## 7. رد Appointment

```bash
curl -X PATCH \
http://127.0.0.1:5000/api/admin/appointments/1 \
-H "Content-Type: application/json" \
-d '{
  "status":"rejected"
}'
```

بعدش:

```bash
curl http://127.0.0.1:5000/api/slots
```

باید دوباره Slot آزاد شده باشد.

---

## 8. ثبت Consultation

```http
POST /api/consultations
```

```bash
curl -X POST \
http://127.0.0.1:5000/api/consultations \
-H "Content-Type: application/json" \
-d '{
  "user_id":1,
  "service":"ژل لب",
  "note":"درباره ماندگاری سوال دارم"
}'
```

---

## 9. مشاهده Consultation ها

```http
GET /api/admin/consultations
```

```bash
curl http://127.0.0.1:5000/api/admin/consultations
```

---

## 10. تغییر وضعیت Consultation

```bash
curl -X PATCH \
http://127.0.0.1:5000/api/admin/consultations/1 \
-H "Content-Type: application/json" \
-d '{
  "status":"called"
}'
```

---
