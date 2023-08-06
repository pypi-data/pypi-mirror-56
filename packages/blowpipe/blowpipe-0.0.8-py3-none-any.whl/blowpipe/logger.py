from datetime import datetime
import json

TRACE = "TRACE"
DEBUG = "DEBUG"
INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"

TRACE_ENABLED = False
DEBUG_ENABLED = True
INFO_ENABLED = True
WARN_ENABLED = True
ERROR_ENABLED = True
CONSOLE_ENABLED = False

GLOBAL_OBSERVERS = []


class LogLine:
    """
    Entry representing a log line
    """

    # log_level: debug/info/warn
    # class: the calling python code/class or Console
    # indent_level: integer indicates how to structure
    # created: datetime of date created
    # message: str of log message
    # err if an exception raised
    # workflow_id if present the owning workflow
    # run_id if present the owning run_id

    def __init__(
        self,
        log_level="",
        log_source="",
        indent_level="",
        created="",
        message="",
        workflow_id="",
        run_id="",
        username="",
        err="",
    ):
        if isinstance(log_level, dict):
            self.data = log_level
        else:
            self.data = {
                "log_level": log_level,
                "log_source": log_source,
                "indent_level": indent_level,
                "created": datetime.strftime(created, "%Y-%m-%d %H:%M:%S"),
                "message": message,
                "workflow_id": workflow_id,
                "run_id": run_id,
                "username": username,
                "err": err,
            }

    def is_log_level_or_higher(self, required_log_level):
        """
        a filter to check if the LogLine log_level (TRACE, DEBUG, INFO, WARN, ERROR)
        passes
        :param required_log_level:
        :return:
        """

        my_log_level = self.get_log_level()
        if required_log_level == TRACE:
            return True
        elif required_log_level == DEBUG:
            return my_log_level in [ DEBUG, INFO, WARN, ERROR ]
        elif required_log_level == INFO:
            return my_log_level in [ INFO, WARN, ERROR]
        elif required_log_level == WARN:
            return my_log_level in [ WARN, ERROR ]
        elif required_log_level == ERROR:
            return my_log_level == ERROR
        else:
            return False

    def get_log_level(self):
        return self.get("log_level", "")

    def get_log_source(self):
        return self.get("log_source", "")

    def get_indent_level(self):
        return self.get("indent_level", "")

    def get_workflow_id(self):
        return self.get("workflow_id", "")

    def get_run_id(self):
        return self.get("run_id", "")

    def get_username(self):
        return self.get("username", "")

    def get_created(self):
        return self.get("created", "")

    def get_message(self):
        return self.get("message", "")

    def get(self, key, default_value=""):
        return self.data.get(key) or default_value

    def to_json_string(self):
        return json.dumps(self.data)

    def to_tsv_string(self):
        line = self.data.get("created") + " " \
             + self.data.get("log_level") + " " \
             + self.data.get("log_source") + " " \
             + self.data.get("message")
        return line

    @staticmethod
    def from_string(source: str):
        data = json.loads(source)
        line = LogLine(data)
        return line


class Logger:
    """
    own-rolled lightweight logger
    """

    def __init__(self, log_source: str):
        # the source of the logs (code/class/function)
        self.log_source = log_source
        # how many tabs to indent when rendering flat
        self.indent_level = 0
        # who was doing the thing
        self.username = ""
        # what was being operated on
        self.workflow_id = ""
        # which run was it
        self.run_id = ""
        self.observers = []

    def set_workflow_id(self, workflow_id:str):
        self.workflow_id = workflow_id

    def set_run_id(self, run_id:str):
        self.run_id = run_id

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def get_observers(self):
        return self.observers

    @staticmethod
    def add_global_observer(observer):
        GLOBAL_OBSERVERS.append(observer)

    @staticmethod
    def remove_global_observer(observer):
        GLOBAL_OBSERVERS.remove(observer)

    def get_global_observers(self):
        return GLOBAL_OBSERVERS

    @staticmethod
    def console(msg):
        print(str(msg))
        entry = LogLine(
            log_level="DEBUG",
            log_source="Console",
            indent_level=0,
            created=datetime.today(),
            message=msg,
            workflow_id="",
            run_id="",
            username="",
            err="",
        )

        for observer in GLOBAL_OBSERVERS:
            observer.log(entry)

    def indent(self):
        self.indent_level += 1

    def unindent(self):
        self.indent_level -= 1

    def debug(self, msg:str):
        if DEBUG_ENABLED:
            self.log(DEBUG, datetime.today(), msg)

    def info(self, msg:str):
        if INFO_ENABLED:
            self.log(INFO, datetime.today(), msg)

    def warn(self, msg:str):
        if WARN_ENABLED:
            self.log(WARN, datetime.today(), msg)

    def trace(self, msg:str):
        if TRACE_ENABLED:
            self.log(TRACE, datetime.today(), msg)

    def error(self, msg:str, e:Exception):
        if ERROR_ENABLED:
            self.log(ERROR, datetime.today(), msg, e)

    def log(self, level:str, created:datetime, msg:str, err:str=""):
        entry = LogLine(
            log_level=level,
            log_source=self.log_source,
            indent_level=self.indent_level,
            created=created,
            message=str(msg),
            workflow_id=self.workflow_id,
            run_id=self.run_id,
            username=self.username,
            err=str(err)
        )

        if CONSOLE_ENABLED:
            print(entry.to_tsv_string())
            if err != "":
                print(str(err))

        for observer in self.observers:
            observer.log(entry)

        for observer in GLOBAL_OBSERVERS:
            observer.log(entry)


class FileWriterObserver:
    def __init__(self, filename: str):
        self.filename = filename

    def log(self, entry: LogLine):
        f = open(self.filename, "a")
        f.write(entry.to_json_string())
        f.write("\n")
        f.close()
