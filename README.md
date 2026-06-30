<div align="center">

# 🔍 Lost & Found — AI-Powered Item Matching System

**Reunite lost items with their owners using computer vision, semantic search, and smart matching.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00BFFF?logo=yolo&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-17%20passed-brightgreen?logo=pytest)](tests/)

</div>

---

## 📖 Overview

**Lost & Found** is a full-stack web application that uses a multi-signal AI pipeline to automatically match lost items with found items. Instead of relying on keyword search alone, the system analyzes uploaded photos using object detection, semantic embeddings, perceptual hashing, keypoint geometry, and GPS location — producing ranked match scores with full transparency.

When both parties confirm a match, contact details are revealed, protecting user privacy until the last moment.

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🤖 **AI Image Matching** | Multi-signal pipeline combining CLIP, pHash, ORB, and location scoring |
| 📸 **Smart Image Upload** | Up to 6 images per item; drag-and-drop, gallery, or direct camera capture |
| 🔐 **Privacy by Design** | Contact info hidden until both parties confirm a mutual match |
| 🔔 **Notifications** | In-app alerts when matches are found or confirmed |
| 🗺️ **Location Filtering** | GPS metadata extraction + manual radius-based proximity search |
| 🧾 **JWT Auth** | Secure user registration, login, and token-based auth |
| ⚡ **Async Backend** | Fully async FastAPI + aiosqlite stack for high throughput |
| 📱 **Responsive UI** | Works on desktop and mobile with drag-and-drop support |

---

## 🧠 AI Matching Pipeline

The core matching engine runs a **4-stage pipeline** for every query:

```
┌────────────────────────────────────────────────────────────┐
│  STAGE 1 — Metadata Filtering                              │
│  ✔ Same item category   ✔ Location within radius          │
│  ✔ Within time window   ✔ Opposite lost/found status      │
└────────────────────┬───────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────────────────────┐
│  STAGE 2 — Vector Similarity Search (CLIP Embeddings)     │
│  Model: OpenCLIP ViT-B/32                                  │
│  Metric: Cosine similarity — Top 50 candidates returned    │
└────────────────────┬───────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────────────────────┐
│  STAGE 3 — Multi-Signal Re-ranking                         │
│  • CLIP vector similarity    40% weight                    │
│  • Perceptual hash (pHash)   25% weight                    │
│  • ORB keypoint geometry     20% weight                    │
│  • Location proximity         15% weight                   │
└────────────────────┬───────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────────────────────┐
│  STAGE 4 — Final Output                                    │
│  Top 10 matches with composite score + breakdown           │
└────────────────────────────────────────────────────────────┘
```

### Signals Explained

| Signal | Technology | Purpose |
|---|---|---|
| **Semantic Embedding** | OpenCLIP ViT-B/32 | Captures visual meaning and object identity |
| **Perceptual Hash** | pHash / dHash / aHash | Detects visual similarity, color, and structure |
| **Keypoint Matching** | ORB (OpenCV) | Finds geometric correspondences between images |
| **Object Detection** | YOLOv8n | Auto-crops the primary object in a photo |
| **GPS / EXIF** | Pillow + custom parser | Extracts location metadata from photos |

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology |
|---|---|
| Web Framework | FastAPI 0.104 |
| Database | SQLite + SQLAlchemy 2.0 (async) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Validation | Pydantic v2 |
| Rate Limiting | SlowAPI |

### AI / ML
| Model | Version | Role |
|---|---|---|
| YOLOv8n | Ultralytics 8.0 | Object detection & cropping |
| OpenCLIP | ViT-B/32 | Semantic image embeddings |
| ImageHash | 4.3 | Perceptual hash comparison |
| OpenCV | 4.8 | ORB keypoint extraction |

### Frontend
- Vanilla HTML5, CSS3, JavaScript (no frameworks)
- Responsive layout with camera capture + drag-and-drop upload
- Served directly from FastAPI as static files

---

## 📁 Project Structure

