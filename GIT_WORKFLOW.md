# Git Workflow - YoPuedo360

## 🌿 Estructura de Ramas

```
main (stable)
  └─ develop (unstable/experimental)
```

### `main` - Rama Estable
- Código probado y funcionando
- Flujos de usuario validados
- Se puede deployar en cualquier momento
- **Solo merge desde develop después de testing**

### `develop` - Rama de Desarrollo
- Código nuevo, features experimentales
- Puede tener bugs
- Refactorings grandes
- Cambios de arquitectura
- **Trabajo diario aquí**

---

## 🔄 Flujo de Trabajo

### 1. Desarrollo Normal (Feature Nueva)

```bash
# Asegúrate de estar en develop
git checkout develop

# Haz cambios
# ... código ...

# Commit
git add .
git commit -m "feat: descripción del feature"

# Push a remote (cuando quieras backup)
git push origin develop
```

### 2. Testing Antes de Merge a Main

```bash
# En develop, ejecuta TODOS los tests
pytest
python manage.py test
python manage.py check

# Prueba flujos manualmente
# - Login
# - Milestone navigation
# - Vocabulary practice
# etc.

# Si todo funciona:
git checkout main
git merge develop
git push origin main
```

### 3. Si Develop se Rompe (Rollback)

```bash
# Volver a commit anterior
git log --oneline  # Ver commits
git reset --hard COMMIT_ID

# O descartar cambios no commiteados
git checkout .
```

---

## 📋 Estado Actual

### Commit en Develop (d35dd4e)

**Cambios incluidos:**
- ✅ Vocabulary app completo
- ✅ VocabularyInMilestone model
- ✅ 9 tests (todos pasan)
- ✅ Migrations aplicadas
- ✅ README.md documentación

**Status:** UNSTABLE
- ⚠️ Migrations nuevas (DB schema cambió)
- ⚠️ Apps renombrados (progress → learning_path, memory_palace → scenarios)
- ⚠️ No probado con frontend
- ⚠️ No hay datos seed todavía

**Antes de merge a main:**
- [ ] Probar flujo completo de usuario
- [ ] Verify migrations no rompen data existente
- [ ] Seed data básico (scenarios, vocabulary)
- [ ] Frontend funciona con nuevos endpoints

### Main Branch (2094e97)

**Último commit:** "Simplificar landing page"
- ✅ Código estable
- ✅ Frontend funcional
- ✅ Landing page actualizado

---

## 🚨 Importantes Recordatorios

### NO hacer en Main:
- ❌ Desarrollo experimental
- ❌ Refactorings grandes
- ❌ Cambios de DB schema sin testing
- ❌ Commits directos (siempre desde develop)

### SÍ hacer en Develop:
- ✅ Features nuevos
- ✅ Refactorings
- ✅ Experiments
- ✅ Breaking changes

### Antes de Merge Develop → Main:
- ✅ Todos los tests pasan
- ✅ Migrations probadas
- ✅ Flujos de usuario funcionan
- ✅ Sin errores en python manage.py check
- ✅ README actualizado

---

## 📍 Comandos Útiles

```bash
# Ver en qué rama estás
git branch

# Cambiar a develop
git checkout develop

# Cambiar a main
git checkout main

# Ver diferencias entre ramas
git diff main develop

# Ver commits solo en develop
git log main..develop --oneline

# Ver archivos modificados
git status
```

---

## 🎯 Próximos Pasos en Develop

1. [ ] Crear scripts de seed
   - `scripts/seed_vocabulary_cambridge.py`
   - `scripts/seed_scenarios.py`

2. [ ] Testing de integración
   - API endpoints
   - Frontend compatibility

3. [ ] Cuando esté estable → Merge a main
