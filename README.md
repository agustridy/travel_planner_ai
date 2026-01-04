# 🤖 Travel Planner AI - FastAPI + LLM + Maps

Aplikasi web cerdas untuk merencanakan perjalanan wisata secara otomatis menggunakan kecerdasan buatan dan integrasi peta interaktif.

[![Tonton di YouTube](https://img.youtube.com/vi/kVp6oC8AxCA/0.jpg)](https://www.youtube.com/watch?v=kVp6oC8AxCA)

## 🎯 Fitur Utama

- **AI-Powered Recommendations**: Generate rencana perjalanan otomatis menggunakan Deepseek LLM
- **Interactive Maps**: Visualisasi peta dengan Leaflet.js dan OpenStreetMap
- **Smart Routing**: Rute optimal berdasarkan lokasi dan preferensi
- **Budget Planning**: Rekomendasi sesuai budget (rendah, menengah, tinggi)
- **Category Filtering**: Filter destinasi berdasarkan minat (sejarah, kuliner, alam, dll)
- **Real-time Geocoding**: Konversi nama lokasi ke koordinat GPS
- **Responsive Design**: Tampilan yang optimal di desktop dan mobile

## 🛠️ Teknologi yang Digunakan

### Backend
- **FastAPI** - Framework web modern dan cepat
- **Python 3.8+** - Bahasa pemrograman utama
- **Deepseek API** - Model LLM untuk rekomendasi cerdas
- **Pydantic** - Validasi data dan serialisasi
- **httpx** - HTTP client async
- **uvicorn** - ASGI server

### Frontend
- **HTML5/CSS3** - Struktur dan styling
- **JavaScript (ES6+)** - Logika client-side
- **Leaflet.js** - Library peta interaktif
- **OpenStreetMap** - Tiles peta gratis

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/travel-planner-ai.git
cd travel-planner-ai
```

### 2. Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pydantic anthropic httpx python-dotenv
```

### 4. Konfigurasi Environment Variables
Buat file `.env` di root folder:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 5. Dapatkan API Key
1. Daftar di [Deepseek Platform](https://platform.deepseek.com/)
2. Buat API key baru
3. Copy ke file `.env`

## 🚀 Cara Menjalankan

### Backend Server
```bash
python main.py
```
Server akan berjalan di `http://localhost:8080`

### Frontend
1. Buka file `frontend/index.html` di browser
2. Atau gunakan live server extension di VS Code

## 📖 Cara Penggunaan

### 1. Input Preferensi
- Masukkan **kota tujuan** (contoh: Yogyakarta, Bali, Jakarta)
- Pilih **minat** (sejarah, kuliner, alam, belanja, religi, seni)
- Tentukan **durasi** (1-14 hari)
- Pilih **budget** (rendah, menengah, tinggi)

### 2. Generate Rencana
- Klik tombol **"Generate Rencana Perjalanan"**
- Tunggu AI memproses (5-10 detik)

### 3. Hasil yang Didapat
- **Daftar destinasi** dengan deskripsi lengkap
- **Peta interaktif** dengan marker dan rute
- **Ringkasan perjalanan** (total waktu, jarak, budget)
- **Tips praktis** untuk setiap destinasi

## 🔧 API Endpoints

### `POST /api/plan`
Generate travel plan berdasarkan preferensi
```json
{
  "city": "Yogyakarta",
  "interests": ["sejarah", "kuliner"],
  "duration": 3,
  "budget": "menengah"
}
```

### `GET /api/geocode?location={nama_lokasi}`
Konversi nama lokasi ke koordinat
```json
{
  "lat": -7.7956,
  "lon": 110.3695
}
```

## 🚀 Deployment

### Backend (FastAPI)
- **Railway**: `railway up`
- **Render**: Deploy dari GitHub
- **PythonAnywhere**: Upload file Python
- **Docker**: Build image dan deploy ke cloud

### Frontend (Static)
- **GitHub Pages**: Gratis untuk static site
- **Netlify**: Drag & drop deployment
- **Vercel**: Optimized for frontend
- **Cloudflare Pages**: Global CDN

## 🔧 Development

### Struktur Proyek
```
travel-planner-ai/
├── main.py              # Backend FastAPI
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html      # Frontend HTML/CSS/JS
└── README.md           # Dokumentasi
```

## Support Me
[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=agustridy&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/agustridy)

## 🙏 Credits

- **OpenStreetMap** untuk tiles peta gratis
- **Deepseek** untuk API LLM yang affordable
- **FastAPI** untuk framework backend yang powerful
- **Leaflet.js** untuk library peta yang ringan

---

**⭐ Jika proyek ini membantu, jangan lupa beri star di GitHub!**
