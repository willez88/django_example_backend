from django.contrib import admin

from .models import (
    City,
    Country,
    Image,
    Municipality,
    Parish,
    Person,
    State,
)


class CountryAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Country al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name',
    )

    # Buscar por campos
    search_fields = ('name',)


class StateAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo State al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name', 'country',
    )

    # Buscar por campos
    search_fields = ('name',)

    # Aplica select2 en campos desplegables
    autocomplete_fields = ('country',)


class MunicipalityAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Municipality al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name', 'state',
    )

    # Buscar por campos
    search_fields = ('name', 'state__name',)

    # Aplica select2 en campos desplegables
    autocomplete_fields = ('state',)


class CityAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo City al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name', 'state',
    )

    # Buscar por campos
    search_fields = ('name',)

    # Aplica select2 en campos desplegables
    autocomplete_fields = ('state',)


class ParishAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Parish al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name', 'municipality',
    )

    # Buscar por campos
    search_fields = ('name', 'municipality__name')

    # Aplica select2 en campos desplegables
    autocomplete_fields = ('municipality',)


class ImageAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Image al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'name', 'file',
    )

    # Buscar por campos
    search_fields = ('name',)


class PersonAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Person al panel administrativo

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos de la clase
    list_display = (
        'user', 'first_name', 'last_name', 'id_number', 'phone',
    )

    # Seleccionar campo para filtrar
    list_filter = ('user',)

    # Aplica select2 en campos desplegables
    autocomplete_fields = ('user', 'images')


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Parish, ParishAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Person, PersonAdmin)
