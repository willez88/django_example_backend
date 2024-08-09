from rest_framework import serializers

from .models import (
    City,
    Country,
    Image,
    Parish,
    Person,
    State,
)
from users.serializers import UserSerializer


class CountrySerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo Country
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = Country
        fields = ('pk', 'name',)


class StateSerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo State
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = State
        fields = ('pk', 'name', 'country',)


class MunicipalitySerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo Municipality
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = Parish
        fields = ('pk', 'name', 'state',)


class CitySerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo City
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = City
        fields = ('pk', 'name', 'state',)


class ParishSerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo Parish
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = Parish
        fields = ('pk', 'name', 'municipality',)


class ImageSerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo Image
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = Image
        fields = ('pk', 'name', 'file',)


class PersonSerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del modelo Person
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Id del modelo Parish
    parish_id = serializers.IntegerField()

    # Relación con User
    user = UserSerializer(many=False, read_only=True)

    # Relación con el modelo Image
    # images = ImageSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'pk', 'first_name', 'last_name', 'id_number', 'phone', 'email', 'address',
            'parish', 'parish_id', 'user', 'images',
        )
        depth = 1
    
    def create(self, validated_data):
        """!
        Método para crear personas

        @author William Páez (paez.william8 at gmail.com)
        """

        user = self.context['user']
        parish = Parish.objects.get(id=validated_data['parish_id'])
        person = Person.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            id_number=validated_data['id_number'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            address=validated_data['address'],
            parish=parish,
            user=user,
        )
        return person

    def update(self, instance, validated_data):
        """!
        Método para actualizar personas

        @author William Páez (paez.william8 at gmail.com)
        """

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.parish_id = validated_data.get('parish_id', instance.parish)
        instance.save()
        return instance
