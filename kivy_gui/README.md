# kivy-gui

**kivy-gui** is a modular environment designed to help developers create Kivy apps quickly and efficiently. It simplifies the process of building apps by providing a base framework with pre-configured components, such as screens, widgets, layouts, logging, and theming.

## Features

- **Modular Design**: Break down your Kivy app into reusable components.
- **Base Classes**: Ready-to-use base classes for `App`, `Screen`, `Widget`, and `Layout`.
- **Logging**: Robust logging system for file and console outputs.
- **Theming**: Easy-to-apply theming for consistent styling across your app.
- **Quick Start**: Get up and running fast with minimal boilerplate code.

## Installation

Install `kivy-gui` using pip:

```bash
pip install kivy-gui


kivy_gui/
    ├── __init__.py          # Exposes core components like BaseApp, Logger, and Theme
    ├── baseapp.py           # BaseApp class for initializing Kivy apps
    ├── widgets/             # Custom reusable widgets
    │   ├── __init__.py
    │   └── basewidget.py    # BaseWidget class for widgets
    ├── utils/               # Utilities such as logging and theming
    │   ├── __init__.py
    │   ├── logger.py        # Robust logging utility
    │   └── theming.py       # Theming utility for consistent styling
    ├── screens/             # Reusable screen components
    │   ├── __init__.py
    │   └── basescreen.py    # BaseScreen class for Kivy screens
    ├── layouts/             # Reusable layouts for organizing UI elements
    │   ├── __init__.py
    │   └── baselayout.py    # BaseLayout class for layouts
    └── examples/            # Example applications to demonstrate usage
        └── example_app.py   # Example app showcasing the package
