# -*- coding: utf-8 -*-
"""
Fix emoji icons for tags
Run with: python manage.py shell < scripts/fix_tag_icons.py
"""

from apps.memory_palace.models import Tag

# Map of tag values to their correct emoji icons
ICON_MAP = {
    # Goals
    'work': '\U0001F4BC',  # 💼
    'travel': '\u2708\uFE0F',  # ✈️
    'personal': '\U0001F3E0',  # 🏠
    'certification': '\U0001F4DC',  # 📜
    'general': '\U0001F310',  # 🌐
    
    # Domains
    'food': '\U0001F37D\uFE0F',  # 🍽️
    'business': '\U0001F4BC',  # 💼
    'health': '\U0001F3E5',  # 🏥
    'entertainment': '\U0001F3AC',  # 🎬
    'transport': '\U0001F68C',  # 🚌
    'accommodation': '\U0001F3E8',  # 🏨
    'shopping': '\U0001F6D2',  # 🛒
    'social': '\U0001F465',  # 👥
    'education': '\U0001F393',  # 🎓
    'finance': '\U0001F3E6',  # 🏦
    'legal': '\u2696\uFE0F',  # ⚖️
    'culture': '\U0001F3AD',  # 🎭
    'literature': '\U0001F4DA',  # 📚
    'technology': '\U0001F4BB',  # 💻
    'home': '\U0001F3E0',  # 🏠
    'news': '\U0001F4F0',  # 📰
    
    # Work domains
    'tech': '\U0001F4BB',  # 💻
    'sales': '\U0001F4CA',  # 📊
    'creative': '\U0001F3A8',  # 🎨
    
    # Interests
    'gaming': '\U0001F3AE',  # 🎮
    'music': '\U0001F3B5',  # 🎵
    'sports': '\u26BD',  # ⚽
    'cinema': '\U0001F3AC',  # 🎬
    'cooking': '\U0001F468\u200D\U0001F373',  # 👨‍🍳
    'art': '\U0001F3A8',  # 🎨
    
    # Skills
    'speaking': '\U0001F5E3\uFE0F',  # 🗣️
    'listening': '\U0001F442',  # 👂
    'reading': '\U0001F4D6',  # 📖
    'writing': '\u270D\uFE0F',  # ✍️
}

print("Fixing tag icons...")

for tag in Tag.objects.all():
    if tag.value in ICON_MAP:
        old_icon = tag.icon
        tag.icon = ICON_MAP[tag.value]
        tag.save()
        print(f"Fixed: {tag.value} -> {tag.icon}")

print(f"\nTotal tags: {Tag.objects.count()}")
print("Done!")
