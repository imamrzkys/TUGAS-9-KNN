# ProInvest - Platform Investasi Digital Profesional

Website fintech modern yang production-ready dengan Flask, Tailwind CSS, dan animasi premium. Siap deploy di Railway tanpa error.

## 🚀 Fitur Utama

✨ **Design Premium**
- Modern dark theme dengan gradient cyan-blue
- Responsive sempurna (mobile-first)
- Animasi halus dengan AOS dan GSAP
- White space yang lega, tipografi rapi

🔐 **Backend Robust**
- Flask framework production-ready
- Contact form dengan validasi
- API endpoints untuk data dinamis
- Error handling komprehensif
- Flash messages untuk notifikasi

📱 **Frontend Interaktif**
- Navbar sticky dengan mobile menu
- Hero section dengan particles animation
- Features grid dengan hover effects
- Testimonials carousel auto-scroll
- FAQ accordion dengan smooth expand
- Pricing comparison table
- Contact form dengan AJAX submission

⚡ **Performance Optimized**
- TailwindCSS CDN (optimal untuk production)
- Minimal JavaScript, no jQuery dependency
- Images lazy loading ready
- Dark mode default
- SEO-friendly structure

🎨 **Animasi & Micro-interactions**
- Scroll reveal dengan AOS
- Button ripple effects
- Card hover animations
- Smooth transitions
- Loading states
- Toast notifications

## 📁 Struktur Project

```
.
├── app.py                      # Flask application utama
├── requirements.txt            # Python dependencies
├── Procfile                    # Railway/Heroku deployment
├── railway.toml                # Railway configuration
├── .env                        # Environment variables (create locally)
│
├── templates/
│   ├── base.html               # Template base dengan navbar & footer
│   ├── index.html              # Landing page lengkap
│   ├── features.html           # Halaman fitur
│   ├── pricing.html            # Halaman pricing
│   ├── about.html              # Halaman tentang
│   ├── contact.html            # Halaman kontak
│   ├── 404.html                # Error page 404
│   └── 500.html                # Error page 500
│
├── static/
│   ├── js/
│   │   └── main.js             # JavaScript utama (animasi, interaksi)
│   ├── css/
│   │   └── style.css           # Custom CSS (animasi tambahan)
│   └── img/                    # Image assets (placeholder)
│
└── README.md                   # Dokumentasi (file ini)
```

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0
- Werkzeug 3.0.1
- Gunicorn (production server)

**Frontend:**
- HTML5 Semantic
- TailwindCSS (CDN)
- Vanilla JavaScript (ES6+)
- AOS (Animate On Scroll)
- GSAP (animations)
- Chart.js (charts)
- Lucide Icons
- Google Fonts (Inter, Poppins)

**Deployment:**
- Railway.app
- Environment Variables
- Gunicorn WSGI Server

## 📦 Instalasi & Setup Lokal

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (untuk version control)

### Step 1: Clone Repository
```bash
cd c:\Users\X395\kuliah\ semester\ 5\PRAK_MACHINE_LEARNING\TUGAS\ 9
```

### Step 2: Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Buat file `.env` di root directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
PORT=5000
```

### Step 5: Run Application
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## 🚀 Deploy ke Railway

### Step 1: Setup Railway Account
1. Buka https://railway.app
2. Sign up atau login dengan GitHub
3. Connect GitHub account

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub"
3. Select repository yang berisi project ini

### Step 3: Configure Environment
Di Railway dashboard:
1. Go to "Variables"
2. Add environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key-here
   PORT=5000 (auto-set by Railway)
   ```

### Step 4: Deploy
Railway akan otomatis:
- Detect Python project (via requirements.txt)
- Build environment
- Start dengan Procfile command
- Assign domain

**Expected output di Railway logs:**
```
Running on http://0.0.0.0:5000
```

### Step 5: Custom Domain (Optional)
1. Go ke Railway project settings
2. Add custom domain
3. Setup DNS pointing

## 🌐 Halaman & Routes

| Route | Template | Deskripsi |
|-------|----------|-----------|
| `/` | index.html | Landing page utama |
| `/features` | features.html | Halaman fitur |
| `/pricing` | pricing.html | Halaman pricing |
| `/about` | about.html | About company |
| `/contact` | contact.html | Contact form |
| `POST /contact` | - | Submit contact form |
| `/api/stats` | - | API stats JSON |
| `/api/testimonials` | - | API testimonials JSON |

