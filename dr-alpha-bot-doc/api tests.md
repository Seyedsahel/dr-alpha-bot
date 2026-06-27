
---

# 1) Services

### Bot

```bash
curl http://localhost:5000/api/services
```

---

### Admin GET

```bash
curl http://localhost:5000/api/admin/services
```

---

### Admin POST

```bash
curl -X POST http://localhost:5000/api/admin/services \
-H "Content-Type: application/json" \
-d '{
    "name":"خدمت تست",
    "price":1500000,
    "description":"توضیحات تست",
    "recovery_days":90
}'
```

---

### Admin PATCH

```bash
curl -X PATCH http://localhost:5000/api/admin/services/1 \
-H "Content-Type: application/json" \
-d '{
    "price":2500000,
    "description":"آپدیت شد",
    "recovery_days":120
}'
```

---

### Admin DELETE

```bash
curl -X DELETE http://localhost:5000/api/admin/services/1
```

---

# 2) FAQs

### Bot

```bash
curl http://localhost:5000/api/faqs
```

---

### Admin GET

```bash
curl http://localhost:5000/api/admin/faqs
```

---

### Admin POST

```bash
curl -X POST http://localhost:5000/api/admin/faqs \
-H "Content-Type: application/json" \
-d '{
    "question":"تست؟",
    "answer":"بله"
}'
```

---

### PATCH

```bash
curl -X PATCH http://localhost:5000/api/admin/faqs/1 \
-H "Content-Type: application/json" \
-d '{
    "answer":"جواب جدید"
}'
```

---

### DELETE

```bash
curl -X DELETE http://localhost:5000/api/admin/faqs/1
```

---

# 3) AfterCare

### Bot List

```bash
curl http://localhost:5000/api/aftercares
```

---

### Bot Single

```bash
curl http://localhost:5000/api/aftercares/1
```

---

### Admin GET

```bash
curl http://localhost:5000/api/admin/aftercares
```

---

### POST

```bash
curl -X POST http://localhost:5000/api/admin/aftercares \
-H "Content-Type: application/json" \
-d '{
    "service_id":2,
    "content":"تا ۴۸ ساعت ورزش نکنید."
}'
```

---

### PATCH

```bash
curl -X PATCH http://localhost:5000/api/admin/aftercares/1 \
-H "Content-Type: application/json" \
-d '{
    "content":"مراقبت جدید"
}'
```

---

### DELETE

```bash
curl -X DELETE http://localhost:5000/api/admin/aftercares/1
```

---

# 4) Festivals

### Bot

```bash
curl http://localhost:5000/api/festivals
```

---

### Admin

```bash
curl http://localhost:5000/api/admin/festivals
```

---

### POST

```bash
curl -X POST http://localhost:5000/api/admin/festivals \
-F "title=جشنواره تابستان" \
-F "description=۳۰ درصد تخفیف" \
-F "image=@/home/mors/Downloads/image.jpg"
```

---

### PATCH

```bash
curl -X PATCH http://localhost:5000/api/admin/festivals/1 \
-F "title=آپدیت جشنواره" \
-F "is_active=true"
```

---

### DELETE

```bash
curl -X DELETE http://localhost:5000/api/admin/festivals/1
```

---

# 5) Available Slots

### Bot

```bash
curl http://localhost:5000/api/slots
```

---

### Admin POST

```bash
curl -X POST http://localhost:5000/api/admin/slots \
-H "Content-Type: application/json" \
-d '{
    "start_time":"2026-08-01 09:00"
}'
```

---

# 6) Appointment

### POST

```bash
curl -X POST http://localhost:5000/api/appointments \
-H "Content-Type: application/json" \
-d '{
    "user_id":1,
    "slot_id":1,
    "service_id":2
}'
```

---

### Admin GET

```bash
curl http://localhost:5000/api/admin/appointments
```

---

### PATCH Status

```bash
curl -X PATCH http://localhost:5000/api/admin/appointments/1 \
-H "Content-Type: application/json" \
-d '{
    "status":"confirmed"
}'
```

---

# 7) Consultation

### POST

```bash
curl -X POST http://localhost:5000/api/consultations \
-H "Content-Type: application/json" \
-d '{
    "user_id":1,
    "message":"مشاوره برای بوتاکس"
}'
```

---

### Admin GET

```bash
curl http://localhost:5000/api/admin/consultations
```

---

### PATCH

```bash
curl -X PATCH http://localhost:5000/api/admin/consultations/1 \
-H "Content-Type: application/json" \
-d '{
    "status":"called"
}'
```

---

# 8) Reminder

### POST

```bash
curl -X POST http://localhost:5000/api/reminders \
-H "Content-Type: application/json" \
-d '{
    "user_id":1,
    "service_id":2,
    "procedure_date":"2026-06-26"
}'
```

---

### Bot GET

```bash
curl http://localhost:5000/api/reminders/1
```

---

### Admin GET List

```bash
curl http://localhost:5000/api/admin/reminders
```

---

### Admin GET One

```bash
curl http://localhost:5000/api/admin/reminders/1
```

---

