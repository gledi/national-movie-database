import sqlite3

from django.http import Http404
from django.shortcuts import render


_db_path = '/home/gledi/Source/DataGripProjects/actors/actors.db'

class Actor:
    def __init__(self, id, name, bio):
        self.id = id
        self.name = name
        self.bio = bio


def get_actor_list(request):
    conn = sqlite3.connect(_db_path)
    cur = conn.cursor()
    cur.execute("select id, name, bio from actors")
    actors = [Actor(*row) for row in cur]
    cur.close()
    conn.close()
    return render(request, "movies/actor_list.html", context={
        "actors": actors
    })


def get_actor_detail(request, id):
    conn = sqlite3.connect(_db_path)
    cur = conn.cursor()
    cur.execute(f"select id, name, bio from actors where id = ?", (id,))
    row = cur.fetchone()
    if row is None:
        raise Http404("Actor not found")
    return render(request, "movies/actor_detail.html", context={
        "actor": Actor(*row)
    })
