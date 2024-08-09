import json

from rest_framework import (
    status,
    viewsets
)
from rest_framework.response import Response

from users.permissions import CustomObjectPermissions
from .models import (
    City,
    Country,
    Image,
    Municipality,
    Parish,
    Person,
    State,
)
from .serializers import (
    CitySerializer,
    CountrySerializer,
    ImageSerializer,
    MunicipalitySerializer,
    ParishSerializer,
    PersonSerializer,
    StateSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo Country

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name',)


class StateViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo State

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = State
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name', 'country__name',)


class MunicipalityViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo Municipality

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Municipality
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name', 'state__name',)


class CityViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo City

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name', 'state__name',)


class ParishViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo Parish

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Parish
    queryset = Parish.objects.all()
    serializer_class = ParishSerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name', 'municipality__name',)


class ImageViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo image

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Image
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('name',)


class PersonViewSet(viewsets.ModelViewSet):
    """!
    Clase que crea los endpoint para el modelo Person

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = Person
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('first_name', 'last_name', 'id_number',)

    def list(self, request):
        """!
        Clase que lista las personas por el usuario logueado

        @author William Páez (paez.william8 at gmail.com)
        """
        
        queryset = Person.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, format=None):
        """!
        Método para crear personas

        @author William Páez (paez.william8 at gmail.com)
        """

        serializer = self.get_serializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        person = serializer.save()
        for image in request.data.get('images'):
            person.images.add(image['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, format=None, pk=None):
        """!
        Método para actualizar personas

        @author William Páez (paez.william8 at gmail.com)
        """

        person = self.get_object()
        if person.user == request.user:
            serializer = self.get_serializer(person, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            images = request.data.get('images')
            if images is not None:
                person.images.clear()
                for image in images:
                    person.images.add(image['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'detail': 'Usted no tiene permiso para realizar esta acción.'},
            status=status.HTTP_403_FORBIDDEN
        )

    def retrieve(self, request, format=None, pk=None):
        """!
        Método para listar una persona

        @author William Páez (paez.william8 at gmail.com)
        """

        person = self.get_object()
        if person.user == request.user:
            serializer = self.get_serializer(person)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'detail': 'Usted no tiene permiso para realizar esta acción.'},
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, pk=None):
        """!
        Método para eliminar una persona

        @author William Páez (paez.william8 at gmail.com)
        """

        person = self.get_object()
        if person.user == request.user:
            person.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Usted no tiene permiso para realizar esta acción.'},
            status=status.HTTP_403_FORBIDDEN
        )