```
lost-and-found/
├── app/
│   ├── main.py                    # FastAPI entry point, lifespan, middleware
│   ├── config.py                  # Settings via pydantic-settings
│   ├── api/
│   │   ├── deps.py                # Auth and DB dependency injection
│   │   └── routes/
│   │       ├── auth.py            # Login → JWT
│   │       ├── users.py           # Register / profile / delete
│   │       ├── items.py           # CRUD + image upload + match trigger
│   │       ├── matches.py         # Confirm / reject matches
│   │       └── notifications.py   # In-app notification management
│   ├── db/
│   │   └── database.py            # Async engine, session factory, init_db
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── image.py
│   │   ├── embedding.py
│   │   ├── match.py
│   │   └── notification.py
│   ├── schemas/                   # Pydantic request/response schemas
│   ├── services/
│   │   ├── auth.py                # Token creation and verification
│   │   ├── storage.py             # Local file storage service
│   │   ├── image_processing.py    # YOLO + CLIP + pHash + ORB pipeline
│   │   ├── matching.py            # Multi-signal matching engine
│   │   └── notification.py        # Notification dispatch
│   └── middleware/
│       └── security.py            # Rate limiting, sanitization, security headers
├── frontend/                      # Vanilla JS/HTML/CSS frontend
│   ├── index.html
│   ├── report.html
│   ├── my-items.html
│   ├── browse.html
│   ├── login.html
│   ├── register.html
│   └── styles.css
├── tests/
│   ├── conftest.py                # Pytest fixtures + SQLite test DB config
│   └── test_api.py                # 17 API endpoint tests
├── alembic/                       # DB migration scripts
├── data/                          # SQLite DB + uploaded files (auto-created)
├── .env.example                   # Environment variables template
├── requirements.txt
└── yolov8n.pt                     # Pre-downloaded YOLOv8 model weights
```

---

## 🚀 Quick Start

### Prerequisites

- [Anaconda / Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended)
- Python 3.10+
- *(Optional)* CUDA-capable GPU for faster ML inference

---

### 1. Clone the Repository

```bash
git clone https://github.com/FuricBond/Lost-And-Found.git
cd Lost-And-Found
```

### 2. Create & Activate the Conda Environment

```bash
conda create -n lost_found_env python=3.10 -y
conda activate lost_found_env
```

> **Windows users**: Use Anaconda Prompt or Windows PowerShell with Conda initialized.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> This installs PyTorch, YOLOv8, OpenCLIP, FastAPI, and all other dependencies (~2–5 min depending on internet speed).

### 4. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and configure the key values:

```env
# Required
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production

# Database (auto-created on first run)
DATABASE_PATH=./data/lostfound.db

# File uploads
UPLOAD_DIR=./data/uploads
MAX_IMAGE_SIZE_MB=10

# Matching
DEFAULT_SEARCH_RADIUS_KM=50
DEFAULT_TIME_RANGE_DAYS=30

# App
DEBUG=True
ENVIRONMENT=development
```

### 5. Run the Server

```bash
conda activate lost_found_env
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Open the Application

| URL | Description |
|---|---|
| http://localhost:8000 | Web frontend |
| http://localhost:8000/docs | Interactive API docs (Swagger UI) |
| http://localhost:8000/redoc | Alternative API docs (ReDoc) |
| http://localhost:8000/health | Health check endpoint |

---

## 📱 How to Use

### Report a Lost or Found Item

1. Go to **Report Item** and choose *"I Lost Something"* or *"I Found Something"*
2. Fill in: **category**, **title**, **description**, **location**, and **date**
3. Upload up to **6 photos** via drag-and-drop, file picker, or direct camera capture
4. Submit — the AI pipeline processes your images in the background

### Find Matches

1. Go to **My Items** and click **Find Matches**
2. Tune the search parameters:
   - 📍 **Radius** — geographic search range (km)
   - 📅 **Time Range** — days before/after the incident
   - 🎯 **Min Score** — match confidence threshold (0–1)
3. Review ranked matches with score breakdowns

### Confirm a Match

1. Both users independently click **Confirm Match**
2. Upon mutual confirmation, contact details are revealed
3. Coordinate item return directly!

---

## 📡 API Reference

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/login` | Login and receive JWT access token |

### Users
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/users` | Register a new user |
| `GET` | `/api/v1/users/me` | Get current user profile |
| `PATCH` | `/api/v1/users/me` | Update profile |
| `DELETE` | `/api/v1/users/me` | Delete account |

### Items
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/items` | Create a new lost/found item |
| `GET` | `/api/v1/items` | List your items |
| `GET` | `/api/v1/items/{id}` | Get item details |
| `PATCH` | `/api/v1/items/{id}` | Update item |
| `DELETE` | `/api/v1/items/{id}` | Delete item |
| `POST` | `/api/v1/items/{id}/images` | Upload an image |
| `GET` | `/api/v1/items/{id}/images` | List item images |
| `DELETE` | `/api/v1/items/{id}/images/{image_id}` | Delete image |
| `GET` | `/api/v1/items/{id}/matches` | Run the matching pipeline |

