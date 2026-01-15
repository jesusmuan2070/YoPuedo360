# -*- coding: utf-8 -*-
"""
Fix display names encoding for tags
"""

from apps.memory_palace.models import Tag

LABEL_FIXES = {
    # Work domains
    ('work_domain', 'education'): 'Educación',
    ('work_domain', 'tech'): 'Tecnología',
    ('work_domain', 'health'): 'Salud',
    ('work_domain', 'sales'): 'Ventas',
    ('work_domain', 'creative'): 'Creativo',
    ('work_domain', 'general'): 'General',
    ('work_domain', 'legal'): 'Legal',
    
    # Goals
    ('goal', 'certification'): 'Certificación',
    ('goal', 'personal'): 'Personal',
    ('goal', 'travel'): 'Viajes',
    ('goal', 'work'): 'Trabajo',
    ('goal', 'general'): 'General',
    
    # Domains
    ('domain', 'food'): 'Comida',
    ('domain', 'business'): 'Negocios',
    ('domain', 'health'): 'Salud',
    ('domain', 'entertainment'): 'Entretenimiento',
    ('domain', 'transport'): 'Transporte',
    ('domain', 'accommodation'): 'Alojamiento',
    ('domain', 'shopping'): 'Compras',
    ('domain', 'social'): 'Social',
    ('domain', 'education'): 'Educación',
    ('domain', 'finance'): 'Finanzas',
    ('domain', 'legal'): 'Legal',
    ('domain', 'culture'): 'Cultura',
    ('domain', 'literature'): 'Literatura',
    ('domain', 'technology'): 'Tecnología',
    ('domain', 'home'): 'Casa',
    ('domain', 'news'): 'Noticias',
    
    # Interests
    ('interest', 'gaming'): 'Gaming',
    ('interest', 'music'): 'Música',
    ('interest', 'sports'): 'Deportes',
    ('interest', 'cinema'): 'Cine',
    ('interest', 'cooking'): 'Cocina',
    ('interest', 'art'): 'Arte',
    
    # Skills
    ('skill', 'speaking'): 'Hablar',
    ('skill', 'listening'): 'Escuchar',
    ('skill', 'reading'): 'Leer',
    ('skill', 'writing'): 'Escribir',
}

print("Fixing display names...")

for (tag_type, value), label in LABEL_FIXES.items():
    updated = Tag.objects.filter(type=tag_type, value=value).update(display_name=label)
    if updated:
        print(f"Fixed: {tag_type}:{value} -> {label}")

print("Done!")
