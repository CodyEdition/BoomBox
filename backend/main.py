import Millennium, PluginUtils # type: ignore
from settings import PluginSettings
from settings_observer import SettingsObserver
from logger import logger
import time

class CustomSettingsObserver(SettingsObserver):
    """Custom observer that tracks specific setting patterns."""
    
    def __init__(self):
        self.change_count = 0
        self.last_changed_setting = None
    
    def update(self, setting_name: str, new_value, old_value=None):
        self.change_count += 1
        self.last_changed_setting = setting_name
        
        # Special handling for different setting types
        if setting_name == 'numberTextInput':
            if new_value > 1000:
                logger.log(f"High value detected in {setting_name}: {new_value}")
        elif setting_name == 'stringTextInput':
            if len(str(new_value)) > 10:
                logger.log(f"Long string detected in {setting_name}: '{new_value}'")
        
        logger.log(f"Custom observer: Total changes: {self.change_count}, Last changed: {setting_name}")


class Backend:
    @staticmethod 
    def receive_frontend_message(message: str, status: bool, count: int):
        logger.log(f"received: {[message, status, count]}")

        # accepted return types [str, int, bool]
        if count == 69:
            return True
        else:
            return False

def get_steam_path():
    logger.log("getting steam path")
    return Millennium.steam_path()

class Plugin:

    # if steam reloads, i.e. from a new theme being selected, or for other reasons, this is called. 
    # with the above said, that means this may be called more than once within your backends lifespan 
    def _front_end_loaded(self):
        # The front end has successfully mounted in the steam app. 
        # You can now use Millennium.call_frontend_method()
        logger.log("The front end has loaded!")

        start_time = time.time()
        value = Millennium.call_frontend_method("classname.method", params=[18, "USA", False])
        end_time = time.time()
        
        logger.log(f"classname.method says -> {value} [{round((end_time - start_time) * 1000, 3)}ms]")


    def _load(self):     
        
        # Register custom callbacks for specific settings
        def on_number_text_change(setting_name, new_value, old_value):
            logger.log(f"Custom callback: {setting_name} changed from {old_value} to {new_value}")
            if new_value == 69:
                logger.log("Special value detected! 69 is the magic number!")
        
        def on_string_text_change(setting_name, new_value, old_value):
            logger.log(f"String setting changed: '{old_value}' -> '{new_value}'")
        
        # Register callbacks
        PluginSettings.register_callback('numberTextInput', on_number_text_change)
        PluginSettings.register_callback('stringTextInput', on_string_text_change)
        
        # Add custom observer
        custom_observer = CustomSettingsObserver()
        PluginSettings.add_observer(custom_observer)

        # Test the observer pattern
        logger.log("=== Testing Observer Pattern ===")
        PluginSettings.numberTextInput += 1
        logger.log("PluginSettings.numberTextInput: " + str(PluginSettings.numberTextInput))

        PluginSettings.numberTextInput += 1
        logger.log("PluginSettings.numberTextInput: " + str(PluginSettings.numberTextInput))
        
        # Test string setting change
        PluginSettings.stringTextInput = "Hello from the observer pattern!"
        
        # Test high value detection
        PluginSettings.numberTextInput = 2000
        logger.log("=== Observer Pattern Test Complete ===")

        # This code is executed when your plugin loads. 
        # notes: thread safe, running for entire lifespan of millennium
        logger.log(f"bootstrapping example plugin, millennium {Millennium.version()}")

        try:
            # This will fail to call the frontend as it is not yet loaded. It is only safe to call the frontend after _front_end_loaded is called.
            value = Millennium.call_frontend_method("classname.method", params=[18, "USA", False])
            logger.log(f"ponged message -> {value}")

        # Frontend not yet loaded
        except ConnectionError as error:
            logger.error(f"Failed to ping frontend, {error}")
            
        Millennium.ready() # this is required to tell Millennium that the backend is ready.


    def _unload(self):
        logger.log("unloading")