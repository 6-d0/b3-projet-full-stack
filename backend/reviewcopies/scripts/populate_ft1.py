import os
import sys
from pathlib import Path

import django
import yaml
from django.db import IntegrityError, transaction

DIR = Path(__file__).parent
sys.path.insert(0, str(DIR.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewcopies.settings.dev")
django.setup()

import reviewcopies.models as models  # noqa:E402


def attr(obj, *attrs, **kwargs):
    try:
        value = getattr(obj, attrs[0])
        for attr in attrs[1:]:
            value = getattr(value, attr)
    except (IndexError, AttributeError):
        return kwargs.get("default", None)
    return value


with open(DIR.parent / "data" / "fixtures1.yaml") as f:
    data = yaml.load(f, yaml.Loader)


user_data = data.pop("User", [])

for user in user_data:
    try:
        password = user.pop("password")
        user_instance, created = models.User.objects.get_or_create(
            username=user.get("username"), defaults=user
        )
        if created:
            user_instance.set_password(password)
            user_instance.role = (
                "student" if user_instance.username.startswith("e") else "teacher"
            )
            user_instance.role = (
                "admin" if user_instance.is_superuser else user_instance.role
            )
            user_instance.full_clean()
            user_instance.save()
            print(f"Utilisateur '{user_instance.username}' créé avec succès.")
        else:
            print(f"Utilisateur '{user_instance.username}' existe déjà.")
    except IntegrityError as e:
        print(f"Erreur d'intégrité pour l'utilisateur {user.get('username')}: {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


with transaction.atomic():
    for model_name, entries in data.items():
        try:
            model = getattr(models, model_name)
        except AttributeError:
            print(f"Modèle '{model_name}' introuvable dans les modèles Django.")
            continue

        for entry in entries:
            try:
                m2m = entry.pop("m2m", [])
                obj, created = model.objects.get_or_create(**entry)
                if created:
                    obj.full_clean()
                    obj.save()
                    print(f"{model_name} instance créée : {entry}")
                else:
                    print(f"{model_name} instance existe déjà : {entry}")

                for d in m2m:
                    name, pk = next(iter(d.items()))
                    related_manager = attr(obj, name, "add")
                    if related_manager:
                        related_manager(pk)
                        print(f"Relation ManyToMany ajoutée : {name} -> {pk}")
            except IntegrityError as e:
                print(f"Erreur d'intégrité pour {model_name}: {e}")
            except Exception as e:
                print(f"Erreur inattendue dans {model_name}: {e}")
