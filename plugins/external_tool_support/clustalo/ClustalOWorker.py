from dataclasses import dataclass, field
from typing import Any, Dict, List


# ----------------------------
# Port
# ----------------------------
@dataclass
class PortDescriptor:
    id: str
    name: str
    description: str
    input: bool = True
    multi: bool = False
    data_type: str = "msa"


# ----------------------------
# Attribute
# ----------------------------
@dataclass
class Attribute:
    id: str
    type: str
    required: bool
    default: Any


# ----------------------------
# Actor Prototype
# ----------------------------
@dataclass
class ActorPrototype:
    id: str
    name: str
    description: str
    ports: List[PortDescriptor]
    attributes: List[Attribute]
    icon: str = ""
    external_tools: Dict[str, str] = field(default_factory=dict)

    def add_external_tool(self, tool, attribute):
        self.external_tools[tool] = attribute


# ----------------------------
# Worker
# ----------------------------
class ClustalOWorker:

    def __init__(self, config):
        self.config = config

    def execute(self, msa):

        print("Running Clustal Omega")

        print("Iterations:",
              self.config["num_iterations"])

        print("Guide Tree:",
              self.config["max_gt_iterations"])

        print("HMM:",
              self.config["max_hmm_iterations"])

        print("Input:", msa)

        # Call Clustal Omega executable here
        return "Aligned MSA"


# ----------------------------
# Worker Factory
# ----------------------------
class ClustalOWorkerFactory:

    ACTOR_ID = "clustalo"

    @staticmethod
    def init():

        ports = [

            PortDescriptor(
                id="input_msa",
                name="Input MSA",
                description="Input alignment",
                input=True
            ),

            PortDescriptor(
                id="output_msa",
                name="Output MSA",
                description="Aligned MSA",
                input=False,
                multi=True
            )
        ]

        attrs = [

            Attribute(
                "num_iterations",
                "int",
                False,
                1
            ),

            Attribute(
                "max_gt_iterations",
                "int",
                False,
                0
            ),

            Attribute(
                "max_hmm_iterations",
                "int",
                False,
                0
            ),

            Attribute(
                "set_auto",
                "bool",
                False,
                False
            ),

            Attribute(
                "tool_path",
                "string",
                True,
                "Default"
            ),

            Attribute(
                "tmp_dir",
                "string",
                True,
                "Default"
            )
        ]

        prototype = ActorPrototype(

            id=ClustalOWorkerFactory.ACTOR_ID,

            name="Align with Clustal Omega",

            description="Aligns multiple sequence alignments using Clustal Omega.",

            ports=ports,

            attributes=attrs,

            icon="clustalo.png"
        )

        prototype.add_external_tool(
            "clustalo",
            "tool_path"
        )

        WorkflowRegistry.register(prototype)

        return prototype

    @staticmethod
    def create_worker(config):

        return ClustalOWorker(config)


# ----------------------------
# Registry
# ----------------------------
class WorkflowRegistry:

    registry = {}

    @classmethod
    def register(cls, prototype):

        cls.registry[prototype.id] = prototype

        print("Registered:", prototype.name)


# ----------------------------
# Example
# ----------------------------
prototype = ClustalOWorkerFactory.init()

config = {
    "num_iterations": 5,
    "max_gt_iterations": 2,
    "max_hmm_iterations": 1,
    "tool_path": "/usr/bin/clustalo",
    "tmp_dir": "/tmp"
}

worker = ClustalOWorkerFactory.create_worker(config)

result = worker.execute("example_alignment.fasta")

print(result)


import os


class ClustalOWorker(BaseWorker):

    def __init__(self, actor, context):
        super().__init__(actor, context)

        self.input = None
        self.output = None
        self.cfg = ClustalOConfig()

    # -----------------------------------------
    # Equivalent of ClustalOWorker::init()
    # -----------------------------------------
    def init(self):
        self.input = self.ports["input_msa"]
        self.output = self.ports["output_msa"]

    # -----------------------------------------
    # Equivalent of ClustalOWorker::tick()
    # -----------------------------------------
    def tick(self):

        # -----------------------------------------
        # Is there a message?
        # -----------------------------------------
        if self.input.has_message():

            input_message = self.get_message_and_setup_script_values(
                self.input
            )

            # Empty message
            if input_message.is_empty():
                self.output.transit()
                return None

            # -----------------------------------------
            # Read Actor parameters
            # -----------------------------------------
            self.cfg.num_iterations = self.actor.get_parameter(
                "num_iterations"
            )

            self.cfg.max_guide_tree_iterations = self.actor.get_parameter(
                "max_gt_iterations"
            )

            self.cfg.max_hmm_iterations = self.actor.get_parameter(
                "max_hmm_iterations"
            )

            self.cfg.set_auto_options = self.actor.get_parameter(
                "set_auto"
            )

            self.cfg.number_of_processors = os.cpu_count()

            # -----------------------------------------
            # External tool path
            # -----------------------------------------
            tool_path = self.actor.get_parameter("tool_path")

            if tool_path.lower() != "default":
                ExternalToolRegistry.set_path(
                    "clustalo",
                    tool_path
                )

            # -----------------------------------------
            # Temporary directory
            # -----------------------------------------
            tmp_dir = self.actor.get_parameter("tmp_dir")

            if tmp_dir.lower() != "default":
                ApplicationSettings.set_temp_directory(
                    tmp_dir
                )

            # -----------------------------------------
            # Retrieve MSA from message
            # -----------------------------------------
            message_data = input_message.data

            msa_id = message_data["multiple_alignment"]

            msa_object = self.context.storage.get_msa_object(
                msa_id
            )

            if msa_object is None:
                raise RuntimeError("NULL MSA Object!")

            msa = msa_object.alignment

            # -----------------------------------------
            # Empty alignment?
            # -----------------------------------------
            if msa.is_empty():

                self.logger.error(
                    f"An empty MSA '{msa.name}' has been supplied."
                )

                return None

            # -----------------------------------------
            # Create task
            # -----------------------------------------
            support_task = ClustalOSupportTask(
                msa=msa,
                config=self.cfg
            )

            support_task.add_listeners(
                self.create_log_listeners()
            )

            task = NoFailTaskWrapper(
                support_task
            )

            task.on_state_changed(
                self.task_finished
            )

            return task

        # -----------------------------------------
        # Workflow finished
        # -----------------------------------------
        elif self.input.is_ended():

            self.set_done()

            self.output.set_ended()

        return None

    # -----------------------------------------
    # Slot equivalent
    # -----------------------------------------
    def task_finished(self, task):
        print("Task completed")