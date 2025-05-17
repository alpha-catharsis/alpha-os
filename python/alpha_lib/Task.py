import enum

class TaskState(enum.Enum):
    CREATED = 0
    RUNNING = 2
    SUCCESSFUL = 3
    FAILED = 4


class Task:
    def __init__(self, name, parent=None):
        self.name = name
        self.state = TaskState.CREATED
        self.parent = parent
        self.children = []

    def run(self, env):
        self.state = TaskState.RUNNING
        (result, message, newenv) = self._run(env)
        if result:
            self.state = TaskState.SUCCESSFUL
        else:
            self.state = TaskState.FAILED
        return (message, newenv)

    def successful(self):
        return self.state == TaskState.SUCCESSFUL

    def __rshift__(self, other):
        if isinstance(other, Task):
            other.parent = self
            self.children.append(other)
            return self
        else:
            raise ValueError("A task is required")

    def start_message(self):
        return None

    def end_message(self):
        return None

    def _run(self, env):
        raise NotImplementedError()


def execute(task, env, level=0, max_col=80):
    start_message = task.start_message()
    if start_message is not None:
        start_message.display(level, max_col)

    (run_message, newenv) = task.run(env)
    if run_message is not None:
        run_message.display(level, max_col)

    if task.successful():
        for child in task.children:
            execute(child, newenv, level + 1, max_col)
            if not child.successful:
                break

    end_message = task.end_message()
    if end_message is not None:
        end_message.display(level, max_col)

    return task.successful()
