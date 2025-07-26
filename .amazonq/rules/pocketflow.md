# PocketFlow Library Reference

PocketFlow is a lightweight workflow orchestration library with sync/async support, retry mechanisms, and flexible node chaining.

## Core Classes

### BaseNode
Base class for all nodes with parameter management and successor chaining.
- `set_params(params)` - Set node parameters
- `next(node, action="default")` - Chain to next node
- `prep(shared)` - Preparation phase
- `exec(prep_res)` - Execution phase  
- `post(shared, prep_res, exec_res)` - Post-processing phase
- `run(shared)` - Execute single node
- `>>` operator - Chain nodes (e.g., `node1 >> node2`)
- `-` operator - Conditional transitions (e.g., `node - "success" >> next_node`)

### Node
Synchronous node with retry and wait capabilities.
- `max_retries=1` - Number of retry attempts
- `wait=0` - Wait time between retries
- `exec_fallback(prep_res, exc)` - Fallback on final failure

### BatchNode
Processes lists of items, executing for each item.

### Flow
Orchestrates node sequences with conditional branching.
- `start(node)` - Set starting node
- `get_next_node(curr, action)` - Determine next node based on action
- Executes nodes until no successor found

### BatchFlow
Executes flow for multiple parameter sets.

## Async Classes

### AsyncNode
Asynchronous version of Node.
- `prep_async(shared)` - Async preparation
- `exec_async(prep_res)` - Async execution
- `exec_fallback_async(prep_res, exc)` - Async fallback
- `post_async(shared, prep_res, exec_res)` - Async post-processing
- `run_async(shared)` - Execute async node

### AsyncBatchNode
Sequential async batch processing.

### AsyncParallelBatchNode  
Parallel async batch processing using `asyncio.gather`.

### AsyncFlow
Async flow orchestration supporting mixed sync/async nodes.

### AsyncBatchFlow
Async batch flow with sequential execution.

### AsyncParallelBatchFlow
Async batch flow with parallel execution.

## Usage Patterns

```python
# Basic chaining
node1 >> node2 >> node3

# Conditional branching
node1 - "success" >> success_node
node1 - "error" >> error_node

# Flow creation
flow = Flow().start(node1)

# Batch processing
batch_node = BatchNode()
batch_flow = BatchFlow()

# Async execution
async_node = AsyncNode()
result = await async_node.run_async(shared_data)
```

## Key Features
- Retry mechanisms with configurable wait times
- Conditional node transitions
- Batch processing (sequential/parallel)
- Mixed sync/async support
- Shared state management
- Flexible error handling