# 🎨 YoPuedo360 Design System

## Paleta de Colores

### Colores Principales
| Nombre | Hex | Uso |
|--------|-----|-----|
| **Purple Primary** | `#667eea` | Gradiente inicio, botones, links |
| **Purple Dark** | `#764ba2` | Gradiente fin, hover states |
| **Pink Accent** | `#ec4899` | Acentos, highlights, badges |

### Gradientes
```css
/* Gradiente Principal (botones, fondos) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Gradiente con Pink */
background: linear-gradient(to right, #667eea, #ec4899);

/* Gradiente Success (World page) */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
```

### UI Colors
| Nombre | Hex | Uso |
|--------|-----|-----|
| **White** | `#ffffff` | Cards, fondos |
| **Gray 50** | `#f9fafb` | Inputs, backgrounds |
| **Gray 200** | `#e5e7eb` | Borders |
| **Gray 500** | `#6b7280` | Text secundario |
| **Gray 900** | `#111827` | Text principal |

### Feedback Colors
| Nombre | Hex | Uso |
|--------|-----|-----|
| **Success** | `#10b981` | Correcto, completado |
| **Warning** | `#f59e0b` | Alertas, tips |
| **Error** | `#ef4444` | Errores, validación |

## Estilos

### Cards (Glassmorphism)
```css
.card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}
```

### Buttons
```css
/* Primary */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

/* Secondary */
.btn-secondary {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}
```

### Typography
- **Font**: Inter (Google Fonts) o system fonts
- **Headings**: Bold, text-gray-900
- **Body**: Regular, text-gray-600
- **Links**: text-purple-600, font-semibold

## Emojis de la App
| Concepto | Emoji |
|----------|-------|
| Brain/Learning | 🧠 |
| Memory Palace | 🏰 |
| Goal | 🎯 |
| Languages | 🌍 |
| Progress | 📊 |
| Streak | 🔥 |
| XP/Stars | ⭐ |
| Lessons | 📚 |
| Speaking | 💬 |
| Success | ✅ |
| Welcome | 🚀 |
