import grpc
import blowpipe
from blowpipe import model, exceptions
from blowpipe.protos import services_pb2_grpc
from blowpipe.config import BlowpipeClientConfig


class GRPCClient:
    def __init__(self, config:BlowpipeClientConfig=None):
        if config is None:
            config = BlowpipeClientConfig()
        self.config = config
        self.ip = None
        self.port = None
        self.channel = None
        self.stub = None

    def connect(self):
        config = self.config
        self.ip = config.get_grpc_client_ip()
        self.port = config.get_grpc_port()
        address = self.ip + ":" + str(self.port)
        self.channel = grpc.insecure_channel(address)
        self.stub = services_pb2_grpc.BlowpipeStub(self.channel)

    def check_connect(self):
        """
        raises an exception if we haven't called connect
        :return:
        """
        if self.stub is None:
            raise exceptions.BlowpipeError("Not connected.")

    def Status(self, since=-1):
        self.check_connect()
        result = self.stub.Status(blowpipe.protos.objects_pb2.Timestamp(value=since))
        return result

    def ManualTrigger(self, workflow_id):
        self.check_connect()
        request = blowpipe.protos.objects_pb2.ManualTriggerRequest(id=workflow_id)
        response = self.stub.ManualTrigger(request)
        return response

    def SetState(self, request):
        self.check_connect()
        return self.stub.SetState(request)

    def ListWorkflows(self, is_deleted=False):
        self.check_connect()
        results = self.stub.ListWorkflows(blowpipe.protos.objects_pb2.ListWorkflowsRequest(include_deleted=is_deleted))
        out = []
        for result in results:
            out.append(result)
        return out

    def ListWorkflowHistory(self, workflow_id):
        self.check_connect()
        results = self.stub.ListWorkflowHistory(blowpipe.protos.objects_pb2.ID(id=workflow_id))
        out = []
        for result in results:
            out.append(result)
        return out

    def ListRunningWorkflows(self, include_completed=False, since=None):
        self.check_connect()
        results = self.stub.ListRunningWorkflows(blowpipe.protos.objects_pb2.ListRunningWorkflowsRequest(include_completed=include_completed, since=since))
        out = []
        for result in results:
            out.append(result)
        return out

    def GetLog(self, grep, grepv, log_level, username, workflow_id, run_id, date_from, date_to, tail):
        self.check_connect()
        # in the server, attach a temporary logger to the Logger
        # route all to the yield
        # on CTRL-C somehow trap and remove the temporary logger from the route
        # perhaps this is on error - the only acceptable error is to remove the trap?
        request = blowpipe.protos.objects_pb2.GetLogRequest()
        request.grep = grep
        request.grepv = grepv
        request.log_level = log_level
        request.username = username
        request.workflow_id = workflow_id
        request.run_id = run_id
        request.date_from = date_from
        request.date_to = date_to
        request.tail = tail
        for response in self.stub.GetLog(request):
            yield response

    def AddWorkflow(self, workflow):
        self.check_connect()
        workflow_rpc = blowpipe.protos.objects_pb2.Workflow(id="", yaml=workflow.to_yaml())
        reply = self.stub.AddWorkflow(workflow_rpc)
        return reply

    def GetWorkflow(self, workflow_id, version=0):
        self.check_connect()
        response = self.stub.GetWorkflow(blowpipe.protos.objects_pb2.GetWorkflowRequest(id=workflow_id, version=version))
        if response.success:
            workflow = model.Workflow()
            workflow.load_raw(response.workflow.yaml)
            return workflow
        else:
            return None

    def UpdateWorkflow(self, workflow_id, workflow, reason):
        self.check_connect()
        request = blowpipe.protos.objects_pb2.UpdateWorkflowRequest(id=workflow_id, yaml=workflow.to_yaml(), reason=reason)
        return self.stub.UpdateWorkflow(request)

    def DeleteWorkflow(self, workflow_id):
        self.check_connect()
        return self.stub.DeleteWorkflow(blowpipe.protos.objects_pb2.ID(id=workflow_id))

    def GetAllConfig(self):
        self.check_connect()
        results = []
        request = blowpipe.protos.objects_pb2.Timestamp(value=-1)
        for c in self.stub.GetAllConfig(request):
            results.append(c)
        return results

    def GetConfig(self, key):
        self.check_connect()
        return self.stub.GetConfig(blowpipe.protos.objects_pb2.GetConfigRequest(key=key))

    def SetConfig(self, key, value):
        self.check_connect()
        return self.stub.SetConfig(blowpipe.protos.objects_pb2.SetConfigRequest(key=key, value=value))

    def DeleteConfig(self, key):
        self.check_connect()
        return self.stub.DeleteConfig(blowpipe.protos.objects_pb2.DeleteConfigRequest(key=key))
