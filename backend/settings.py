from MillenniumUtils import CheckBox, DefineSetting, DropDown, NumberTextInput, Settings, FloatSlider, StringTextInput, FloatTextInput, NumberSlider
from logger import logger
from settings_observer import SettingsObservable, PluginSettingsObserver, CallbackSettingsObserver


class ObservableSettings(Settings):
    """Custom metaclass that adds observer functionality to Settings."""
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Add observer functionality
        cls._observable = SettingsObservable()
        cls._default_observer = PluginSettingsObserver()
        cls._callback_observer = CallbackSettingsObserver()
        
        # Add observers
        cls._observable.add_observer(cls._default_observer)
        cls._observable.add_observer(cls._callback_observer)
        
        # Store original __setattr__ method
        original_setattr = cls.__setattr__
        
        def observable_setattr(self, name, value):
            # Get old value if it exists
            old_value = getattr(self, name, None) if hasattr(self, name) else None
            
            # Set the new value
            original_setattr(self, name, value)
            
            # Notify observers if this is a setting property
            if hasattr(self.__class__, name) and not name.startswith('_'):
                cls._observable.notify_observers(name, value, old_value)
        
        # Replace __setattr__ with our observable version
        cls.__setattr__ = observable_setattr
        
        return cls


class PluginSettings(metaclass=ObservableSettings):

    @DefineSetting(
        name='CheckBox Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=CheckBox(),
        default=True
    )
    def checkboxInput(self): pass

    @DefineSetting(
        name='Dropdown Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=DropDown(items=["String Value", False, 69]),
        default="String Value"
    )
    def dropDownInput(self): pass

    @DefineSetting(
        name='Float Slider Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=FloatSlider(range=(0.0, 10.0), step=0.5),
        default=0.5
    )
    def floatSliderInput(self): pass

    @DefineSetting(
        name='Number Slider Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=NumberSlider(range=(0, 10), step=1),
        default=5
    )
    def numberSliderInput(self): pass

    @DefineSetting(
        name='Number Text Input Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=NumberTextInput(range=(0, 10000)),
        default=1234
    )
    def numberTextInput(self): pass

    @DefineSetting(
        name='String Text Input Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=StringTextInput(),
        default='Hello World!'
    )
    def stringTextInput(self): pass

    @DefineSetting(
        name='Float Text Input Example', 
        description='lorem ipsum dolor sit amet, consectetur adipiscing elit',
        style=FloatTextInput(range=(0, 10000)),
        default=1234.0
    )
    def floatTextInput(self): pass

    @classmethod
    def register_callback(cls, setting_name: str, callback):
        """
        Register a custom callback for a specific setting.
        
        Args:
            setting_name: The name of the setting to monitor
            callback: Function to call when the setting changes
                     Signature: callback(setting_name, new_value, old_value)
        """
        cls._callback_observer.register_callback(setting_name, callback)
    
    @classmethod
    def unregister_callback(cls, setting_name: str):
        """Remove callback for a specific setting."""
        cls._callback_observer.unregister_callback(setting_name)
    
    @classmethod
    def add_observer(cls, observer):
        """Add a custom observer to monitor all setting changes."""
        cls._observable.add_observer(observer)
    
    @classmethod
    def remove_observer(cls, observer):
        """Remove a custom observer."""
        cls._observable.remove_observer(observer)


