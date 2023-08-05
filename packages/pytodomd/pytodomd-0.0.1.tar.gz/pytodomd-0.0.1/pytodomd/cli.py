#!/usr/bin/env python

import click

import pytodomd

@click.command()
@click.argument('filepath')
def main(filepath):
	"""
	PyTodoMd CLI

	Parse TODO.md file and display it's contents.

	FILEPATH is the path of the TODO.md file.
	"""
	todo_lists = pytodomd.from_file(filepath)

	for todo_list in todo_lists:
		click.echo('\n' + todo_list.title)
		for todo in todo_list.todos:
			click.echo(f"- [{'x' if todo.completed else ' '}] {todo.text}")

if __name__ == '__main__':
	main()
