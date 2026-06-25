- Routes:
```
app/

routes/

├── admin/
│   ├── slots.py
│   ├── festivals.py
│
├── bot/
│   ├── slots.py
│   ├── appointments.py
│   ├── consultations.py
│
└── __init__.py

```

- پنل ادمین
```
POST   /api/admin/slots
GET    /api/admin/slots
DELETE /api/admin/slots/<id>

POST   /api/admin/festivals
GET    /api/admin/festivals

GET    /api/admin/appointments
PATCH  /api/admin/appointments/<id>

GET    /api/admin/consultations
PATCH  /api/admin/consultations/<id>
```

- ربات
```
GET    /api/slots

POST   /api/appointments

POST   /api/consultations

GET    /api/festivals

GET    /api/faqs

GET    /api/aftercare
```

-----------


# API های مورد نیاز نسخه 1

## نوبت‌دهی

### ادمین

```
POST   /api/admin/slots
GET    /api/admin/slots
DELETE /api/admin/slots/<id>
```

### ربات

```
GET    /api/slots
POST   /api/appointments
```

---

## مدیریت نوبت‌ها

### ادمین

```
GET    /api/admin/appointments
PATCH  /api/admin/appointments/<id>
```

مثلاً:

```
{  "status":"confirmed"}
```

یا:

```
{  "status":"rejected"}
```

---

## مشاوره تلفنی

### ربات

```
POST /api/consultations
```

### ادمین

```
GET /api/admin/consultations
PATCH /api/admin/consultations/<id>
```

---

## جشنواره‌ها

### ادمین

```
POST   /api/admin/festivals
GET    /api/admin/festivals
PUT    /api/admin/festivals/<id>
DELETE /api/admin/festivals/<id>
```

### ربات

```
GET /api/festivals
```

---

### Service

### API ادمین

```
GET    /api/services
GET    /api/admin/services

POST   /api/admin/services

PATCH  /api/admin/services/<id>

DELETE /api/admin/services/<id>
```

---

### API ربات

```
GET /api/services
```

---

### FAQ

### ادمین

```
POST /api/admin/faqsGET /api/admin/faqsPUT /api/admin/faqs/<id>DELETE /api/admin/faqs/<id>
```

---

### ربات

```
GET /api/faqs
```

---

### AfterCare

### ادمین

```
POST /api/admin/aftercaresGET /api/admin/aftercaresPUT /api/admin/aftercares/<id>DELETE /api/admin/aftercares/<id>
```

---

### ربات

```
GET /api/aftercares
```

یا:

```
GET /api/aftercares/بوتاکس
```

---

