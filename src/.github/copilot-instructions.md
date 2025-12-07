# AI Coding Agent Instructions for This Codebase

## Project Overview

**Willow** - A resizable multi-threaded tkinter application with 7 widgets controlled by 10 background threads communicating via Python queues.

- **`willow.py`** - Main application entry point (WillowApplication class)
- **`requirements.txt`** - Dependencies (Pillow for image handling)
- **`workspace.code-workspace`** - VS Code workspace configuration

## Architecture & Components

### Widget Layout (Resizable Grid)
The application uses tkinter grid geometry manager with responsive weights for window resizing.

- **Widget 1** (Row 0, Col 0): GIF display with frame animation (25% width × 25% height)
- **Widget 2** (Row 1, Col 0): PNG image display (25% width × 25% height)
- **Widget 3** (Row 2, Col 0): PNG image display (25% width × 25% height)
- **Widget 4** (Row 3, Col 0): PNG image display (25% width × 25% height)
- **Widget 5** (Row 0-3, Col 1): PNG image display (50% width × 100% height)
- **Widget 6** (Row 0-2, Col 2): Read-only scrollable text box (display output)
- **Widget 7** (Row 3, Col 2): User input text box (accepts ENTER-terminated commands)

### Thread Architecture
10 background threads communicate exclusively via Python queues (`queue.Queue()`):

| Thread | Purpose | Input Queue | Outputs |
|--------|---------|------------|---------|
| 1 | Widget 1 Controller | `queues[1]` | Receives `{type: "display_gif", filepath}` |
| 2-5 | Widget 2-5 Controllers | `queues[2-5]` | Receive `{type: "display_image", filepath}` |
| 6 | Widget 6 Controller | `queues[6]` | Receives `{type: "append_text", text}` |
| 7 | Widget 7 Controller | `queues[7]` | Passive monitoring (UI events handled by bindings) |
| 8 | **Orchestrator** | `queues[8]` | Routes user input → Widget 6 (Thread 6) + Archive (Thread 10) |
| 9 | **Housekeeper** | (N/A) | Runs maintenance every 60 seconds |
| 10 | **Archivist** | `queues[10]` | Stores messages as JSON in `self.archive` list |

### Message Flow (User Input Example)
1. User types in Widget 7 and presses ENTER
2. `on_widget7_input()` → sends to `queues[8]` (Orchestrator)
3. Thread 8 receives message, sends to `queues[6]` (Widget 6) and `queues[10]` (Archive)
4. Thread 6 appends timestamped text to Widget 6
5. Thread 10 stores JSON archive entry with timestamp

## Development Workflow

### Setup
```pwsh
# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```pwsh
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run via main entry point (recommended)
python main.py

# Or use backward-compatible wrapper
python willow.py
```

### GIF Animation Implementation (Widget 1)
- Uses `PIL.Image` to load all frames from GIF file
- Stores frames as `ImageTk.PhotoImage` objects in `self.gif_frames`
- `animate_gif()` method cycles frames every 100ms via `root.after()`
- Called by Thread 1 when receiving `display_gif` message

### Image Display (Widgets 2-5)
- Uses `PIL.Image.thumbnail()` to resize images to widget bounds
- Displays in `tk.Label` with `PhotoImage` reference kept to prevent garbage collection
- Automatically scales with window resize due to grid weight configuration

### Thread-Safe Queue Communication
- Each thread monitors `self.queues[thread_number]` with `queue.get(timeout=1)`
- Non-blocking with 1-second timeout to allow clean shutdown
- All inter-thread communication via queue messages (no shared mutable state)

## Key Files & Conventions

### Project Structure
```
willow/                          # Main package
├── __init__.py                  # Package exports
├── application.py               # WillowApplication class (orchestrates threads & UI)
├── image_utils.py               # GifAnimator, ImageDisplayer utilities
├── ui/
│   ├── __init__.py
│   ├── widgets.py               # WidgetFactory (widget creation & layout)
│   └── event_handlers.py        # WidgetEventHandlers (input event handling)
└── threads/
    ├── __init__.py
    ├── widget_controllers.py    # Threads 1-7 (GifDisplayController, PngDisplayController, etc.)
    ├── orchestrator.py          # Thread 8 (Orchestrator class)
    ├── housekeeper.py           # Thread 9 (Housekeeper class)
    └── archivist.py             # Thread 10 (Archivist class)

main.py                          # Entry point: python main.py
willow.py                        # Backward-compatible wrapper (imports from willow package)
requirements.txt                 # Pillow dependency
```

### Key Modules
- **`willow/application.py`** - Main `WillowApplication` class that coordinates all UI and threads
- **`willow/ui/widgets.py`** - `WidgetFactory` creates and lays out all 7 widgets
- **`willow/ui/event_handlers.py`** - `WidgetEventHandlers` manages user input from Widget 7
- **`willow/image_utils.py`** - `GifAnimator` (GIF loading/animation) and `ImageDisplayer` (PNG display)
- **`willow/threads/`** - Individual thread implementations for separation of concerns
- **`requirements.txt`** - Pillow dependency for image manipulation
- **`.github/`** - Directory for GitHub-specific files

## Patterns & Conventions

### Queue Message Format
All queue messages follow this convention:
```python
{
    "type": "operation_name",
    "key1": value1,
    "key2": value2
}
```

Examples:
- `{"type": "display_gif", "filepath": "/path/to/image.gif"}` (Thread 1)
- `{"type": "display_image", "filepath": "/path/to/image.png"}` (Threads 2-5)
- `{"type": "append_text", "text": "message to display"}` (Thread 6)
- `{"type": "user_input", "text": "user command"}` (Thread 8)
- `{"type": "archive_message", "text": "msg", "timestamp": unix_timestamp}` (Thread 10)

### Tkinter Grid Layout
- Grid weights configured on initialization for responsive resizing
- Widgets use `sticky="nsew"` to fill allocated grid cells
- Column weights: [1, 2, 1] → enforces 25%-50%-25% distribution
- Row weights: all equal → enforces 25% height distribution

### Thread-Safe Operations
- UI updates from background threads go through queues
- Main thread monitors queues via `monitor_queues()` with 100ms polling
- PhotoImage references stored in instance variables to prevent garbage collection
- Each thread uses `queue.get(timeout=1)` for non-blocking queue checks with clean shutdown support

### Module Organization
- **`application.py`**: Initializes all components and starts threads
- **`threads/`**: Each thread has its own module with a `.run()` method
- **`ui/`**: Separate concerns for widget creation and event handling
- **`image_utils.py`**: Reusable image manipulation classes
- Thread controllers are instantiated as objects and their `.run()` method is passed to threading.Thread

## Next Steps for AI Agents

When extending this application:
1. **Add new widgets**: Create controller in `threads/widget_controllers.py` following `PngDisplayController` pattern
2. **Add commands**: Send messages to Thread 8 (orchestrator) via `queues[8]` for routing
3. **Add persistence**: Extend `Archivist` class to write archive to JSON file
4. **Enhance housekeeper**: Add custom maintenance tasks in `Housekeeper.perform_maintenance()`
5. **Testing**: Add unit tests for thread communication patterns in `tests/` directory
6. **Maintenance**: Thread controller classes can be tested independently by mocking queues
