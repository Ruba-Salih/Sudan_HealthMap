from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer
from disease.models import Disease
from hospital.models import Hospital
from hospital.hospital_tok import HospitalToken, HospitalTokenAuthentication


@login_required
def manage_case(request):

    try:
        hospital = Hospital.objects.get(email=request.user.email)
    except Hospital.DoesNotExist:
        return render(request, 'error.html', {'message': 'No hospital found for the logged-in user.'})

    token, _ = HospitalToken.objects.get_or_create(hospital=request.user)

    diseases = Disease.objects.all()

    context = {
        'diseases': diseases,
        'token': token.key,
        'hospital': hospital,
    }


    if request.method == 'POST':
        data = request.POST.copy()
        data['hospital'] = hospital.id
        serializer = CaseSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New case added successfully!")
            return redirect('hospital:hospital_dashboard')
        else:
            context['errors'] = serializer.errors
            return render(request, 'case/manage_case.html', context)
    else:
        return render(request, 'case/manage_case.html', context)


class CaseAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [HospitalTokenAuthentication]

    def get(self, request, pk=None):
        """
        Retrieve all cases for the authenticated hospital or a specific case if `pk` is provided.
        """
        hospital = self.get_hospital(request.user)
        if not hospital:
            return Response({"error": "No hospital found for the logged-in user."}, status=403)

        if pk:
            case = Case.objects.filter(pk=pk, hospital=hospital).first()
            if not case:
                return Response({"error": "Case not found."}, status=404)
            serializer = CaseSerializer(case)
            return Response(serializer.data, status=200)

        cases = Case.objects.filter(hospital=hospital)
        serializer = CaseSerializer(cases, many=True)

        return Response(serializer.data, status=200)

    def get_hospital(self, user):
        """
        Helper method to retrieve the associated hospital for the logged-in user.
        """
        try:
            return Hospital.objects.get(email=user.email)
        except Hospital.DoesNotExist:
            return None


    def post(self, request):
        """
        Create a new case for the authenticated hospital.
        """
        hospital = self.get_hospital(request.user)
        if not hospital:
            return Response({"error": "You are not associated with a hospital."}, status=403)

        data = request.data.copy()
        
        if not data.get('disease'):
            return Response({"error": "The disease field is required."}, status=400)

        data['hospital'] = hospital.id
        serializer = CaseSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        """
        Update a specific case for the authenticated hospital.
        """
        hospital = self.get_hospital(request.user)
        if not hospital:
            return Response({"error": "No associated hospital found."}, status=403)
    
        try:
            case = Case.objects.get(pk=pk, hospital=hospital)
        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=404)

        serializer = CaseSerializer(case, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """
        Delete a specific case for the authenticated hospital.
        """
        hospital = self.get_hospital(request.user)
        if not hospital:
            return Response({"error": "No associated hospital found."}, status=403)

        try:
            case = Case.objects.get(pk=pk, hospital=hospital)
            case.delete()
            return Response({"message": "Case deleted successfully."}, status=204)
        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=404)
