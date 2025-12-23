# Hallmarking Center API Contract

**Version:** 1.0  
**Last Updated:** December 23, 2025  
**Status:** Production Ready

This document defines the exact API contract between the Django backend and React frontend. All response shapes have been verified and tested.

---

## Base Configuration

**Backend URL:** `http://localhost:3001`  
**API Base Path:** `/api`  
**Frontend URL:** `http://localhost:3000`  
**Authentication:** Session-based (HTTP-only cookies)  
**Content-Type:** `application/json`  
**CORS:** Enabled for localhost:3000 with credentials

---

## Authentication Endpoints

### 1. User Registration

**Endpoint:** `POST /api/auth/register/`  
**Authentication:** None required  
**CORS:** Public

**Request Body:**
```json
{
  "username": "string (required, unique)",
  "email": "string (required, unique, valid email)",
  "password": "string (required, min 8 chars, must include letters & numbers)",
  "password2": "string (required, must match password)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": "",
    "date_joined": "2025-12-23T20:00:00Z"
  }
}
```

**Error Response (400):**
```json
{
  "username": ["A user with this username already exists."],
  "email": ["A user with this email already exists."],
  "password": ["This password is too common."]
}
```

---

### 2. User Login

**Endpoint:** `POST /api/auth/login/`  
**Authentication:** None required  
**CORS:** Public  
**Side Effect:** Sets `sessionid` HTTP-only cookie

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": "",
    "date_joined": "2025-12-23T20:00:00Z"
  }
}
```

**Session Cookie Set:**
```
Set-Cookie: sessionid=<session_token>; HttpOnly; Path=/; SameSite=Lax
```

**Error Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. User Logout

**Endpoint:** `POST /api/auth/logout/`  
**Authentication:** Required (session cookie)  
**CORS:** Protected  
**Side Effect:** Destroys session

**Request Body:** None

**Success Response (200):**
```json
{
  "message": "Logout successful"
}
```

**Error Response (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Get Current User

**Endpoint:** `GET /api/auth/user/`  
**Authentication:** Required (session cookie)  
**CORS:** Protected

**Request Body:** None

**Success Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "",
  "last_name": "",
  "date_joined": "2025-12-23T20:00:00Z"
}
```

