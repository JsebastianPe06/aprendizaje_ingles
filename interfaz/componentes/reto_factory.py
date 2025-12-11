# Archivo: interfaz/componentes/reto_factory.py
"""
Fábrica para crear widgets de reto según el tipo.
"""

from interfaz.componentes import RETO_WIDGETS


class RetoWidgetFactory:
    """Fábrica para crear widgets de reto."""
    
    @staticmethod
    def crear_widget(reto_data, parent=None):
        """
        Crea un widget de reto basado en el tipo.
        
        :param reto_data: Datos del reto (debe incluir 'tipo_reto')
        :param parent: Widget padre
        :return: Instancia del widget de reto apropiado
        """
        tipo = reto_data.get('tipo_reto')
        
        if not tipo:
            raise ValueError("Los datos del reto deben incluir 'tipo_reto'")
        
        widget_class = RETO_WIDGETS.get(tipo)
        
        if not widget_class:
            raise ValueError(f"Tipo de reto no soportado: {tipo}")
        
        # Crear instancia del widget
        widget = widget_class(reto_data, parent)
        
        return widget
    
    @staticmethod
    def crear_widget_desde_reto(reto_obj, parent=None):
        """
        Crea un widget a partir de un objeto reto.
        
        :param reto_obj: Instancia de RetoBase (o subclase)
        :param parent: Widget padre
        :return: Widget de reto configurado
        """
        # Generar datos del reto
        reto_data = reto_obj.generar()
        
        # Agregar información adicional
        reto_data['palabra_objetivo'] = reto_obj.palabra_objetivo
        reto_data['nivel_dificultad'] = reto_obj.nivel_dificultad
        
        # Crear widget
        return RetoWidgetFactory.crear_widget(reto_data, parent)