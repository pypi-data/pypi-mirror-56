# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys
import threading
import time
from collections import defaultdict
from collections import deque
from copy import deepcopy


import typing
import pytest
def _ensure_hashable(input: typing.Union[typing.List[str], typing.Tuple[str, ...], str]) -> typing.Union[typing.Tuple[str, ...], str]:
    if isinstance(input, list):
        return tuple(input)
    return input


BUFFER = typing.Union[None, io.BytesIO, io.StringIO]
OPTIONAL_TEXT_OR_ITERABLE = typing.Union[str, bytes, None, typing.List[typing.Union[str, bytes]], typing.Tuple[typing.Union[str, bytes], ...]]
OPTIONAL_TEXT = typing.Union[str, bytes, None]
class FakePopen:
    """Base class that fakes the real subprocess.Popen()"""
    args: typing.Union[typing.List[str], typing.Tuple[str, ...], str]
    __stdout: OPTIONAL_TEXT_OR_ITERABLE
    __stderr: OPTIONAL_TEXT_OR_ITERABLE
    __returncode: typing.Optional[int]
    __wait: typing.Optional[float]
    __universal_newlines: typing.Optional[bool]
    __callback: typing.Optional[typing.Optional[typing.Callable]]
    __thread: typing.Optional[threading.Thread]
    stdout: BUFFER = None
    stderr: BUFFER = None
    returncode: typing.Optional[int] = None
    text_mode: bool = False
    pid: int = 0

    def __init__(
        self,
        command: typing.Union[typing.Tuple[str, ...], str],
        stdout: OPTIONAL_TEXT_OR_ITERABLE = None,
        stderr: OPTIONAL_TEXT_OR_ITERABLE = None,
        returncode: int = 0,
        wait: typing.Optional[float] = None,
        callback: typing.Optional[typing.Callable] = None,
        **_: typing.Dict[str, typing.Any]
    ) -> None:
        self.args = command
        self.__stdout = stdout
        self.__stderr = stderr
        self.__returncode = returncode
        self.__wait = wait
        self.__thread = None
        self.__callback = callback

    def __enter__(self) -> 'FakePopen':
        return self

    def __exit__(self, *args: typing.List, **kwargs: typing.Dict) -> None:
        pass

    def communicate(self, input: OPTIONAL_TEXT = None, timeout: typing.Optional[float] = None) -> typing.Tuple[typing.Any, typing.Any]:
        return (
            self.stdout.getvalue() if self.stdout else None,
            self.stderr.getvalue() if self.stderr else None,
        )

    def poll(self) -> None:
        return self.returncode

    def wait(self, timeout: typing.Optional[float] = None) -> int:
        # todo: make it smarter and aware of time left
        if timeout and timeout < self.__wait:
            raise subprocess.TimeoutExpired(self.args, timeout)
        if self.__thread is not None:
            self.__thread.join()
        return self.returncode

    def configure(self, **kwargs: typing.Optional[typing.Dict]) -> None:
        """Setup the FakePopen instance based on a real Popen arguments."""
        self.__universal_newlines = kwargs.get("universal_newlines", None)
        text = kwargs.get("text", None)

        if text and sys.version_info < (3, 7):
            raise TypeError("__init__() got an unexpected keyword argument 'text'")

        self.text_mode = bool(text or self.__universal_newlines)

        # validation taken from the real subprocess
        if (
            text is not None
            and self.__universal_newlines is not None
            and bool(self.__universal_newlines) != bool(text)
        ):
            raise subprocess.SubprocessError(
                "Cannot disambiguate when both text "
                "and universal_newlines are supplied but "
                "different. Pass one or the other."
            )

        if kwargs.get("stdout") == subprocess.PIPE:
            self.stdout = self._prepare_buffer(self.__stdout)
        stderr = kwargs.get("stderr")
        if stderr == subprocess.STDOUT:
            self.stdout = self._prepare_buffer(self.__stderr, self.stdout)
        elif stderr == subprocess.PIPE:
            self.stderr = self._prepare_buffer(self.__stderr)

    def _prepare_buffer(self, input: typing.Union[str, bytes, None], io_base: BUFFER = None) -> io.BytesIO:
        linesep = self._convert(os.linesep)
        if io_base is None:
            io_base = io.StringIO() if self.text_mode else io.BytesIO()

        if input is None:
            return io_base

        if isinstance(input, (list, tuple)):
            input = linesep.join(map(self._convert, input))

        if isinstance(input, str) and not self.text_mode:
            input = input.encode()

        if isinstance(input, bytes) and self.text_mode:
            input = input.decode()

        if not input.endswith(linesep):
            input += linesep

        if self.text_mode and self.__universal_newlines:
            input = input.replace("\r\n", "\n")
        io_base.write(input)
        return io_base

    def _convert(self, input: typing.Union[str, bytes]) -> typing.Union[str, bytes]:
        if isinstance(input, bytes) and self.text_mode:
            return input.decode()
        if isinstance(input, str) and not self.text_mode:
            return input.encode()
        return input

    def _wait(self, wait_period: float) -> None:
        time.sleep(wait_period)
        if self.returncode is None:
            self._finish_process()

    def run_thread(self) -> None:
        """Run the user-defined callback or wait in a thread."""
        if self.__wait is None and self.__callback is None:
            self._finish_process()
        else:
            if self.__callback:
                self.__thread = threading.Thread(target=self.__callback, args=(self,))
            else:
                self.__thread = threading.Thread(target=self._wait, args=(self.__wait,))
            self.__thread.start()

    def _finish_process(self) -> None:
        self.returncode = self.__returncode

        if self.stdout:
            self.stdout.seek(0)

        if self.stderr:
            self.stderr.seek(0)


