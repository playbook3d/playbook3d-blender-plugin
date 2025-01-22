import bpy
import queue


execution_queue = queue.Queue()


def execute_queued_functions():
    while not execution_queue.empty():
        function = execution_queue.get()
        function()
    return 0.2


def add(function):
    execution_queue.put(function)


def register():
    if not bpy.app.timers.is_registered(execute_queued_functions):
        bpy.app.timers.register(execute_queued_functions)


def unregister():
    if bpy.app.timers.is_registered(execute_queued_functions):
        bpy.app.timers.unregister(execute_queued_functions)
