from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Country(models.Model):
    """!
    Clase que contiene los paises

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre del pais
    name = models.CharField(
        'nombre', max_length=80, unique=True,
        db_comment='Nombre del país',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name
    
    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'País'
        verbose_name_plural = 'Países'


class State(models.Model):
    """!
    Clase que contiene los estados

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    name = models.CharField(
        'nombre', max_length=50, unique=True,
        db_comment='Nombre del estado',
    )

    # Relación con el modelo Country
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='país',
        db_comment='Relación con el modelo país',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name
    
    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Municipality(models.Model):
    """!
    Clase que contiene los municipios

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    name = models.CharField(
        'nombre', max_length=50, db_comment='Nombre del municipio',
    )

    # Relación con el modelo State
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, verbose_name='estado',
        db_comment='Relación con el modelo estado',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name
    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'


class City(models.Model):
    """!
    Clase que contiene las ciudades

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    name = models.CharField(
        'nombre', max_length=50, db_comment='Nombre de la ciudad',
    )

    # Relación con el modelo State
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, verbose_name='estado',
        db_comment='Relación con el modelo estado',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name
    
    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Parish(models.Model):
    """!
    Clase que contiene las parroquias

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    name = models.CharField(
        'nombre', max_length=50, db_comment='Nombre de la parroquia',
    )

    # Relación con el modelo Municipality
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, verbose_name='municipio',
        db_comment='Relación con el modelo municipio',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name
    
    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'


class Image(models.Model):
    """!
    Clase que registra las imagenes

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    name = models.CharField(
        'nombre', max_length=100, db_comment='Nombre de la imagen',
    )

    # Archivo
    file = models.ImageField(
        'archivo', upload_to='images/', db_comment='Archivo con la imagen',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    """!
    Función que permite eliminar la imagen del disco duro

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>
        GNU Public License versión 3 (GPLv3)</a>
    """

    instance.file.delete(False)


class Person(models.Model):
    """!
    Clase que contiene las personas

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre
    first_name = models.CharField(
        'nombres', max_length=100, db_comment='Nombres de la persona',
    )

    # Apellido
    last_name = models.CharField(
        'apellidos', max_length=100, db_comment='Apellidos de la persona',
    )

    # Cédula de identidad
    id_number = models.CharField(
        'cédula de identidad',
        max_length=9,
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                'Introduzca un número de cédula válido. Ej. V00000000 ó E00000000'
            ),
        ],
        unique=True,
        db_comment='Cédula de identidad de la persona',
    )

    # Número telefónico
    phone = models.CharField(
        'teléfono',
        max_length=15,
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                'Número telefónico inválido. Ej. +58-416-0000000.'
            ),
        ],
        db_comment='Número telefónico de la persona',
    )

    # Correo electrónico
    email = models.EmailField(
        'correo electrónico', max_length=100, help_text='correo@correo.com',
        db_comment='Correo electrónico de la persona',
    )

    # Dirección
    address = models.TextField(
        'dirección', db_comment='Dirección de la persona',
    )

    # Relación con el modelo Parish
    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, verbose_name='parroquia',
        db_comment='Relación con el modelo parroquia',
    )

    # Relación con el modelo User
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='usuario',
        db_comment='Relación con el modelo usuario',
    )

    # Relación con el modelo Image
    images = models.ManyToManyField(
        Image, verbose_name='imágenes',
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (paez.william8 at gmail.com)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return string <b>{object}</b> Objeto con el nombre, apellido y la
            cédula de identidad
        """

        return '%s %s, %s' % (
            self.first_name, self.last_name, self.id_number
        )

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