class ProcessNotRegisteredError(Exception):
    """
    Raised when the attempted command wasn't registered before.
    Use `fake_process.allow_unregistered(True)` if you want to use real subprocess.
    """


class ProcessDispatcher:
    """Main class for handling processes."""

    process_list: typing.List['FakeProcess'] = []
    built_in_popen: typing.Optional[typing.Optional[typing.Callable]] = None
    _allow_unregistered: bool = False
    _cache: typing.Dict[FakeProcess, typing.Dict[FakeProcess, typing.Any]] = dict()
    _keep_last_process: bool = False
    _pid: bool = 0

    @classmethod
    def register(cls, process: 'FakeProcess') -> None:
        if not cls.process_list:
            cls.built_in_popen = subprocess.Popen
            subprocess.Popen = cls.dispatch
        cls._cache[process] = {
            proc: deepcopy(proc.definitions) for proc in cls.process_list
        }
        cls.process_list.append(process)

    @classmethod
    def deregister(cls, process: 'FakeProcess') -> None:
        cls.process_list.remove(process)
        cache = cls._cache.pop(process)
        for proc, processes in cache.items():
            proc.definitions = processes
        if not cls.process_list:
            subprocess.Popen = cls.built_in_popen
            cls.built_in_popen = None

    @classmethod
    def dispatch(cls, command: typing.Union[typing.Tuple[str, ...], str], **kwargs: typing.Optional[typing.Dict]) -> FakePopen:
        """This method will be used instead of the subprocess.Popen()"""
        command = _ensure_hashable(command)

        processes, process_instance = cls._get_process(command)

        if not processes:
            if not cls._allow_unregistered:
                raise ProcessNotRegisteredError(
                    "The process '%s' was not registered."
                    % (command if isinstance(command, str) else " ".join(command),)
                )
            else:
                return cls.built_in_popen(command, **kwargs)

        process = processes.popleft()
        if not processes and process_instance:
            if cls._keep_last_process:
                processes.append(process)
            else:
                del process_instance.definitions[command]

        cls._pid += 1
        if process is True:
            return cls.built_in_popen(command, **kwargs)

        result = FakePopen(**process)
        result.pid = cls._pid
        result.configure(**kwargs)
        result.run_thread()
        return result

    @classmethod
    def _get_process(cls, command: str) -> typing.Tuple[typing.Optional[typing.Deque[typing.Dict]], typing.Optional['FakeProcess']]:
        for proc in reversed(cls.process_list):
            processes = proc.definitions.get(command)
            process_instance = proc
            if processes:
                return processes, process_instance
        return None, None

    @classmethod
    def allow_unregistered(cls, allow: bool) -> None:
        cls._allow_unregistered = allow

    @classmethod
    def keep_last_process(cls, keep: bool) -> None:
        cls._keep_last_process = keep


class IncorrectProcessDefinition(Exception):
    """Raised when the register_subprocess() has been called with wrong arguments"""


class FakeProcess:
    """Class responsible for tracking the processes"""
    definitions: typing.DefaultDict[str, typing.Deque[typing.Union[typing.Dict, bool]]]
    def __init__(self) -> None:
        self.definitions = defaultdict(deque)

    def register_subprocess(
        self,
        command: typing.Union[typing.List[str], typing.Tuple[str, ...], str],
        stdout: OPTIONAL_TEXT_OR_ITERABLE = None,
        stderr: OPTIONAL_TEXT_OR_ITERABLE = None,
        returncode: int = 0,
        wait: typing.Optional[float] = None,
        callback: typing.Optional[typing.Callable] = None,
        occurrences: int = 1
    ) -> None:
        """
        Main method for registering the subprocess instances.

        Args:
            command: register the command that will be faked
            stdout: value of the standard output
            stderr: value of the error output
            returncode: return code of the faked process
            wait: artificially wait for the process to finish
            callback: function that will be executed instead of the process
            occurrences: allow multiple usages of the same command
        """
        if wait is not None and callback is not None:
            raise IncorrectProcessDefinition(
                "The 'callback' and 'wait' arguments cannot be used "
                "together. Add sleep() to your callback instead."
            )
        command = _ensure_hashable(command)
        self.definitions[command].extend(
            [
                {
                    "command": command,
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": returncode,
                    "wait": wait,
                    "callback": callback,
                }
            ]
            * occurrences
        )

    def pass_command(self, command: typing.Union[typing.List[str], typing.Tuple[str, ...], str], occurrences: int = 1) -> None:
        """
        Allow to use a real subprocess together with faked ones.

        Args:
            command: allow to execute the supplied command
            occurrences: allow multiple usages of the same command
        """
        command = _ensure_hashable(command)
        self.definitions[command].extend([True] * occurrences)

    def __enter__(self) -> 'FakeProcess':
        ProcessDispatcher.register(self)
        return self

    def __exit__(self, *args: typing.List, **kwargs: typing.Dict) -> None:
        ProcessDispatcher.deregister(self)

    def allow_unregistered(cls, allow: bool) -> None:
        """
        Allow / block unregistered processes execution. When allowed, the real
        subprocesses will be called. Blocking will raise the exception.

        Args:
            allow: decide whether the unregistered process shall be allowed
        """
        ProcessDispatcher.allow_unregistered(allow)

    @classmethod
    def keep_last_process(cls, keep: bool) -> None:
        """
        Keep last process definition from being removed. That can allow / block
        multiple execution of the same command.

        Args:
            keep: decide whether last process shall be kept
        """
        ProcessDispatcher.keep_last_process(keep)

    @classmethod
    def context(cls) -> 'FakeProcess':
        """Return a new FakeProcess instance to use it as a context manager."""
        return cls()
