"""
Complete seed - All 25 scenarios from the plan
Run with: python scripts/seed_all_scenarios.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.scenarios.models import Tag, Scenario, Milestone

print("🌱 Seeding ALL 25 scenarios...")

# ============================================
# ENSURE ALL TAGS EXIST
# ============================================

all_tags_data = [
    # Goals (5 consolidated options)
    ('goal', 'work', '💼', 'Trabajo'),
    ('goal', 'travel', '✈️', 'Viajes'),
    ('goal', 'education', '📚', 'Estudios'),
    ('goal', 'personal', '🧠', 'Desarrollo personal'),
    ('goal', 'entertainment', '🎮', 'Entretenimiento'),
    
    # Domains
    ('domain', 'food', '🍽️', 'Comida'),
    ('domain', 'business', '💼', 'Negocios'),
    ('domain', 'health', '🏥', 'Salud'),
    ('domain', 'entertainment', '🎬', 'Entretenimiento'),
    ('domain', 'transport', '🚌', 'Transporte'),
    ('domain', 'accommodation', '🏨', 'Alojamiento'),
    ('domain', 'shopping', '🛒', 'Compras'),
    ('domain', 'social', '👥', 'Social'),
    ('domain', 'education', '🎓', 'Educación'),
    ('domain', 'finance', '🏦', 'Finanzas'),
    ('domain', 'legal', '⚖️', 'Legal'),
    ('domain', 'culture', '🎭', 'Cultura'),
    ('domain', 'literature', '📚', 'Literatura'),
    ('domain', 'technology', '💻', 'Tecnología'),
    ('domain', 'home', '🏠', 'Casa'),
    ('domain', 'news', '📰', 'Noticias'),
    
    # Work domains
    ('work_domain', 'tech', '💻', 'Tecnología'),
    ('work_domain', 'sales', '📊', 'Ventas'),
    ('work_domain', 'health', '⚕️', 'Salud'),
    ('work_domain', 'education', '📚', 'Educación'),
    ('work_domain', 'creative', '🎨', 'Creativo'),
    ('work_domain', 'general', '🔧', 'General'),
    ('work_domain', 'legal', '⚖️', 'Legal'),
    
    # Interests
    ('interest', 'gaming', '🎮', 'Gaming'),
    ('interest', 'music', '🎵', 'Música'),
    ('interest', 'sports', '⚽', 'Deportes'),
    ('interest', 'cinema', '🎬', 'Cine y Series'),
    ('interest', 'cooking', '👨‍🍳', 'Cocina'),
    ('interest', 'art', '🎨', 'Arte y Diseño'),
    ('interest', 'fashion', '👗', 'Moda'),
    ('interest', 'dance', '💃', 'Baile'),
    ('interest', 'fitness', '💪', 'Fitness'),
    ('interest', 'nature', '🌲', 'Naturaleza'),
    ('interest', 'pets', '🐾', 'Mascotas'),
    ('interest', 'photography', '📸', 'Fotografía'),
    ('interest', 'reading', '📚', 'Lectura'),
    ('interest', 'technology', '💻', 'Tecnología'),
    ('interest', 'travel', '✈️', 'Viajes'),
    
    # Skills
    ('skill', 'speaking', '🗣️', 'Hablar'),
    ('skill', 'listening', '👂', 'Escuchar'),
    ('skill', 'reading', '📖', 'Leer'),
    ('skill', 'writing', '✍️', 'Escribir'),
]

created_tags = {}
for tag_type, value, icon, display_name in all_tags_data:
    tag, _ = Tag.objects.get_or_create(
        type=tag_type,
        value=value,
        defaults={'icon': icon, 'display_name': display_name}
    )
    created_tags[f"{tag_type}:{value}"] = tag

print(f"📌 Tags ready: {Tag.objects.count()}")

# ============================================
# ALL 25 SCENARIOS
# ============================================

scenarios_data = [
    # ========== A1-A2 BÁSICO ==========
    {
        'slug': 'greetings',
        'name': 'Conocer personas',
        'icon': '👋',
        'description': 'Saludos, presentaciones y conversación básica con nuevas personas.',
        'difficulty_min': 'A1', 'difficulty_max': 'A2',
        'tags': ['goal:personal', 'domain:social', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Saludar', 5, 10),
            ('A1', 2, 'Presentarte', 10, 15),
            ('A1', 3, 'Preguntar el nombre', 10, 15),
            ('A2', 1, 'Hablar de tu trabajo', 15, 25),
            ('A2', 2, 'Intercambiar información', 15, 30),
        ],
    },
    {
        'slug': 'restaurant',
        'name': 'Café/Restaurante',
        'icon': '☕',
        'description': 'Ordenar comida y bebidas en restaurantes y cafeterías.',
        'difficulty_min': 'A1', 'difficulty_max': 'B1',
        'tags': ['goal:travel', 'goal:personal', 'domain:food', 'skill:speaking', 'interest:cooking'],
        'milestones': [
            ('A1', 1, 'Pedir una mesa', 10, 20),
            ('A1', 2, 'Leer el menú', 10, 25),
            ('A1', 3, 'Ordenar comida', 15, 30),
            ('A1', 4, 'Pedir la cuenta', 10, 15),
            ('A2', 1, 'Hacer modificaciones', 15, 25),
            ('A2', 2, 'Pedir recomendaciones', 15, 30),
            ('B1', 1, 'Hacer una queja', 20, 35),
        ],
    },
    {
        'slug': 'shopping',
        'name': 'Tienda',
        'icon': '🛒',
        'description': 'Comprar en tiendas, preguntar precios y tallas.',
        'difficulty_min': 'A1', 'difficulty_max': 'A2',
        'tags': ['goal:personal', 'domain:shopping', 'skill:speaking', 'interest:fashion'],
        'milestones': [
            ('A1', 1, 'Preguntar precio', 10, 15),
            ('A1', 2, 'Pedir una talla', 10, 20),
            ('A1', 3, 'Pagar', 10, 15),
            ('A2', 1, 'Pedir descuento', 15, 25),
            ('A2', 2, 'Hacer devolución', 15, 30),
        ],
    },
    {
        'slug': 'hotel',
        'name': 'Hotel',
        'icon': '🏨',
        'description': 'Check-in, check-out y servicios del hotel.',
        'difficulty_min': 'A1', 'difficulty_max': 'B1',
        'tags': ['goal:travel', 'domain:accommodation', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Hacer check-in', 10, 20),
            ('A1', 2, 'Pedir la llave', 10, 15),
            ('A1', 3, 'Preguntar por servicios', 15, 25),
            ('A2', 1, 'Reportar problemas', 15, 30),
            ('A2', 2, 'Hacer check-out', 15, 20),
            ('B1', 1, 'Reservar por teléfono', 20, 40),
        ],
    },
    {
        'slug': 'transport',
        'name': 'Transporte',
        'icon': '🚌',
        'description': 'Usar transporte público, taxis y preguntar direcciones.',
        'difficulty_min': 'A1', 'difficulty_max': 'A2',
        'tags': ['goal:travel', 'domain:transport', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Comprar boleto', 10, 15),
            ('A1', 2, 'Preguntar la parada', 10, 20),
            ('A2', 1, 'Tomar un taxi', 15, 25),
            ('A2', 2, 'Entender anuncios', 15, 30),
        ],
    },
    {
        'slug': 'home',
        'name': 'En casa',
        'icon': '🏠',
        'description': 'Vocabulario del hogar y rutinas diarias.',
        'difficulty_min': 'A1', 'difficulty_max': 'A2',
        'tags': ['goal:personal', 'domain:home', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Objetos de la casa', 10, 30),
            ('A1', 2, 'Rutina diaria', 15, 35),
            ('A2', 1, 'Describir tu casa', 15, 30),
            ('A2', 2, 'Problemas del hogar', 15, 25),
        ],
    },
    {
        'slug': 'directions',
        'name': 'Direcciones',
        'icon': '📍',
        'description': 'Pedir y dar direcciones en la ciudad.',
        'difficulty_min': 'A1', 'difficulty_max': 'A2',
        'tags': ['goal:travel', 'domain:transport', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Preguntar dónde está', 10, 20),
            ('A1', 2, 'Entender izquierda/derecha', 10, 15),
            ('A2', 1, 'Dar direcciones', 15, 30),
            ('A2', 2, 'Usar un mapa', 15, 25),
        ],
    },
    
    # ========== B1-B2 INTERMEDIO ==========
    {
        'slug': 'office',
        'name': 'Oficina',
        'icon': '💼',
        'description': 'Vocabulario y frases para el ambiente laboral.',
        'difficulty_min': 'A1', 'difficulty_max': 'C1',
        'tags': ['goal:work', 'domain:business', 'work_domain:general', 'skill:speaking', 'skill:writing'],
        'milestones': [
            ('A1', 1, 'Objetos de la oficina', 10, 20),
            ('A1', 2, 'Instrucciones básicas', 5, 10),
            ('A2', 1, 'Presentarte en el trabajo', 15, 25),
            ('A2', 2, 'Pedir ayuda a colegas', 15, 30),
            ('B1', 1, 'Participar en reuniones', 20, 40),
            ('B1', 2, 'Escribir emails básicos', 20, 35),
            ('B2', 1, 'Dar presentaciones', 25, 50),
            ('B2', 2, 'Negociar con clientes', 25, 45),
        ],
    },
    {
        'slug': 'doctor',
        'name': 'Hospital/Doctor',
        'icon': '🏥',
        'description': 'Describe síntomas y entiende instrucciones médicas.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'domain:health', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A2', 1, 'Hacer una cita', 15, 25),
            ('A2', 2, 'Describir síntomas', 15, 30),
            ('B1', 1, 'Entender diagnóstico', 20, 40),
            ('B1', 2, 'Instrucciones de medicina', 20, 35),
            ('B2', 1, 'Discutir tratamiento', 25, 50),
        ],
    },
    {
        'slug': 'bank',
        'name': 'Banco',
        'icon': '🏦',
        'description': 'Transacciones bancarias y servicios financieros.',
        'difficulty_min': 'A1', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'goal:work', 'domain:finance', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Billetes y monedas', 10, 15),
            ('A1', 2, 'Números grandes', 10, 20),
            ('A2', 1, 'Abrir una cuenta', 15, 30),
            ('A2', 2, 'Hacer un depósito', 10, 20),
            ('B1', 1, 'Pedir un préstamo', 20, 40),
            ('B1', 2, 'Resolver problemas', 20, 35),
        ],
    },
    {
        'slug': 'phone',
        'name': 'Llamadas telefónicas',
        'icon': '📞',
        'description': 'Hacer y recibir llamadas en contextos formales e informales.',
        'difficulty_min': 'A1', 'difficulty_max': 'B2',
        'tags': ['goal:work', 'goal:personal', 'domain:business', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Identificarse', 5, 10),
            ('A1', 2, 'Números de teléfono', 10, 15),
            ('A2', 1, 'Contestar una llamada', 10, 20),
            ('A2', 2, 'Dejar un mensaje', 15, 25),
            ('B1', 1, 'Llamadas de trabajo', 20, 35),
            ('B2', 1, 'Conferencias', 25, 45),
        ],
    },
    {
        'slug': 'airport',
        'name': 'Aeropuerto',
        'icon': '✈️',
        'description': 'Navega el aeropuerto con confianza.',
        'difficulty_min': 'A1', 'difficulty_max': 'B2',
        'tags': ['goal:travel', 'domain:transport', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Mostrar documentos', 10, 15),
            ('A1', 2, 'Pasar seguridad', 10, 20),
            ('A2', 1, 'Preguntar por la puerta', 10, 20),
            ('A2', 2, 'Comprar en duty free', 15, 25),
            ('B1', 1, 'Manejar retrasos', 20, 35),
            ('B1', 2, 'Hacer conexiones', 20, 30),
        ],
    },
    {
        'slug': 'university',
        'name': 'Universidad',
        'icon': '🎓',
        'description': 'Vida académica, clases y campus.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:personal', 'domain:education', 'skill:speaking', 'skill:writing', 'skill:reading', 'interest:reading'],
        'milestones': [
            ('B1', 1, 'Inscribirte a clases', 15, 30),
            ('B1', 2, 'Hablar con profesores', 20, 35),
            ('B2', 1, 'Presentar trabajos', 25, 50),
            ('B2', 2, 'Debates académicos', 25, 45),
        ],
    },
    {
        'slug': 'news',
        'name': 'Noticias',
        'icon': '📰',
        'description': 'Entender y discutir noticias actuales.',
        'difficulty_min': 'B1', 'difficulty_max': 'C2',
        'tags': ['goal:general', 'domain:news', 'skill:reading', 'skill:listening'],
        'milestones': [
            ('B1', 1, 'Entender titulares', 15, 30),
            ('B1', 2, 'Resumen de noticias', 20, 40),
            ('B2', 1, 'Análisis de eventos', 25, 50),
            ('C1', 1, 'Opiniones complejas', 30, 60),
        ],
    },
    {
        'slug': 'opinions',
        'name': 'Dar opiniones',
        'icon': '🗣️',
        'description': 'Expresar y defender tus opiniones.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:personal', 'domain:social', 'skill:speaking'],
        'milestones': [
            ('B1', 1, 'Expresar preferencias', 15, 25),
            ('B1', 2, 'Estar de acuerdo/desacuerdo', 15, 30),
            ('B2', 1, 'Argumentar tu posición', 25, 45),
            ('C1', 1, 'Debates complejos', 30, 55),
        ],
    },
    
    # ========== C1-C2 AVANZADO ==========
    {
        'slug': 'legal',
        'name': 'Legal/Contratos',
        'icon': '⚖️',
        'description': 'Vocabulario legal y documentos formales.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'domain:legal', 'work_domain:legal', 'skill:reading', 'skill:writing'],
        'milestones': [
            ('B2', 1, 'Leer contratos básicos', 25, 50),
            ('C1', 1, 'Negociar términos', 30, 60),
            ('C2', 1, 'Documentos complejos', 35, 70),
        ],
    },
    {
        'slug': 'presentations',
        'name': 'Presentaciones',
        'icon': '📊',
        'description': 'Dar presentaciones profesionales efectivas.',
        'difficulty_min': 'A1', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'domain:business', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Saludo inicial', 5, 10),
            ('A1', 2, 'Conectores simples', 10, 15),
            ('B1', 1, 'Estructura básica', 20, 35),
            ('B2', 1, 'Gráficos y datos', 25, 45),
            ('C1', 1, 'Manejar preguntas', 30, 55),
            ('C2', 1, 'Presentaciones ejecutivas', 35, 65),
        ],
    },
    {
        'slug': 'negotiations',
        'name': 'Negociaciones',
        'icon': '🤝',
        'description': 'Negociar en contextos de negocios.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'domain:business', 'skill:speaking'],
        'milestones': [
            ('B2', 1, 'Propuestas', 25, 45),
            ('C1', 1, 'Técnicas de negociación', 30, 55),
            ('C2', 1, 'Negociaciones complejas', 35, 65),
        ],
    },
    {
        'slug': 'culture',
        'name': 'Cultura/Arte',
        'icon': '🎭',
        'description': 'Discutir arte, música y cultura.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:personal', 'domain:culture', 'domain:entertainment', 'skill:speaking', 'interest:art', 'interest:music'],
        'milestones': [
            ('B2', 1, 'Describir obras de arte', 25, 45),
            ('C1', 1, 'Crítica cultural', 30, 55),
            ('C2', 1, 'Análisis profundo', 35, 65),
        ],
    },
    {
        'slug': 'literature',
        'name': 'Literatura',
        'icon': '📚',
        'description': 'Leer y discutir literatura.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:personal', 'domain:literature', 'domain:education', 'skill:reading', 'interest:reading'],
        'milestones': [
            ('B2', 1, 'Resumen de libros', 25, 50),
            ('C1', 1, 'Análisis literario', 30, 60),
            ('C2', 1, 'Interpretación avanzada', 35, 70),
        ],
    },
    {
        'slug': 'humor',
        'name': 'Humor/Sarcasmo',
        'icon': '😂',
        'description': 'Entender y usar humor en el idioma.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:personal', 'domain:social', 'domain:entertainment', 'skill:listening'],
        'milestones': [
            ('B2', 1, 'Chistes simples', 20, 35),
            ('C1', 1, 'Sarcasmo e ironía', 25, 45),
            ('C2', 1, 'Humor cultural', 30, 55),
        ],
    },
    {
        'slug': 'idioms',
        'name': 'Expresiones idiomáticas',
        'icon': '🗣️',
        'description': 'Dominar frases hechas y expresiones.',
        'difficulty_min': 'B1', 'difficulty_max': 'C2',
        'tags': ['goal:general', 'domain:social', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('B1', 1, 'Idioms básicos', 15, 30),
            ('B2', 1, 'Idioms de negocios', 20, 40),
            ('C1', 1, 'Idioms avanzados', 25, 50),
            ('C2', 1, 'Expresiones regionales', 30, 60),
        ],
    },
    {
        'slug': 'dialects',
        'name': 'Dialectos regionales',
        'icon': '🌍',
        'description': 'Entender variaciones regionales del idioma.',
        'difficulty_min': 'C1', 'difficulty_max': 'C2',
        'tags': ['goal:general', 'domain:culture', 'skill:listening'],
        'milestones': [
            ('C1', 1, 'Acentos principales', 30, 50),
            ('C2', 1, 'Slang regional', 35, 60),
            ('C2', 2, 'Variaciones culturales', 35, 65),
        ],
    },
    {
        'slug': 'formal_emails',
        'name': 'Emails formales',
        'icon': '📧',
        'description': 'Escribir emails profesionales y formales.',
        'difficulty_min': 'A1', 'difficulty_max': 'C1',
        'tags': ['goal:work', 'domain:business', 'skill:writing'],
        'milestones': [
            ('A1', 1, 'Partes de un email', 5, 10),
            ('A1', 2, 'Saludos básicos', 5, 10),
            ('B1', 1, 'Emails básicos', 15, 30),
            ('B2', 1, 'Emails de negocios', 20, 40),
            ('C1', 1, 'Correspondencia ejecutiva', 25, 50),
        ],
    },
    {
        'slug': 'gaming',
        'name': 'Gaming',
        'icon': '🎮',
        'description': 'Vocabulario de videojuegos y gaming online.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'interest:gaming', 'domain:entertainment', 'domain:technology', 'skill:speaking', 'skill:listening', 'interest:technology'],
        'milestones': [
            ('A2', 1, 'Vocabulario básico de gaming', 15, 30),
            ('B1', 1, 'Comunicación en equipo', 20, 40),
            ('B2', 1, 'Streaming y comunidad', 25, 50),
        ],
    },
    
    # ========== ADICIONALES (INTERESES) ==========
    {
        'slug': 'cooking',
        'name': 'Cocina/Recetas',
        'icon': '🍳',
        'description': 'Vocabulario de cocina, ingredientes y seguir recetas.',
        'difficulty_min': 'A1', 'difficulty_max': 'B1',
        'tags': ['goal:personal', 'interest:cooking', 'domain:food', 'skill:reading', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Ingredientes básicos', 10, 30),
            ('A1', 2, 'Utensilios de cocina', 10, 25),
            ('A2', 1, 'Seguir recetas simples', 15, 35),
            ('A2', 2, 'Medir y pesar', 15, 20),
            ('B1', 1, 'Explicar cómo cocinar', 20, 40),
        ],
    },
    {
        'slug': 'salon',
        'name': 'Peluquería/Spa',
        'icon': '💇',
        'description': 'Pedir un corte de pelo, tratamientos de belleza.',
        'difficulty_min': 'A2', 'difficulty_max': 'B1',
        'tags': ['goal:personal', 'goal:travel', 'domain:social', 'skill:speaking', 'interest:fashion'],
        'milestones': [
            ('A2', 1, 'Pedir cita', 10, 20),
            ('A2', 2, 'Describir qué quieres', 15, 30),
            ('B1', 1, 'Tratamientos específicos', 20, 40),
        ],
    },
    {
        'slug': 'car_rental',
        'name': 'Renta de autos',
        'icon': '🚗',
        'description': 'Rentar un auto, seguros y devolución.',
        'difficulty_min': 'A2', 'difficulty_max': 'B1',
        'tags': ['goal:travel', 'domain:transport', 'skill:speaking', 'skill:reading'],
        'milestones': [
            ('A2', 1, 'Reservar un auto', 15, 25),
            ('A2', 2, 'Entender el contrato', 15, 30),
            ('B1', 1, 'Reportar problemas', 20, 35),
            ('B1', 2, 'Devolución del auto', 15, 25),
        ],
    },
    {
        'slug': 'gym',
        'name': 'Gimnasio/Deportes',
        'icon': '🏋️',
        'description': 'Inscribirse al gym, ejercicios y deportes.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'interest:sports', 'domain:health', 'skill:speaking', 'interest:fitness'],
        'milestones': [
            ('A2', 1, 'Inscripción al gym', 15, 25),
            ('A2', 2, 'Partes del cuerpo', 10, 30),
            ('B1', 1, 'Hablar de rutinas', 20, 40),
            ('B2', 1, 'Discutir estrategias', 25, 50),
        ],
    },
    {
        'slug': 'music',
        'name': 'Música/Conciertos',
        'icon': '🎵',
        'description': 'Hablar de música, artistas y eventos.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'interest:music', 'domain:entertainment', 'skill:speaking', 'skill:listening', 'interest:dance'],
        'milestones': [
            ('A2', 1, 'Géneros musicales', 10, 25),
            ('A2', 2, 'Tu música favorita', 15, 30),
            ('B1', 1, 'Comprar boletos', 15, 25),
            ('B2', 1, 'Reseñar un concierto', 25, 45),
        ],
    },
    {
        'slug': 'social_media',
        'name': 'Redes sociales',
        'icon': '📱',
        'description': 'Vocabulario de redes sociales y comunicación digital.',
        'difficulty_min': 'A2', 'difficulty_max': 'B1',
        'tags': ['goal:personal', 'domain:technology', 'domain:social', 'skill:reading', 'skill:writing', 'interest:technology', 'interest:photography'],
        'milestones': [
            ('A2', 1, 'Crear un perfil', 10, 25),
            ('A2', 2, 'Publicar y comentar', 15, 30),
            ('B1', 1, 'Describir tendencias', 20, 40),
        ],
    },
    {
        'slug': 'pharmacy',
        'name': 'Farmacia',
        'icon': '🏪',
        'description': 'Comprar medicinas y productos de salud.',
        'difficulty_min': 'A1', 'difficulty_max': 'B1',
        'tags': ['goal:personal', 'goal:travel', 'domain:health', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Pedir medicina básica', 10, 20),
            ('A2', 1, 'Describir síntomas', 15, 30),
            ('B1', 1, 'Entender indicaciones', 20, 35),
        ],
    },
    {
        'slug': 'movies',
        'name': 'Cine/Series',
        'icon': '📺',
        'description': 'Hablar de películas, series y entretenimiento.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'interest:cinema', 'domain:entertainment', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A2', 1, 'Géneros de películas', 10, 25),
            ('A2', 2, 'Describir una película', 15, 30),
            ('B1', 1, 'Dar tu opinión', 20, 40),
            ('B2', 1, 'Análisis de series', 25, 50),
        ],
    },
    {
        'slug': 'pets',
        'name': 'Mascotas/Veterinario',
        'icon': '🐶',
        'description': 'Hablar de mascotas y visitas al veterinario.',
        'difficulty_min': 'A2', 'difficulty_max': 'B1',
        'tags': ['goal:personal', 'domain:health', 'domain:home', 'skill:speaking', 'interest:pets'],
        'milestones': [
            ('A2', 1, 'Describir tu mascota', 15, 25),
            ('A2', 2, 'En el veterinario', 15, 30),
            ('B1', 1, 'Cuidado de mascotas', 20, 40),
        ],
    },
    {
        'slug': 'dating',
        'name': 'Citas/Romance',
        'icon': '💑',
        'description': 'Vocabulario para citas y relaciones románticas.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:personal', 'domain:social', 'skill:speaking'],
        'milestones': [
            ('B1', 1, 'Invitar a alguien', 15, 25),
            ('B1', 2, 'Primera cita', 20, 35),
            ('B2', 1, 'Expresar sentimientos', 25, 45),
            ('C1', 1, 'Relaciones complejas', 30, 55),
        ],
    },
    # ===========================================
    # NUEVOS ESCENARIOS - Enero 2026
    # ===========================================
    {
        'slug': 'job-interview',
        'name': 'Entrevista de trabajo',
        'icon': '🤝',
        'description': 'Prepárate para entrevistas de trabajo en inglés.',
        'difficulty_min': 'A1', 'difficulty_max': 'C1',
        'tags': ['goal:work', 'domain:business', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('A1', 1, 'Datos personales', 10, 15),
            ('A1', 2, 'Adjetivos profesionales', 10, 15),
            ('A2', 1, 'Presentarte profesionalmente', 15, 30),
            ('A2', 2, 'Describir tu experiencia', 15, 35),
            ('A2', 3, 'Responder "Háblame de ti"', 15, 25),
            ('B1', 1, 'Hablar de tus fortalezas', 20, 40),
            ('B1', 2, 'Responder preguntas difíciles', 20, 45),
            ('B2', 1, 'Negociar salario', 25, 50),
        ],
    },
    {
        'slug': 'work-meetings',
        'name': 'Reuniones de trabajo',
        'icon': '📋',
        'description': 'Participa efectivamente en reuniones profesionales.',
        'difficulty_min': 'B1', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'domain:business', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('B1', 1, 'Entender la agenda', 15, 30),
            ('B1', 2, 'Dar tu opinión', 20, 35),
            ('B1', 3, 'Pedir aclaraciones', 15, 25),
            ('B2', 1, 'Proponer ideas', 25, 45),
            ('B2', 2, 'Debatir profesionalmente', 25, 50),
            ('C1', 1, 'Liderar una reunión', 30, 60),
        ],
    },
    {
        'slug': 'emergencies',
        'name': 'Emergencias',
        'icon': '🚨',
        'description': 'Comunicación en situaciones de emergencia.',
        'difficulty_min': 'A2', 'difficulty_max': 'B2',
        'tags': ['goal:travel', 'goal:personal', 'domain:health', 'skill:speaking', 'skill:listening', 'interest:travel'],
        'milestones': [
            ('A2', 1, 'Llamar al 911', 15, 25),
            ('A2', 2, 'Describir una emergencia', 15, 30),
            ('A2', 3, 'Dar tu ubicación', 10, 20),
            ('B1', 1, 'Reportar un robo', 20, 40),
            ('B1', 2, 'Hablar con la policía', 20, 45),
            ('B2', 1, 'Hacer una denuncia formal', 25, 55),
        ],
    },
    {
        'slug': 'chat-messaging',
        'name': 'WhatsApp/Chat',
        'icon': '💬',
        'description': 'Comunicación informal por mensajes.',
        'difficulty_min': 'A1', 'difficulty_max': 'B2',
        'tags': ['goal:personal', 'domain:entertainment', 'skill:writing', 'skill:reading'],
        'milestones': [
            ('A1', 1, 'Saludos y despedidas', 10, 15),
            ('A1', 2, 'Hacer planes básicos', 10, 20),
            ('A1', 3, 'Usar emojis y abreviaturas', 10, 25),
            ('A2', 1, 'Conversación casual', 15, 30),
            ('A2', 2, 'Expresar emociones', 15, 25),
            ('B1', 1, 'Contar historias por chat', 20, 40),
            ('B2', 1, 'Humor y sarcasmo escrito', 25, 50),
        ],
    },
    # ===========================================
    # ESCENARIOS AVANZADOS B2-C2 - Enero 2026
    # ===========================================
    {
        'slug': 'explaining-ideas',
        'name': 'Explicar ideas complejas',
        'icon': '🧠',
        'description': 'Explicar conceptos, razonamiento y relaciones causa-efecto.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'goal:certification', 'domain:education', 'skill:speaking'],
        'milestones': [
            ('B2', 1, 'Describir un proceso', 25, 45),
            ('B2', 2, 'Explicar causa y efecto', 25, 50),
            ('C1', 1, 'Analogías y comparaciones', 30, 55),
            ('C1', 2, 'Argumentar con evidencia', 30, 60),
            ('C2', 1, 'Explicar teorías abstractas', 35, 70),
        ],
    },
    {
        'slug': 'debate',
        'name': 'Debate / Discusión formal',
        'icon': '🗣️',
        'description': 'Debate estructurado: acordar, refutar, conceder puntos.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:certification', 'domain:education', 'skill:speaking', 'skill:listening'],
        'milestones': [
            ('B2', 1, 'Expresar acuerdo/desacuerdo', 25, 40),
            ('B2', 2, 'Estructurar un argumento', 25, 50),
            ('C1', 1, 'Refutar argumentos', 30, 60),
            ('C1', 2, 'Conceder y contraargumentar', 30, 65),
            ('C2', 1, 'Debate avanzado', 35, 75),
        ],
    },
    {
        'slug': 'academic-writing',
        'name': 'Escritura académica / Ensayos',
        'icon': '✍️',
        'description': 'Escribir ensayos, introducciones, argumentos y conclusiones.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:certification', 'domain:education', 'skill:writing'],
        'milestones': [
            ('B2', 1, 'Escribir introducciones', 30, 50),
            ('B2', 2, 'Desarrollar párrafos de argumento', 30, 55),
            ('C1', 1, 'Conclusiones efectivas', 30, 60),
            ('C1', 2, 'Transiciones y conectores', 25, 45),
            ('C2', 1, 'Ensayo académico completo', 45, 80),
        ],
    },
    {
        'slug': 'complaints',
        'name': 'Quejas y reclamos formales',
        'icon': '📢',
        'description': 'Comunicación formal para quejas: servicio al cliente, escalación.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:personal', 'goal:travel', 'domain:shopping', 'skill:speaking', 'skill:writing'],
        'milestones': [
            ('B1', 1, 'Describir un problema', 20, 35),
            ('B1', 2, 'Pedir una solución', 20, 40),
            ('B2', 1, 'Escalar una queja', 25, 50),
            ('B2', 2, 'Escribir una queja formal', 30, 55),
            ('C1', 1, 'Tono legal y firme', 30, 60),
        ],
    },
    {
        'slug': 'conflict-resolution',
        'name': 'Resolución de conflictos',
        'icon': '🤝',
        'description': 'Disculparse, aclarar malentendidos, lenguaje diplomático.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:work', 'goal:personal', 'domain:social', 'skill:speaking'],
        'milestones': [
            ('B1', 1, 'Disculparse sinceramente', 20, 30),
            ('B1', 2, 'Aclarar un malentendido', 20, 40),
            ('B2', 1, 'Mediar en un conflicto', 25, 50),
            ('B2', 2, 'Lenguaje diplomático', 25, 55),
            ('C1', 1, 'Negociar soluciones', 30, 60),
        ],
    },
    {
        'slug': 'public-opinion',
        'name': 'Opinión pública / Sociedad',
        'icon': '📰',
        'description': 'Discutir temas sociales, noticias y discurso público avanzado.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:certification', 'domain:news', 'skill:speaking', 'skill:reading'],
        'milestones': [
            ('B2', 1, 'Resumir una noticia', 25, 45),
            ('B2', 2, 'Dar tu opinión sobre un tema', 25, 50),
            ('C1', 1, 'Analizar perspectivas', 30, 60),
            ('C1', 2, 'Discurso con matices', 30, 65),
            ('C2', 1, 'Debate de temas complejos', 35, 75),
        ],
    },
    {
        'slug': 'teaching',
        'name': 'Enseñar / Explicar a otros',
        'icon': '📚',
        'description': 'Dar instrucciones, enseñar conceptos, guiar a otros.',
        'difficulty_min': 'A1', 'difficulty_max': 'C2',
        'tags': ['goal:work', 'work_domain:education', 'skill:speaking'],
        'milestones': [
            ('A1', 1, 'Imperativos de clase', 10, 15),
            ('A1', 2, 'Feedback simple', 5, 10),
            ('B2', 1, 'Dar instrucciones claras', 25, 45),
            ('B2', 2, 'Verificar comprensión', 20, 35),
            ('C1', 1, 'Adaptar explicaciones', 30, 55),
            ('C1', 2, 'Retroalimentación constructiva', 30, 60),
            ('C2', 1, 'Enseñanza avanzada', 35, 70),
        ],
    },
    {
        'slug': 'migration',
        'name': 'Migración / Trámites oficiales',
        'icon': '🧳',
        'description': 'Visas, formularios, burocracia e inglés formal técnico.',
        'difficulty_min': 'B1', 'difficulty_max': 'C1',
        'tags': ['goal:travel', 'goal:personal', 'domain:legal', 'skill:speaking', 'skill:writing'],
        'milestones': [
            ('B1', 1, 'Llenar formularios básicos', 20, 40),
            ('B1', 2, 'Entrevista de visa', 25, 50),
            ('B2', 1, 'Documentos legales', 30, 55),
            ('B2', 2, 'Explicar tu situación', 25, 50),
            ('C1', 1, 'Apelar decisiones', 35, 65),
        ],
    },
    {
        'slug': 'mental-health',
        'name': 'Salud mental / Emociones',
        'icon': '🧘',
        'description': 'Expresar sentimientos, estrés, establecer límites.',
        'difficulty_min': 'B2', 'difficulty_max': 'C2',
        'tags': ['goal:personal', 'domain:health', 'skill:speaking'],
        'milestones': [
            ('B2', 1, 'Describir emociones complejas', 25, 45),
            ('B2', 2, 'Hablar de estrés', 25, 50),
            ('C1', 1, 'Establecer límites', 30, 55),
            ('C1', 2, 'Conversaciones difíciles', 30, 60),
            ('C2', 1, 'Vocabulario emocional avanzado', 35, 70),
        ],
    },
]

# Create scenarios and milestones
for data in scenarios_data:
    scenario, created = Scenario.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'name': data['name'],
            'icon': data['icon'],
            'description': data['description'],
            'difficulty_min': data['difficulty_min'],
            'difficulty_max': data['difficulty_max'],
        }
    )
    
    # Clear existing tags and add new ones
    scenario.tags.clear()
    for tag_key in data['tags']:
        if tag_key in created_tags:
            scenario.tags.add(created_tags[tag_key])
    
    # Create milestones
    for level, order, name, time, vocab in data['milestones']:
        Milestone.objects.update_or_create(
            scenario=scenario,
            level=level,
            order=order,
            defaults={
                'name': name,
                'estimated_time': time,
                'new_vocab_count': vocab,
            }
        )
    
    status = "✅ Created" if created else "🔄 Updated"
    print(f"  {status}: {scenario}")

print(f"\n🏰 Total scenarios: {Scenario.objects.count()}")
print(f"🎯 Total milestones: {Milestone.objects.count()}")
print(f"📌 Total tags: {Tag.objects.count()}")
print("\n✅ All 48 scenarios seeded!")


