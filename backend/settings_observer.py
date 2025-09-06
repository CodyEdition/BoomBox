from typing import Any, Callable, List
from logger import logger


class SettingsObserver:
    """Base observer class for monitoring setting changes."""
    
    def update(self, setting_name: str, new_value: Any, old_value: Any = None):
        """
        Called when a setting changes.
        
        Args:
            setting_name: The name of the setting that changed
            new_value: The new value of the setting
            old_value: The previous value of the setting (if available)
        """
        pass


class SettingsObservable:
    """Observable class that manages observers and notifies them of setting changes."""
    
    def __init__(self):
        self._observers: List[SettingsObserver] = []
    
    def add_observer(self, observer: SettingsObserver):
        """Add an observer to the list of observers."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.log(f"Added observer: {type(observer).__name__}")
    
    def remove_observer(self, observer: SettingsObserver):
        """Remove an observer from the list of observers."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.log(f"Removed observer: {type(observer).__name__}")
    
    def notify_observers(self, setting_name: str, new_value: Any, old_value: Any = None):
        """Notify all observers of a setting change."""
        logger.log(f"Notifying {len(self._observers)} observers of setting change: {setting_name} = {new_value}")
        for observer in self._observers:
            try:
                observer.update(setting_name, new_value, old_value)
            except Exception as e:
                logger.error(f"Error in observer {type(observer).__name__}: {e}")


class PluginSettingsObserver(SettingsObserver):
    """Default observer for plugin settings that logs all changes."""
    
    def update(self, setting_name: str, new_value: Any, old_value: Any = None):
        """Log setting changes with detailed information."""
        if old_value is not None:
            logger.log(f"Setting '{setting_name}' changed from {old_value} to {new_value}")
        else:
            logger.log(f"Setting '{setting_name}' changed to {new_value}")


class CallbackSettingsObserver(SettingsObserver):
    """Observer that allows custom callback functions for specific settings."""
    
    def __init__(self):
        self._callbacks: dict[str, Callable] = {}
    
    def register_callback(self, setting_name: str, callback: Callable[[str, Any, Any], None]):
        """
        Register a callback function for a specific setting.
        
        Args:
            setting_name: The name of the setting to monitor
            callback: Function to call when the setting changes
                     Signature: callback(setting_name, new_value, old_value)
        """
        self._callbacks[setting_name] = callback
        logger.log(f"Registered callback for setting: {setting_name}")
    
    def unregister_callback(self, setting_name: str):
        """Remove callback for a specific setting."""
        if setting_name in self._callbacks:
            del self._callbacks[setting_name]
            logger.log(f"Unregistered callback for setting: {setting_name}")
    
    def update(self, setting_name: str, new_value: Any, old_value: Any = None):
        """Call the registered callback if one exists for this setting."""
        if setting_name in self._callbacks:
            try:
                self._callbacks[setting_name](setting_name, new_value, old_value)
            except Exception as e:
                logger.error(f"Error in callback for setting '{setting_name}': {e}")