### Matches
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/matches` | List all your matches |
| `GET` | `/api/v1/matches/{id}` | Match details |
| `POST` | `/api/v1/matches/{id}/confirm` | Confirm a match |
| `POST` | `/api/v1/matches/{id}/reject` | Reject a match |

### Notifications
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/notifications` | List notifications |
| `POST` | `/api/v1/notifications/mark-read` | Mark specific notifications read |
| `POST` | `/api/v1/notifications/mark-all-read` | Mark all as read |
| `DELETE` | `/api/v1/notifications/{id}` | Delete notification |

---

## 🔒 Security

- **JWT Authentication** — stateless token-based auth with configurable expiry
- **bcrypt Password Hashing** — industry-standard secure storage
- **Rate Limiting** — 100 requests/minute per IP (configurable)
- **Input Sanitization** — middleware strips dangerous inputs
- **Security Headers** — HSTS, CSP, X-Frame-Options, and more
- **File Validation** — type and size checks on all uploads
- **Privacy Guard** — contact info hidden until mutual match confirmation

---

## ⚙️ Configuration Reference

| Variable | Description | Default |
|---|---|---|
| `JWT_SECRET_KEY` | Secret key for JWT signing | **Required** |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `1440` (24h) |
| `DATABASE_PATH` | Path to SQLite database file | `./data/lostfound.db` |
| `UPLOAD_DIR` | Image storage directory | `./data/uploads` |
| `MAX_IMAGE_SIZE_MB` | Max upload file size | `10` |
| `YOLO_MODEL_PATH` | Path to YOLO weights file | `yolov8n.pt` |
| `CLIP_MODEL_NAME` | OpenCLIP model identifier | `ViT-B/32` |
| `DEFAULT_SEARCH_RADIUS_KM` | Default match search radius | `50` |
| `DEFAULT_TIME_RANGE_DAYS` | Default time window for matching | `30` |
| `VECTOR_SIMILARITY_THRESHOLD` | Minimum match score | `0.7` |
| `TOP_K_VECTOR_RESULTS` | Candidates from vector search | `50` |
| `FINAL_TOP_K_MATCHES` | Final matches returned | `10` |
| `RATE_LIMIT_REQUESTS` | Max requests per window | `100` |
| `RATE_LIMIT_PERIOD` | Rate limit window (seconds) | `60` |
| `DEBUG` | Enable debug mode + API docs | `True` |
| `ENVIRONMENT` | Runtime environment | `development` |

---

## 🧪 Development & Testing

### Run the Test Suite

```bash
conda activate lost_found_env
pytest tests/ -v
```

Expected output: **17 passed** covering health checks, user registration/auth, full item CRUD, and notification endpoints.

### Reset the Database

```bash
# Windows
del data\lostfound.db

# macOS / Linux
rm data/lostfound.db

# Restart server — tables are auto-recreated
python -m uvicorn app.main:app --reload
```

### Upload Storage Layout

```
data/uploads/
└── items/
    └── {item_id}/
        └── images/
            └── {image_id}/
                ├── original.jpg    ← raw upload
                ├── processed.jpg   ← YOLO-cropped version
                └── thumbnail.jpg   ← 256px thumbnail
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and add tests where applicable
4. **Run the test suite**: `pytest tests/ -v`
5. **Commit**: `git commit -m "feat: describe your change"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

Please follow conventional commits and keep PRs focused.

---

## 📄 License

This project is licensed under the **MIT License** — free for personal and commercial use. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — blazing fast async Python web framework
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) — state-of-the-art object detection
- [OpenCLIP](https://github.com/mlfoundations/open_clip) — open-source CLIP model implementation
- [ImageHash](https://github.com/JohannesBuchner/imagehash) — perceptual image hashing library
- [SQLAlchemy](https://www.sqlalchemy.org/) — powerful async ORM
- [Pydantic](https://docs.pydantic.dev/) — data validation and settings management

---

<div align="center">

Made with ❤️ by [FuricBond](https://github.com/FuricBond)

</div>