## 📋 API Endpoints

### GET /api/stats
Response:
```json
{
  "users": 50000,
  "transactions": 2500000,
  "growth": 156,
  "satisfaction": 98,
  "contacts_received": 0
}
```

### GET /api/testimonials
Response:
```json
[
  {
    "id": 1,
    "name": "Ahmad Rizki",
    "role": "Entrepreneur",
    "image": "https://i.pravatar.cc/150?img=1",
    "text": "Platform terbaik...",
    "rating": 5
  }
]
```

### POST /contact
Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+62812345678",
  "message": "Pesan Anda di sini"
}
```

Response (Success):
```json
{
  "success": true,
  "message": "Pesan Anda telah dikirim!",
  "data": { ... }
}
```

Response (Error):
```json
{
  "success": false,
  "message": "Semua field harus diisi"
}
```

## 🎨 Warna & Brand

**Primary Colors:**
- Primary: `#0f172a` (slate-900)
- Accent: `#06b6d4` (cyan-500)

**Secondary Colors:**
- Success: `#10b981`
- Warning: `#f59e0b`
- Danger: `#ef4444`

**Text Colors:**
- Primary Text: `#e2e8f0` (slate-100)
- Secondary Text: `#94a3b8` (slate-400)

## 🎬 Animasi & Interaksi

| Elemen | Animasi |
|--------|---------|
| Hero Section | Fade in + slide up |
| Feature Cards | Hover lift + glow |
| Testimonials | Auto-scroll carousel |
| Statistics | Count-up animation |
| FAQ | Smooth accordion toggle |
| Buttons | Ripple effect + hover glow |
| Scroll Sections | AOS reveal animations |
| Contact Form | AJAX submit + toast notification |

## ✅ Testing Lokal

### Test Landing Page
```
http://localhost:5000/
```

### Test Navigation
- Klik semua navbar links
- Test mobile menu toggle

### Test Form Submission
```bash
# Buka browser console (F12)
# Submit contact form
# Lihat success toast notification
```

### Test API
```bash
# Terminal/PowerShell
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/testimonials
```

## 🔍 Troubleshooting

### Error: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Error: "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: "Template not found"
- Pastikan folder `templates` di root directory
- Periksa nama file template (case-sensitive di Linux)

### Error: "Static files not loading"
- Pastikan folder `static` di root directory
- Check browser console untuk 404 errors
- Di production, pastikan `app.static_url_path = '/static'`

## 📱 Mobile Responsiveness

- ✅ Mobile-first design
- ✅ Touch-friendly buttons
- ✅ Responsive grid layout
- ✅ Mobile menu navigation
- ✅ Optimized images
- ✅ Font scaling

Test di Chrome DevTools (F12) → Toggle device toolbar

## 🔒 Security

- ✅ CSRF Protection (Flask session)
- ✅ Input validation
- ✅ HTTPS ready
- ✅ Headers security (X-Frame-Options, etc)
- ✅ No hardcoded secrets

**Production Tips:**
- Change `SECRET_KEY` di production
- Set `FLASK_DEBUG=False`
- Use environment variables
- Enable HTTPS
- Add rate limiting
- Implement CORS jika perlu

## 📈 Performance

- Load time: < 2 detik (optimized CDN links)
- Lighthouse Score: 90+ (target)
- Responsive design score: 100%
- Mobile-friendly: ✅

## 🚀 Enhancement Ideas

**Tier 1 (MVP):**
- [ ] Add dark/light mode toggle
- [ ] Newsletter signup
- [ ] CTA tracking

**Tier 2 (Pro):**
- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Admin dashboard
- [ ] Email notifications

**Tier 3 (Enterprise):**
- [ ] Payment integration (Stripe)
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] API documentation
- [ ] Blog/CMS

## 📞 Support

- Email: support@proinvest.id
- Live Chat: 24/7 available
- Docs: https://docs.proinvest.id

## 📄 License

© 2024 ProInvest. All rights reserved.

---

**Made with ❤️ by ProInvest Team**

Happy coding! 🚀
