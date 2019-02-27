class TodoListAddAction:
    def __init__(self, desc, priority=None, project=None):
        self.desc = desc
        self.priority = priority
        self.project = project

    def make_todo_item(self):
        # A newly created action is not completed for obvious reasons
        item = {"desc": self.desc, "completed": False}

        # Optional parameters
        if self.priority is not None:
            item["priority"] = self.priority

        if self.project is not None:
            item["project"] = self.project

        return item


class TodoListUpdateAction:
    def __init__(self, id, desc=None, priority=None, project=None, completed=None):
        self.id = id
        self.desc = desc
        self.priority = priority
        self.project = project
        self.completed = completed

    def get_update(self):
        item = {}
        if self.desc is not None:
            item["desc"] = self.desc
        if self.priority is not None:
            item["priority"] = self.priority
        if self.project is not None:
            item["project"] = self.project
        if self.completed is not None:
            item["completed"] = self.completed

        return item

    def apply_changes(self, item):
        return {**item, **self.get_update()}


class TodoListRemoveAction:
    def __init__(self, attr, value):
        self.attr = attr
        self.value = value


class TodoListManager:
    def __init__(self, filename):
        self.data = {}
        self.filename = filename

    def load(self):
        """
        Loads list of tasks from file
        """
        pass

    def save(self):
        """
        Saves list of tasks to file
        """
        pass

    def add_item(self, new_item):
        """
        Adds item to list of tasks
        Returns ID of added item
        """
        try:
            id = max(self.data.keys()) + 1
        except ValueError:
            id = 1

        self.data[id] = new_item
        return id

    def update_item(self, id, update_item):
        """
        Updates an item by its id using a update of an item
        """
        try:
            self.data[id] = {**self.data[id], **update_item}
            return True
        except KeyError:
            return False
        

    def remove_items(self, attr, value):
        """
        Removes items by attribute/value combination
        """
        ids_to_remove = self.get_items(attr, value).keys()
        for id in ids_to_remove:
            del self.data[id]

        return len(ids_to_remove)

    def get_items(self, attr=None, value=None):
        """
        Retrieves items by attribute/value combination
        """
        return {k: v for k, v in self.data.items() if (attr=="id" and k==value) or (attr!="id" and (attr is None or v[attr] == value))}

    def apply_action(self, action):
        """Applies an action to the list of tasks"""
        if type(action) is TodoListAddAction:
            return self.add_item(action.make_todo_item())

        if type(action) is TodoListUpdateAction:
            return self.update_item(action.id, action.get_update())

        if type(action) is TodoListRemoveAction:
            return self.remove_items(action.attr, action.value)


tlm = TodoListManager("test.txt")

def add_item(command):
    description = ""
    priority = None
    project = None

    last_word = -1

    try:
        for i, token in enumerate(command):
            if token.startswith("!"):
                if priority is not None:
                    raise ValueError("Too many priorities")

                priority = int(token[1:])

                if priority > 4 or priority < 0:
                    raise ValueError("Invalid priority value")

            elif token.startswith("#"):
                if project is not None:
                    raise ValueError("Too many projects")

                project = token[1:]
            else:
                if last_word + 1 < i and description != "":
                    raise ValueError("Literally unparsable")

                description += token + " "
                last_word = i

        if description == "":
            raise ValueError("Missing description")

    except ValueError:
        # No text for task was entered
        description_input = input("Description: ")
        description = description_input.strip()

        # Loop until priority either has a valid value, or will be left as None if nothing is entered and the loop is broken
        while priority == None:
            try:
                priority_input = input(f'Priority: ({str(priority)}) ')
                if priority_input == "":
                    break
                if int(priority_input) > 4 or int(priority_input) < 0:
                    raise ValueError("Invalid priority value")
                if priority_input != "":
                    priority = int(priority_input)
            except ValueError:
                print("Enter a priority between 1 and 4")

        
        while project == None:
            try:
                project_input = input(f'Project: ({str(project)}) ')
                if " " in project_input:
                    raise ValueError("Project cannot contain spaces")

                if project_input != "":
                    project = project_input
                else:
                    break
            except ValueError:
                print("Project name must be a single word to which the task belongs")

    return TodoListAddAction(description, priority, project)


