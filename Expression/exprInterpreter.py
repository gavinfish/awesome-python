import re
from log import gen_log
from instruction import InstructionFactory
from instruction import ReturnInstruction


class ExprInterpreter(object):
    methods = []
    variable_map = {}

    def interpret(self):
        data = self.load_data("example-list.ll")
        m = self.get_methods(data)
        for target in m:
            commands = self.get_commands(target)
            for command in commands:
                instruct = InstructionFactory.parse(command)
                if instruct:
                    instruct.refresh_variable(self.variable_map)
                if isinstance(instruct,ReturnInstruction):
                    print(instruct)
            self.variable_map.clear()

    @staticmethod
    def load_data(path):
        with open(path) as f:
            data = f.read()
            gen_log.info("log file " + path + " successfully")

        return data

    @staticmethod
    def get_methods(source):
        method_pattern = re.compile("(; Function Attrs:.*?)}", re.S)

        methods = re.findall(method_pattern, source)
        return methods

    @staticmethod
    def get_method_name(method):
        name_pattern = re.compile("@.*?\(")
        result = re.search(name_pattern, method)
        if not result:
            gen_log.error("cannot find method name in method: " + method)
        else:
            name = result.group()[1:-1]
            return name

    @staticmethod
    def get_commands(method):
        body_pattern = re.compile("{\n.*", re.S)
        result = re.search(body_pattern, method)
        commands_list = []
        if not result:
            gen_log.error("cannot find commands in method: " + method)
        else:
            commands = result.group()[2:]
            commands_list = commands.split("\n")
            # Skip blank line
            commands_list = [line for line in commands_list if line]
        return commands_list