**Error Response (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Center Information Endpoints

### 5. Get Center Information

**Endpoint:** `GET /api/center/`  
**Authentication:** None required  
**CORS:** Public

**Request Body:** None

**Success Response (200):**
```json
{
  "id": 1,
  "name": "Premier Gold Hallmarking Center",
  "description": "Leading hallmarking assay testing center providing certification services for gold jewelry and precious metals with international standards compliance.",
  "address": "123 Gold Street, Jewelry District, Mumbai 400001",
  "contact_email": "contact@premierhallmarking.com",
  "contact_phone": "+91-22-1234-5678"
}
```

**Error Response (404):**
```json
{
  "error": "Center information not found"
}
```

---

## Services Endpoints

### 6. List Services

**Endpoint:** `GET /api/services/`  
**Authentication:** None required  
**CORS:** Public

**Query Parameters:**
- `include_inactive` (boolean, optional): Include inactive services (default: false)

**Request Body:** None

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "Gold Purity Testing",
    "description": "Comprehensive gold purity assessment using advanced XRF technology to determine exact karat value and composition.",
    "price": "500.00",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Hallmark Certification",
    "description": "Official hallmarking certification service with BIS-approved stamps for jewelry items meeting quality standards.",
    "price": "750.00",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Complete Assay Analysis",
    "description": "Full laboratory analysis of precious metal content including trace elements and detailed composition report.",
    "price": "1200.00",
    "is_active": true
  }
]
```

---

### 7. Get Service Details

**Endpoint:** `GET /api/services/{id}/`  
**Authentication:** None required  
**CORS:** Public

**Path Parameters:**
- `id` (integer, required): Service ID

**Request Body:** None

**Success Response (200):**
```json
{
  "id": 1,
  "name": "Gold Purity Testing",
  "description": "Comprehensive gold purity assessment using advanced XRF technology to determine exact karat value and composition.",
  "price": "500.00",
  "is_active": true,
  "certifications": [
    {
      "id": 1,
      "title": "BIS License Certificate",
      "description": "Bureau of Indian Standards authorized hallmarking center license for gold and precious metal testing.",
      "issued_date": "2023-01-15",
      "certificate_number": "BIS-HM-2023-001234",
      "services": [...]
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Service not found"
}
```

---

## Certifications Endpoints

### 8. List Certifications

**Endpoint:** `GET /api/certifications/`  
**Authentication:** None required  
**CORS:** Public

**Request Body:** None

**Success Response (200):**
```json
[
  {
    "id": 1,
    "title": "BIS License Certificate",
    "description": "Bureau of Indian Standards authorized hallmarking center license for gold and precious metal testing.",
    "issued_date": "2023-01-15",
    "certificate_number": "BIS-HM-2023-001234",
    "services": [
      {
        "id": 1,
        "name": "Gold Purity Testing",
        "description": "Comprehensive gold purity assessment using advanced XRF technology to determine exact karat value and composition.",
        "price": "500.00",
        "is_active": true
      },
      {
        "id": 2,
        "name": "Hallmark Certification",
        "description": "Official hallmarking certification service with BIS-approved stamps for jewelry items meeting quality standards.",
        "price": "750.00",
        "is_active": true
      }
    ]
  }
]
```

---

### 9. Get Certification Details

**Endpoint:** `GET /api/certifications/{id}/`  
**Authentication:** None required  
**CORS:** Public

**Path Parameters:**
- `id` (integer, required): Certification ID

**Request Body:** None

**Success Response (200):**
```json
{
  "id": 1,
  "title": "BIS License Certificate",
  "description": "Bureau of Indian Standards authorized hallmarking center license for gold and precious metal testing.",
  "issued_date": "2023-01-15",
  "certificate_number": "BIS-HM-2023-001234",
  "services": [
    {
      "id": 1,
      "name": "Gold Purity Testing",
      "description": "Comprehensive gold purity assessment using advanced XRF technology to determine exact karat value and composition.",
      "price": "500.00",
      "is_active": true
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Certification not found"
}
```

---

## Portfolio Endpoint

### 10. Get Portfolio Data

**Endpoint:** `GET /api/portfolio/`  
**Authentication:** None required  
**CORS:** Public

**Request Body:** None

**Success Response (200):**
```json
{
  "services": [
    {
      "id": 1,
      "name": "Gold Purity Testing",
      "description": "Comprehensive gold purity assessment using advanced XRF technology to determine exact karat value and composition.",
      "price": "500.00",
      "is_active": true
    },
    {
      "id": 2,
      "name": "Hallmark Certification",
      "description": "Official hallmarking certification service with BIS-approved stamps for jewelry items meeting quality standards.",
      "price": "750.00",
      "is_active": true
    },
    {
      "id": 3,
      "name": "Complete Assay Analysis",
      "description": "Full laboratory analysis of precious metal content including trace elements and detailed composition report.",
      "price": "1200.00",
      "is_active": true
    }
  ],
  "certifications": [
    {
      "id": 1,
      "title": "BIS License Certificate",
      "description": "Bureau of Indian Standards authorized hallmarking center license for gold and precious metal testing.",
      "issued_date": "2023-01-15",
      "certificate_number": "BIS-HM-2023-001234",
      "services": [...]
    },
    {
      "id": 2,
      "title": "ISO 9001:2015 Quality Management",
      "description": "International standard certification for quality management systems in testing and certification services.",
      "issued_date": "2023-03-20",
      "certificate_number": "ISO-9001-2023-567890",
      "services": [...]
    },
    {
      "id": 3,
      "title": "NABL Accreditation",
      "description": "National Accreditation Board for Testing and Calibration Laboratories accreditation for precious metal testing.",
      "issued_date": "2023-06-10",
      "certificate_number": "NABL-TC-2023-098765",
      "services": [...]
    }
  ]
}
```

---

## Health Check Endpoint

### 11. Health Check

**Endpoint:** `GET /api/health/`  
**Authentication:** None required  
**CORS:** Public

**Request Body:** None

**Success Response (200):**
```json
{
  "message": "Server is up!"
}
```

---

## CORS Headers

All responses include these CORS headers for requests from http://localhost:3000:

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: DELETE, GET, OPTIONS, PATCH, POST, PUT
Access-Control-Allow-Headers: accept, authorization, content-type, user-agent, x-csrftoken, x-requested-with
Access-Control-Max-Age: 86400
```

---

## Session Authentication

**Cookie Name:** `sessionid`  
**Cookie Attributes:**
- HttpOnly: true
- SameSite: Lax
- Path: /
- Secure: false (true in production)

**Frontend Requirements:**
- Must include `credentials: 'include'` in fetch requests
- Session cookie automatically sent with authenticated requests
- No manual token management required

---

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```
or
```json
{
  "error": "Invalid credentials"
}
```

**404 Not Found:**
```json
{
  "error": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error message"
}
```

---

## Frontend Integration

### API Client Configuration

```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

fetch(`${API_BASE_URL}/endpoint/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
  credentials: 'include', // Required for session cookies
});
```

### Example: Registration Flow

```javascript
import { registerUser } from './services/apiClient';

const handleRegister = async (formData) => {
  const result = await registerUser({
    username: formData.username,
    email: formData.email,
    password: formData.password,
    password2: formData.password2,
  });
  
  if (result.ok) {
    // result.data.message = "User registered successfully"
    // result.data.user = { id, username, email, ... }
  } else {
    // result.error = error message
    // result.data = validation errors object
  }
};
```

### Example: Login Flow

```javascript
import { loginUser } from './services/apiClient';

const handleLogin = async (credentials) => {
  const result = await loginUser({
    username: credentials.username,
    password: credentials.password,
  });
  
  if (result.ok) {
    // Session cookie automatically set
    // result.data.user = { id, username, email, ... }
  }
};
```

---

## Database Schema

### Tables Used

**center_info:**
- id (primary key)
- name
- description
- address
- contact_email
- contact_phone

**services:**
- id (primary key)
- name
- description
- price (decimal)
- is_active (boolean)

**certifications:**
- id (primary key)
- title
- description
- issued_date (date)
- certificate_number

**service_certifications (junction table):**
- service_id (foreign key → services)
- certification_id (foreign key → certifications)

---

## API Documentation URLs

- **Swagger UI:** http://localhost:3001/docs/
- **ReDoc:** http://localhost:3001/redoc/
- **OpenAPI JSON:** http://localhost:3001/swagger.json
- **Local File:** interfaces/openapi.json

---

## Testing

### Test User Accounts

**User 1:**
- Username: testuser1766521270
- Email: test1766521270@example.com
- Password: TestPass123!

**User 2:**
- Username: e2etest1766521388
- Email: e2etest1766521388@example.com
- Password: SecurePass123!

### Quick Test Commands

```bash
# Health check
curl http://localhost:3001/api/health/

# Register user
curl -X POST http://localhost:3001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"TestPass123!","password2":"TestPass123!"}'

# Login
curl -X POST http://localhost:3001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123!"}' \
  -c cookies.txt

# Get current user
curl http://localhost:3001/api/auth/user/ -b cookies.txt

# Get portfolio
curl http://localhost:3001/api/portfolio/
```

---

**Contract Version:** 1.0  
**Last Verified:** December 23, 2025  
**Status:** ✅ Production Ready  
**All Endpoints Tested:** ✅ Yes  
**Response Shapes Verified:** ✅ Yes
