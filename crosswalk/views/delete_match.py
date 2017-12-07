from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from crosswalk.authentication import AuthenticatedView
from crosswalk.models import Domain, Entity


class DeleteMatch(AuthenticatedView):

    def post(self, request, domain):
        """
        POST searches for an entity based on criteria. If only one entity is
        returned from query, it is deleted. If more than one, return 403.
        """
        match_attrs = request.data.copy()

        try:
            domain = Domain.objects.get(slug=domain)
        except ObjectDoesNotExist:
            return Response({
                "message": "Domain not found."
            }, status=status.HTTP_404_NOT_FOUND)

        entities = Entity.objects.filter(domain=domain)
        entities = entities.filter(attributes__contains=match_attrs)

        if entities.count() == 0:
            return Response({
                "message": "Entity not found."
            }, status=status.HTTP_404_NOT_FOUND)

        elif entities.count() > 1:
            return Response({
                "message": "Found more than one entity. Be more specific?"
            }, status=status.HTTP_403_FORBIDDEN)

        entities.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
