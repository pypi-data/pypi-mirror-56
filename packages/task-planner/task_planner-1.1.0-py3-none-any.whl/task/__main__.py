#!/usr/bin/env python3

# Copyright 2019 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.


import sqlite3

from os import system, name
from sys import argv


usage = '''usage: ./task.py [] [order] [add] [priority] [do] [done]

View all tasks:
./task.py
./task.py order <task|priority|status>

Add a task:
./task.py add "<name>"
./task.py add "<name>" priority <priority>

Set the priority of an existing task:
./task.py priority <priority> for <task id>

Set a task to doing:
./task.py do <task id>

Delete a task:
./task.py done <task id>
'''


def create_table_if_not_exists():
    with sqlite3.connect('tasks.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS "TASKS" (
            "ID"	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "TASK"	    TEXT NOT NULL,
            "PRIORITY"	INTEGER NOT NULL,
            "STATUS"	INTEGER NOT NULL
            );''')


def add_task():
    priority = 0

    if len(argv) >= 5:
        if argv[3] == 'priority':
            priority = argv[4]

    with sqlite3.connect('tasks.db') as connection:
        connection.cursor().execute('INSERT INTO TASKS (TASK, PRIORITY, STATUS) VALUES (?, ?, ?);',
                                    (argv[2], priority, 0))


def edit_priority():
    if argv[3] == 'for':
        with sqlite3.connect('tasks.db') as connection:
            connection.cursor().execute('UPDATE TASKS SET PRIORITY=? WHERE ID=?;', (argv[2], argv[4]))


def edit_status():
    with sqlite3.connect('tasks.db') as connection:
        connection.cursor().execute('UPDATE TASKS SET STATUS=1 WHERE ID=?;', (argv[2],))


def delete_task():
    with sqlite3.connect('tasks.db') as connection:
        connection.cursor().execute('DELETE FROM TASKS WHERE ID=?;', argv[2], )


def print_tasks(order_by=''):
    _clear()

    with sqlite3.connect('tasks.db') as connection:
        cursor = connection.cursor()

        if order_by != '':
            order_how = 'DESC'
            if order_by == 'TASK':
                order_how = 'ASC'
            sql = 'SELECT * FROM TASKS ORDER BY {} {};'.format(order_by, order_how)
        else:
            sql = 'SELECT * FROM TASKS;'

        max_id = 0
        for x in cursor.execute('SELECT MAX(ID) FROM TASKS;'):
            max_id = x[0]

        offset_id = len(str(max_id))
        print('ID', ' ' * offset_id, 'Task', ' ' * 40, 'Priority', 'Status')
        print('-' * (offset_id + 65))

        for task_id, task, priority, status in cursor.execute(sql):
            print(task_id, ' ' * (offset_id + len(str(task_id))), task, ' ' * (44 - len(task)), priority, ' ' * 6,
                  'TODO' if status == 0 else 'DOING')


def _clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


if __name__ == '__main__':
    create_table_if_not_exists()
    if len(argv) >= 3:
        if argv[1] == 'add':
            add_task()
        elif argv[1] == 'priority':
            edit_priority()
        elif argv[1] == 'do':
            edit_status()
        elif argv[1] == 'done':
            delete_task()
        elif argv[1] == 'order':
            order = ''
            if argv[2] == 'priority':
                order = 'PRIORITY'
            elif argv[2] == 'status':
                order = 'STATUS'
            elif argv[2] == 'task':
                order = 'TASK'
            print_tasks(order)
        else:
            print(usage)
    elif len(argv) == 1:
        print_tasks()
    else:
        print(usage)
