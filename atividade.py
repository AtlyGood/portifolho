from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
import random

class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.line_width = 2
        self.current_shape = 'line'  # Pode ser 'line', 'rectangle', 'ellipse'
        self.start_pos = None
        self.current_shape_obj = None
    
    def on_touch_down(self, touch):
        # Gerar cor aleatória para cada novo traço
        color = (random.random(), random.random(), random.random())
        
        with self.canvas:
            Color(*color)
            
            if self.current_shape == 'line':
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
            elif self.current_shape == 'rectangle':
                self.start_pos = (touch.x, touch.y)
                self.current_shape_obj = Rectangle(pos=self.start_pos, size=(1, 1))
            elif self.current_shape == 'ellipse':
                self.start_pos = (touch.x, touch.y)
                self.current_shape_obj = Ellipse(pos=self.start_pos, size=(1, 1))
    
    def on_touch_move(self, touch):
        if self.current_shape == 'line':
            # Verifica se a linha foi criada antes de tentar atualizar
            if 'line' in touch.ud:
                touch.ud['line'].points += [touch.x, touch.y]
        elif self.current_shape in ['rectangle', 'ellipse'] and self.start_pos:
            # Atualizar o retângulo ou elipse conforme o movimento
            start_x, start_y = self.start_pos
            current_x, current_y = touch.x, touch.y
            
            # Calcular posição e tamanho
            pos_x = min(start_x, current_x)
            pos_y = min(start_y, current_y)
            width = abs(current_x - start_x)
            height = abs(current_y - start_y)
            
            self.current_shape_obj.pos = (pos_x, pos_y)
            self.current_shape_obj.size = (width, height)
    
    def clear_canvas(self, instance):
        self.canvas.clear()
    
    def set_line_width(self, instance, value):
        self.line_width = value
    
    def set_shape(self, instance, text):
        self.current_shape = text.lower()

class MyPaintApp(App):
    def build(self):
        # Criar layout principal
        layout = FloatLayout()
        
        # Criar o widget de pintura
        paint_widget = MyPaintWidget()
        layout.add_widget(paint_widget)
        
        # Botão para limpar
        clear_btn = Button(
            text='Limpar',
            size_hint=(0.1, 0.05),
            pos_hint={'x': 0.9, 'top': 1}
        )
        clear_btn.bind(on_release=paint_widget.clear_canvas)
        layout.add_widget(clear_btn)
        
        # Slider para espessura da linha
        slider = Slider(
            min=1,
            max=20,
            value=2,
            size_hint=(0.2, 0.05),
            pos_hint={'x': 0.1, 'top': 1}
        )
        slider.bind(value=paint_widget.set_line_width)
        layout.add_widget(slider)
        
        # Label para o slider
        slider_label = Label(
            text='Espessura:',
            size_hint=(0.1, 0.05),
            pos_hint={'x': 0, 'top': 1}
        )
        layout.add_widget(slider_label)
        
        # Spinner para seleção de forma
        spinner = Spinner(
            text='Linha',
            values=('Linha', 'Retângulo', 'Elipse'),
            size_hint=(0.2, 0.05),
            pos_hint={'x': 0.4, 'top': 1}
        )
        spinner.bind(text=paint_widget.set_shape)
        layout.add_widget(spinner)
        
        return layout

if __name__ == '__main__':
    MyPaintApp().run()