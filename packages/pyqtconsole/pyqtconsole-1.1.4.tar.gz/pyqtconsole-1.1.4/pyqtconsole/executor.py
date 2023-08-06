from .qt.QtCore import QObject


class Executor(QObject):

    def spawn(self, func, *args):
        """Start task."""

    def interrupt(self):
        """Cancel current task."""

    def active(self):
        """Check if task is active."""

    def _wait(self, event):
        """Wait for more input."""


class ThreadExecutor(Executor):
    pass
