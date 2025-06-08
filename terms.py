from enum import Enum

class PhotographicStyle(str, Enum):
    Arquitectonico = "Arquitectónico"
    Astrofotografia = "Astrofotografía"
    Artistico = "Artístico"
    Callejero = "Callejero"
    Documental = "Documental"
    Directa = "Directa"
    Desnudos = "Desnudos"
    Fotoperiodismo = "Fotoperiodismo"
    Macrofotografia = "Macrofotografía"
    Moda = "Moda"
    Publicitaria = "Publicitaria"
    Paisaje = "Paisaje"
    Retrato = "Retrato"


class Genre(Enum):
    Femenino = "Femenino"
    Masculino = "Masculino"


class Nationality(Enum):
    Argentina = "Argentina"
    Australia = "Australia"
    Alemania = "Alemania"
    Brasil = "Brasil"
    Colombia = "Colombia"
    Canada = "Canadá"
    Chile = "Chile"
    China = "China"
    Cuba = "Cuba"
    Espania = "España"
    Estados_unidos ="Estados Unidos"
    Francia = "Francia"
    Hungria = "Hungría"
    Italia = "Italia"
    Japon = "Japón"
    Mexico = "México"
    Reino_unido = "Reino Unido"