def update_item(command):
    id = None
    description = None
    priority = None
    project = None

    last_word = -1

    try:
        try:
            id = int(command[0])
        except IndexError:
            raise ValueError("Missing ID")
        
        if len(command) < 2:
            raise ValueError("Nothing to do. Fail to prompt.")

        for i, token in enumerate(command[1:]):
            if token.startswith("!"):
                if priority is not None:
                    raise ValueError("Too many priorities")

                priority = int(token[1:])

                if priority > 4 or priority < 0:
                    raise ValueError("Invalid priority value")

            elif token.startswith("#"):
                if project is not None:
                    raise ValueError("Too many projects")

                project = token[1:]
            else:
                if last_word + 1 < i and description != "":
                    raise ValueError("Literally unparsable")

                description += token + " "
                last_word = i

    except ValueError:

        while id is None:
            try:
                id_input = int(input(f'ID: '))
                if id_input < 0:
                    raise ValueError("Need positive ID")
                id = id_input

            except ValueError:
                print("Enter a positive number for the id to update")

        description_input = input(f'Description: ({str(description)}) ')
        if description_input != "":
            description = description_input.strip()

        # Loop until priority either has a valid value, or will be left as None if nothing is entered and the loop is broken
        while priority == None:
            try:
                priority_input = input(f'Priority: ({str(priority)}) ')
                if priority_input == "":
                    break
                if int(priority_input) > 4 or int(priority_input) < 0:
                    raise ValueError("Invalid priority value")
                if priority_input != "":
                    priority = int(priority_input)
            except ValueError:
                print("Enter a priority between 1 and 4")

        
        while project == None:
            try:
                project_input = input(f'Project: ({str(project)}) ')
                if " " in project_input:
                    raise ValueError("Project cannot contain spaces")

                if project_input != "":
                    project = project_input
                else:
                    break
            except ValueError:
                print("Project name must be a single word to which the task belongs")

    return TodoListUpdateAction(id, description, priority, project)

def remove_item(command):
    id = None
    try:
        try:
            id = int(command[0])
        except IndexError:
            raise ValueError("Missing index")
    except ValueError:
        while id is None:
            try:    
                id = int(input("Enter ID to Remove: "))
            except ValueError:
                print("Enter an ID to remove")

    return TodoListRemoveAction("id", id)

def purge_items():
    return TodoListRemoveAction("completed", True)

def done_item(command):
    id = None
    try:
        try:
            id = int(command[0])
        except IndexError:
            raise ValueError("Missing index")
    except ValueError:
        while id is None:
            try:    
                id = int(input("Enter ID to mark as completed: "))
            except ValueError:
                print("Enter an ID to mark as completed")

    return TodoListUpdateAction(id, completed=True)

def print_all_tasks():
    for k, v in tlm.get_items().items():
        print(f'#{k}: {v.description} {v.priority} {v.project}')

def print_remaining_tasks():
    for k, v in tlm.get_items("competed", False).items():
        print(f'#{k}: {v.description} {v.priority} {v.project}')

while True:
    try:
        cmd = input("=> ")
    except KeyboardInterrupt:
        print("Goodbye")
        exit(0)

    try:
        # Parse command
        tokens = cmd.split(' ')
        # The command is the first word, simple to extract
        command = tokens[0].lower()
        if command == "add":
            action = add_item(tokens[1:])
            print("Added new task with ID " + str(tlm.apply_action(action)))

        if command == "upd":
            updated = tlm.apply_action(update_item(tokens[1:]))
            if not updated:
                print("No such ID, nothing to do")
            else:
                print("Task updated")

        if command == "rem":
            updated = tlm.apply_action(remove_item(tokens[1:])) > 0
            if not updated:
                print("No such ID, nothing to do")
            else:
                print("Task removed")

        if command == "done":
            updated = tlm.apply_action(done_item(tokens[1:]))
            if not updated:
                print("No such ID, nothing to do")
            else:
                print("Task updated")

        if command == "purge":
            updated = tlm.apply_action(purge_items())
            print(str(updated) + " completed tasks removed")
        
    except KeyboardInterrupt:
        print("Operation cancelled")
    
