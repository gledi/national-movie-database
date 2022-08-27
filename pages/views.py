from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    print(request.session)
    greeting = "I don't know who you are!"
    if request.user.is_authenticated:
        greeting = f"Hello {request.user.get_full_name()}"
    return render(request, "pages/index.html", context={"greeting": greeting})


def about_us(request):
    return render(request, "pages/about_us.html")


def contact_us(request):
    return render(request, "pages/contact_us.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


import sqlite3


class Migration:
    def __init__(self, id, app, name, applied):
        self.id = self.pk = id
        self.app = app
        self.name = name
        self.applied = applied

    def __str__(self):
        return f"{self.pk}. {self.app}.{self.name}"


def get_django_migrations(request):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    sql_query = "SELECT id, app, name, applied FROM django_migrations"

    cur.execute(sql_query)
    migrations = [Migration(*row) for row in cur]

    html_parts = [
        "<table>"
        "<thead><tr>"
        "<th>ID</th>"
        "<th>App</th>"
        "<th>Name</th>"
        "<th>Applied</th>"
        "</tr></thead>"
        "<tbody>"
    ]

    for migration in migrations:
        html_parts.append(
            "<tr>"
            f"<td>{migration.id}.</td>"
            f"<td>{migration.app}</td>"
            f"<td>{migration.name}</td>"
            f"<td>{migration.applied}</td>"
            "</tr>"
        )

    html_parts.append("</tbody></table>")

    cur.close()
    conn.close()

    return HttpResponse("".join(html_parts))
