# Personnalisation du Panneau d'Administration Django : Thèmes, Sécurité et Améliorations UI

Ce projet vise à améliorer et personnaliser le panneau d'administration par défaut de Django en introduisant des fonctionnalités de gestion de thèmes, d'analyse d'accessibilité basée sur l'IA, et une API robuste pour l'interaction.

---

## ✨ Fonctionnalités Implémentées

### 🎨 Gestion des Thèmes (`AdminTheme` Model)
- Modèle `AdminTheme` pour définir et stocker les configurations de thèmes (nom, URLs CSS/JS, statut actif).
- Validation des URLs CSS/JS pour s'assurer qu'elles se terminent par les extensions correctes.

### 🛠️ API RESTful pour la Gestion des Thèmes
- Endpoints pour **lister, créer, récupérer, mettre à jour et supprimer** des thèmes.
- Endpoint dédié pour **activer un thème spécifique** (`is_active=True`), désactivant automatiquement les autres.
- Endpoint `/api/themes/upload/` pour **téléverser des fichiers CSS/JS** et les associer à un thème existant ou nouveau, avec gestion de l’écrasement.

### ⚙️ API GraphQL pour la Gestion des Thèmes
- Types GraphQL pour exposer les données des thèmes.
- Mutation `switchAdminSkin` pour changer le thème actif via GraphQL.

### 🔒 Sécurité Robuste
- Accès aux APIs REST et mutations GraphQL **restreint aux superutilisateurs uniquement**.
- Protection CSRF intégrée (Django).

### 📦 Intégration Celery pour les Tâches d'Arrière-Plan
- Tâche `analyze_ui_suggestions` pour analyser les fichiers CSS et générer des suggestions d’accessibilité (contraste des couleurs, dépendance à la couleur seule).

### 📑 Rapport d'Accessibilité
- Rapport textuel stocké dans le champ `accessibility_report`, avec détails lisibles sur les problèmes détectés.

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d’avoir les éléments suivants installés :

- Python 3.x (recommandé : 3.9+)
- pip
- Redis

📌 Pour Redis :
- **Windows** : [Port non officiel Redis](https://github.com/microsoftarchive/redis/releases)
- **Linux/macOS** : via terminal :  
  `sudo apt install redis-server` ou `brew install redis`

---

## 🚀 Installation

```bash
# Clonez le dépôt
git clone https://github.com/BerrimaFedi/admin-ui.git
cd admin-ui

# Créez un environnement virtuel
python -m venv venv

# Activez-le
# Sous Windows
.\venv\Scripts\activate
# Sous Linux/macOS
source venv/bin/activate

# Installez les dépendances
pip install -r requirements.txt

# Appliquez les migrations
python manage.py migrate

# Créez un superutilisateur
python manage.py createsuperuser

# Lancez le serveur de
