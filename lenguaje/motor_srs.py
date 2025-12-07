"""
Docstring for lenguaje.motor_srs
"""

class MotorSRS:
    """
    Implementación básica del algoritmo SM-2 (Anki) adaptado.

    Cada palabra tiene un estado con campos:
    - easiness (ef, float)
    - interval (días)
    - repetitions (int)
    - last_practiced (timestamp)
    - next_review (timestamp o None)

    Métodos:
    - registrar_resultado(palabra, quality)  quality en 0..5
    - obtener_deberes(fecha_hoy) -> lista de palabras a repasar

    NOTA: Este motor no persiste a disco; se espera que la capa que usa
    MotorSRS guarde el estado en SQLite/JSON según necesite.
    """

    def __init__(self, state=None):
        # state: dict palabra -> estado
        self.state = state or {}

    def _init_estado(self, palabra):
        if palabra not in self.state:
            self.state[palabra] = {
                'easiness': 2.5,
                'interval': 0,
                'repetitions': 0,
                'last_practiced': None,
                'next_review': None
            }
        return self.state[palabra]

    def registrar_resultado(self, palabra, quality, hoy=None):
        """
        Registra el resultado del usuario para "palabra".
        quality: entero 0..5 (0 = total fail, 5 = perfect)
        """
        from datetime import datetime, timedelta
        if hoy is None:
            hoy = datetime.utcnow()
        st = self._init_estado(palabra)
        q = max(0, min(5, int(quality)))

        if q < 3:
            st['repetitions'] = 0
            st['interval'] = 1
            # no change easiness
        else:
            st['repetitions'] += 1
            if st['repetitions'] == 1:
                st['interval'] = 1
            elif st['repetitions'] == 2:
                st['interval'] = 6
            else:
                st['interval'] = int(round(st['interval'] * st['easiness']))
            # actualizar easiness
            st['easiness'] = max(1.3, st['easiness'] + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))

        st['last_practiced'] = hoy.isoformat()
        st['next_review'] = (hoy + timedelta(days=st['interval'])).isoformat()
        self.state[palabra] = st
        return st

    def obtener_deberes(self, fecha_hoy=None):
        """Devuelve lista de palabras con next_review <= fecha_hoy o sin next_review (nuevo)
        fecha_hoy puede ser datetime o None (se usa utcnow).
        """
        from datetime import datetime
        if fecha_hoy is None:
            fecha_hoy = datetime.utcnow()
        res = []
        for palabra, st in self.state.items():
            nr = st.get('next_review')
            if nr is None:
                res.append(palabra)
                continue
            try:
                import dateutil.parser as dp
                dt = dp.parse(nr)
            except Exception:
                # fallback: strings en isoformat comparables
                dt = None
            if dt is None:
                res.append(palabra)
            else:
                if dt <= fecha_hoy:
                    res.append(palabra)
        return res