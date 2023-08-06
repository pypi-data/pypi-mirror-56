import os
import blowpipe
from blowpipe import constants
from blowpipe import bp_utils
from blowpipe import model
from blowpipe.protos import services_pb2_grpc
from blowpipe import client_grpc
from blowpipe import logger
from blowpipe import bootstrap


class BlowpipeClient:
    def __init__(self, config):
        self.config = config

    def get_method(self, method_name):
        try:
            method_to_call = getattr(self, method_name)
            if method_to_call is not None:
                return method_to_call
            else:
                return None
        except:
            return None

    def check_connection(self):
        try:
            client = client_grpc.GRPCClient(self.config)
            client.connect()
            client.Status()
            return True, client
        except Exception:
            print("Server is unavailable at " + self.config.get_grpc_client_ip() + ":" + str(self.config.get_grpc_port()))
            return False, None

    def ping(self):
        """
        establishes connection with server, returning a tuple containing
        the result and the client
        """
        try:
            client = client_grpc.GRPCClient(self.config)
            client.Status()
            return True, client
        except Exception:
            return False, None

    def do_init(self, cli) -> bool:
        """
        initialises the blowpipe.cfg and .db files
        The autodiscover logic will attempt to find in order
        A CLI parameter, the BLOWPIPE_HOME directory or the current directory
        :return:
        """
        filename = bootstrap.autodiscover_config_file()
        if os.path.isfile(filename):
            # already exists, won't init.
            logger.Logger.console("Error, '" + filename + "' already exists, won't init.")
            return False
        else:
            bootstrap.init(filename)
            logger.Logger.console("Successfully initialised blowpipe at " + filename)
            return True

    def do_config(self, cli):
        result, client = self.check_connection()
        if not result:
            return False

        subcommand = cli.get_or_die("config", "You must specify 'get', 'set' or 'rm'")
        if subcommand == "ls":
            all_config = client.GetAllConfig()
            arrs = []
            for c in all_config:
                arr = [c.key, c.value]
                arrs.append(arr)

            from tabulate import tabulate

            print(tabulate(arrs, headers=["Key", "Value"]))
            return True

        elif subcommand == "get":
            key = cli.get_or_default(subcommand, None)
            key = cli.get_or_die(subcommand, "You must specify a configuration key.")
            response = client.GetConfig(key)
            if response.success:
                print(response.value)

            else:
                print("No such key '" + key + "'")
                return False

        elif subcommand == "set":
            key = cli.get_or_die(subcommand, "You must specify a configuration key.")
            value = cli.get_or_die(key, "You must specify a configuration value.")
            if os.path.isfile(value):
                f = open(value)
                content = f.read()
                f.close()
                client.SetConfig(key, content)
            else:
                client.SetConfig(key, value)
            return True

        elif subcommand == "rm":
            key = cli.get_or_die(subcommand, "You must specify a configuration key.")
            client.DeleteConfig(key)
            return True
        else:
            print("You must specify 'get', 'set' or 'rm'")
            return False

    def do_status(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        response = client.Status()
        print(response.message)
        return True

    def do_context(self, cli):
        ctx = cli.get_or_default("context", None)
        if ctx is None:
            # print the current context
            print(self.config.get_context())
        else:
            self.config.set_context(ctx)
            self.config.save()
        return True

    def do_add(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        filename = cli.get_or_die("add")
        workflow = model.Workflow()
        workflow.load_file(filename)
        response = client.AddWorkflow(workflow)
        print("Success, added '" + filename + "', id=" + response.id)
        return True

    def do_update(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("update")
        filename = cli.get_or_die(workflow_id)
        reason = cli.get_or_die("-reason")
        workflow = model.Workflow()
        workflow.load_file(filename)
        response = client.UpdateWorkflow(workflow_id, workflow, reason)
        print("OK, updated '" + response.id + "'.")
        return True

    def do_enable(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("enable")
        request = blowpipe.protos.objects_pb2.SetStateRequest(
            id=workflow_id, state=constants.STATE_ENABLED
        )
        response = client.SetState(request)
        if response.success:
            print("OK, enabled '" + response.id + "'.")
            return True
        else:
            print("Failed, did not enable the workflow, msg=" + response.message)
            return False

    def do_disable(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("disable")
        request = blowpipe.protos.objects_pb2.SetStateRequest(
            id=workflow_id, state=constants.STATE_DISABLED
        )
        response = client.SetState(request)
        if response.success:
            print("OK, enabled '" + response.id + "'.")
            return True
        else:
            print("Failed, did not disable the workflow, msg=" + response.message)
            return False

    def do_ls(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        is_deleted = cli.contains("-d")
        workflows = client.ListWorkflows(is_deleted)
        if len(workflows) == 0:
            print("Blowpipe is empty.")
        else:
            arrs = []
            for result in workflows:

                workflow = model.Workflow()
                workflow.load_raw(result.yaml)

                arr = [
                    result.id,
                    workflow.get_name(),
                    result.version,
                    result.last_modified,
                    result.created,
                    result.is_enabled,
                    result.is_deleted,
                ]
                arrs.append(arr)

                """
                msg = result.id + "\t" + workflow.name() + "\t" + str(result.version) + "\t" + result.last_modified + "\t" + result.created + "\t"
                if result.is_enabled:
                    msg += " ENABLED"
                else:
                    msg += " DISABLED"

                if result.is_deleted:
                    msg += " DELETED "
                print(msg)
                """

            from tabulate import tabulate

            print(
                tabulate(
                    arrs,
                    headers=[
                        "ID",
                        "Name",
                        "Version",
                        "Last Modified",
                        "Created",
                        "Enabled",
                        "Deleted",
                    ],
                )
            )
        return True

    def do_rm(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("rm")
        result = client.DeleteWorkflow(workflow_id)
        print("OK.")
        return True

    def do_ps(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        from tabulate import tabulate

        include_completed = cli.contains("-a")
        since = None
        results = client.ListRunningWorkflows(include_completed, since)
        arrs = []
        for result in results:
            workflow_yaml = result.workflow.yaml
            workflow = blowpipe.model.Workflow(workflow_yaml)
            arr = [
                result.id,
                workflow.get_name(),
                result.state,
                result.created,
                result.last_modified,
            ]
            arrs.append(arr)
        arrs.reverse()
        print(
            tabulate(
                arrs, headers=["run_id", "Name", "State", "Created", "Last Modified"]
            )
        )
        return True

    def do_rename(self, cli):
        result, client = self.check_connection()
        if not result:
            return False

        workflow_id = cli.get_or_die("rename")
        new_name = cli.get_or_die(workflow_id)
        workflow = client.GetWorkflow(workflow_id)
        if workflow is not None:
            old_name = workflow.get_name()
            workflow.set_name(new_name)
            response = client.UpdateWorkflow(
                workflow_id,
                workflow,
                "Renamed (was '" + old_name + "', is now '" + new_name + "').",
            )
            print("OK, renamed '" + response.id + "'.")
            return True
        else:
            print("No such workflow " + workflow_id + ".")
            return False

    def do_describe(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("describe")
        new_desc = cli.get_or_die(workflow_id)
        workflow = client.GetWorkflow(workflow_id)
        old_desc = workflow.get_description()
        workflow.set_description(new_desc)
        response = client.UpdateWorkflow(workflow_id, workflow, "Updated description.")
        print("OK, updated description '" + response.id + "'.")
        return True

    def do_cp(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        print("cp")
        return True

    def do_cat(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("cat")
        version = int(cli.get_or_default("-version", 0))
        result = client.GetWorkflow(workflow_id, version)
        if result is not None:
            print(result.to_yaml())
            return True
        else:
            print("No such workflow.")
            return False

    def do_history(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("history")
        results = client.ListWorkflowHistory(workflow_id)
        from tabulate import tabulate

        arrs = []
        for result in results:
            arr = [result.version, result.date, result.reason]
            arrs.append(arr)
        arrs.reverse()
        print(tabulate(arrs, headers=["Version", "Date", "Reason"]))
        return True

    def do_pause(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        print("pause")
        return True

    def do_resume(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        print("resume")
        return True

    def do_log(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        grep = cli.get_or_default("-grep", "")
        grepv = cli.get_or_default("-grepv", "")
        username = cli.get_or_default("-username", "")
        workflow_id = cli.get_or_default("-workflow_id", "")
        log_level = cli.get_or_default("-level", "DEBUG").upper()
        run_id = cli.get_or_default("-run_id", "")
        date_to = cli.get_or_default("-to", "")
        date_from = cli.get_or_default("-from", "")
        tail = cli.contains("-f")
        try:
            for response in client.GetLog(
                grep, grepv, log_level, username, workflow_id, run_id, date_from, date_to, tail
            ):
                log_line = logger.LogLine.from_string(response.log_message.strip())
                print(log_line.get_created() + " " \
                    + log_line.get_log_level() + " " \
                    + log_line.get_log_source() + " " \
                    + log_line.get_message() )
        except KeyboardInterrupt as ke:
            # this is okay
            pass
        return True

    def do_trigger(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        workflow_id = cli.get_or_die("trigger")
        response = client.ManualTrigger(workflow_id)
        if response.success:
            print(
                "Blowpipe trigger "
                + workflow_id
                + " success!\nRun ID is "
                + response.run_id
            )
            return True
        else:
            print("Failed to trigger: " + response.message)
            return False

    def do_validate(self, cli):
        result, client = self.check_connection()
        if not result:
            return False
        print("validate")
        return True

    def do_version(self):
        msg = "blowpipe client version " + constants.CLIENT_VERSION
        print(msg)
        return True

    def usage(self, cli=None):
        bp_utils.print_logo()
        LJUST = 20
        msg = "Blowpipe is a tool for data processing pipelines."
        msg += "\n"
        msg += "\nUsage:"
        msg += "\n"
        msg += "\n\tblowpipe <command> [arguments]"
        msg += "\n"
        msg += "\nThe commands are:"
        msg += "\n"
        msg += "\n\tadd".ljust(LJUST) + "add a workflow"
        msg += (
            "\n\tconfig".ljust(LJUST)
            + "(ls|get|set|rm) manages server configuration values"
        )
        msg += "\n\t*cancel".ljust(LJUST) + "cancels a job"
        msg += "\n\t*context".ljust(LJUST) + "manages client context"
        msg += "\n\tcat".ljust(LJUST) + "print the workflow definition to STDOUT"
        msg += "\n\t*disable".ljust(LJUST) + "disable a workflow"
        msg += "\n\tdescribe".ljust(LJUST) + "alter the description of a workflow"
        msg += "\n\t*enable".ljust(LJUST) + "enable a workflow"
        msg += "\n\thistory".ljust(LJUST) + "show revision history for workflow"
        msg += "\n\tinit".ljust(LJUST) + "initialise the db and home directory"
        msg += "\n\tls".ljust(LJUST) + "list workflows"
        msg += "\n\tlog".ljust(LJUST) + "prints logs"
        msg += "\n\tps".ljust(LJUST) + "list jobs"
        msg += "\n\t*pause".ljust(LJUST) + "force a job to pause processing"
        msg += "\n\t*rm".ljust(LJUST) + "delete a workflow"
        msg += "\n\t*resume".ljust(LJUST) + "mark a job to resume processing"
        msg += "\n\trename".ljust(LJUST) + "rename a workflow"
        msg += "\n\t*repository".ljust(LJUST) + "(ls|add|rm) manages repository"
        msg += "\n\tstatus".ljust(LJUST) + "print status of the server"
        msg += "\n\tserver".ljust(LJUST) + "run a blowpipe server"
        msg += (
            "\n\ttrigger".ljust(LJUST) + "forces a workflow to commence (starts a job)"
        )
        msg += "\n\tupdate".ljust(LJUST) + "update an existing workflow"
        msg += "\n\tversion".ljust(LJUST) + "prints out the version of the client"
        msg += "\n"
        msg += "\n"
        msg += 'Use "blowpipe help <command>" for more information about the command.'
        msg += "\n\t(* not implemented)"
        msg += "\n"
        print(msg)
        return True

    def help_add(self):
        print("usage: blowpipe add <FILE | URL>")
        print("Adds a yaml workflow definition into the server.")
        print("")

    def help_update(self):
        print("usage: blowpipe update $WORKFLOW_ID <FILE | URL>")
        print("Updates a workflow yaml.")
        print("")

    def help_cat(self):
        print("usage: blowpipe cat $WORKFLOW_ID")
        print("Prints the yaml config of a workflow to STDOUT.")
        print("")

    def help_cancel(self):
        print("usage: blowpipe cancel $RUN_ID")
        print("Cancels a running job.")
        print("")

    def help_describe(self):
        print('usage: blowpipe describe $WORKFLOW_ID "The description"')
        print("Updates the description of a workflow.")
        print("")

    def help_enable(self):
        print("usage: blowpipe enable $WORKFLOW_ID")
        print(
            "Enables a workflow meaning it can run when triggered or schedules are met."
        )
        print("")

    def help_disable(self):
        print("usage: blowpipe enable $WORKFLOW_ID")
        print("Disables a workflow - this will not respond to triggers or schedules.")
        print("")

    def help_history(self):
        print("usage: blowpipe history $WORKFLOW_ID")
        print("Shows a list of all changes to a workflow.")
        print("")

    def help_ls(self):
        print("usage: blowpipe ls")
        print("Shows a list of all workflow definitions")
        print("")

    def help_ps(self):
        print("usage: blowpipe ps (-a)")
        print("Shows a list of all running jobs (-a shows completed jobs.")
        print("")

    def help_pause(self):
        print("usage: blowpipe pause $RUN_ID")
        print(
            "Marks a runnning job to pause.  Existing steps will complete then the workflow will halt."
        )
        print("")

    def help_rm(self):
        print("usage: blowpipe rm $WORKFLOW_ID")
        print("Deletes a workflow.")
        print("")

    def help_rename(self):
        print('usage: blowpipe rename $WORKFLOW_ID "The new name"')
        print("Renames a workflow.")
        print("")

    def help_rename(self):
        print('usage: blowpipe rename $WORKFLOW_ID "The new name"')
        print("Renames a workflow.")
        print("")

    def help_trigger(self):
        print("usage: blowpipe trigger $WORKFLOW_ID")
        print("Manually forces a workflow to commence.")
        print("")

    def help_resume(self):
        print("usage: blowpipe resume $RUN_ID")
        print("Marks a runnning job to resume.  Remaining steps will then start.")
        print("")

    def help_log(self, cli):
        msg = "usage: blowpipe log"
        msg += "Prints server logs with filtering."
        msg += "\n\t    -run_id XXX "
        msg += "\n\t    -workflow_id XXXXX "
        msg += "\n\t    -level TRACE|(DEBUG)|INFO|WARN|ERROR "
        msg += "\n\t    -grep \"xxxx\" "
        msg += "\n\t    -grepv \"xxxx\" "
        msg += "\n\t    -to \"yyyy-mm-dd hh:mm:ss\" "
        msg += "\n\t    -from \"yyyy-mm-dd hh:mm:ss\" "
        msg += "\n\t    -username xxxxx"
        msg += "\n\t    -format json|(text)  - controls output format."
        msg += "\n"
        print(msg)

    def test(self, cli):
        client = client_grpc.GRPCClient(self.config)
        return True

    def process(self, cli):
        if len(cli.argv) == 1:
            self.usage()
            return False
        command = cli.get_command()
        if command == "":
            self.usage()
            return False

        fn_name = "do_" + command
        method_to_call = self.get_method(fn_name)
        if method_to_call is not None:
            return method_to_call(cli)
        else:
            print("I don't know how to '" + command + "'")
            return False

    def do_help(self, cli):
        command = cli.get_or_default("help", "")
        fn_name = "help_" + command
        method_to_call = getattr(self, fn_name)
        if method_to_call is not None:
            method_to_call(cli)
            return True
        else:
            print("I don't have any help for '" + command + "'")
            return False
