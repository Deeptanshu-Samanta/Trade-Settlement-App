                    REGISTER
                       │
                       ↓
              POST /auth/register
                       │
                       ↓
                  UserCreate
                       │
                       ↓
                  auth.py
                       │
                       ↓
              auth_service.py
                       │
                 bcrypt hash
                       │
                       ↓
                  User Model
                       │
                       ↓
                  PostgreSQL










                     LOGIN
                       │
                       ↓
               POST /auth/login
                       │
                       ↓
                 LoginRequest
                       │
                       ↓
                  auth.py
                       │
                       ↓
              auth_service.py
                       │
              ┌────────┴────────┐
              ↓                 ↓
          Find User       Verify password
              │                 │
              └────────┬────────┘
                       ↓
                  create JWT
                       │
                       ↓
                 TokenResponse