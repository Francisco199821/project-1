from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label

class ScrollableGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ScrollableGridLayout, self).__init__(**kwargs)
        self.cols = 10
        self.spacing = [5, 5]
        self.size_hint_x = None
        self.bind(minimum_width=self.setter('width'))
        self.button_counters = {}  # Diccionario para mantener el registro de las pulsaciones
        for i in range(1, 91):
            button = Button(text=str(i), size_hint=(None, None), size=(100, 100))
            button.bind(on_release=self.button_pressed)
            self.add_widget(button)
            self.button_counters[i] = 0

    def button_pressed(self, instance):
        # Incrementar el contador de la pulsación del botón
        button_number = int(instance.text)
        self.button_counters[button_number] += 1

class MyApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height - 200))
        layout = ScrollableGridLayout(cols=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        scroll_view.add_widget(layout)
        
        start_button = Button(text="Iniciar")
        start_button.bind(on_release=self.reset_counters)  # Enlace del botón "Iniciar" a la función de reinicio
        
        get_numbers_button = Button(text="Obtener números")
        get_numbers_button.bind(on_release=self.get_most_pressed_numbers)  # Enlace del botón "Obtener números" a la función de obtención

        self.label = Label(text="", size_hint=(1, None), height=50)
        
        root.add_widget(scroll_view)
        root.add_widget(start_button)
        root.add_widget(get_numbers_button)
        root.add_widget(self.label)
        
        self.button_counters = layout.button_counters  # Referencia al diccionario de contadores de botones
        
        return root

    def reset_counters(self, instance):
        # Función para reiniciar los contadores de botones
        for button_number in self.button_counters:
            self.button_counters[button_number] = 0

    def get_most_pressed_numbers(self, instance):
        # Función para obtener los 24 números más pulsados y mostrarlos en el Label
        most_pressed_numbers = [number for number, count in self.button_counters.items() if count > 0]
        most_pressed_numbers.sort(key=lambda number: self.button_counters[number], reverse=True)
        most_pressed_numbers = most_pressed_numbers[:24]
        self.label.text = "Los 24 números más pulsados: " + ", ".join(map(str, most_pressed_numbers))

if __name__ == '__main__':
    MyApp().run()