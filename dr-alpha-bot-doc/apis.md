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