# Task

## Overview

*Task* is a task planning tool for the command line.

## Installation

```bash
python -m pip install task-planner
```

## Command reference

```
usage: python -m task [] [order] [add] [priority] [do] [done]

View all tasks:
python -m task
python -m task order <task|priority|status>

Add a task:
python -m task add "<name>"
python -m task add "<name>" priority <priority>

Set the priority of an existing task:
python -m task priority <priority> for <task id>

Set a task to doing:
python -m task do <task id>

Delete a task:
python -m task done <task id>
```

## License

Copyright (c) 2019, Yannick Kirschen, All rights reserved.
Licensed under the [MIT License](https://github.com/yannickkirschen/task/blob/master/LICENSE).
Happy forking :fork_and_knife:
