from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Case
from .serializers import CaseSerializer
from .models import Case
from .serializers import CaseSerializer
from disease.models import Disease
from hospital.models import Hospital


@login_required
def manage_case(request):
    if request.user.role != 'hospital':
        return render(request, 'error.html', {'message': 'Access denied.'})

    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return render(request, 'error.html', {'message': 'No associated hospital found.'})

    # Generate or retrieve the token for the authenticated user
    token, _ = Token.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        data = request.POST.copy()
        data['hospital'] = hospital.id
        serializer = CaseSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New case added successfully!")
            return redirect('hospital:hospital_dashboard')
        else:
            diseases = Disease.objects.all()
            return render(request, 'case/manage_case.html', {
                'diseases': diseases,
                'errors': serializer.errors,
                'token': token.key,  # Pass token to template
            })
    else:
        diseases = Disease.objects.all()
        return render(request, 'case/manage_case.html', {
            'diseases': diseases,
            'token': token.key,  # Pass token to template
        })
    

class CaseAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request, pk=None):
        """
        Retrieve all cases for the authenticated hospital or a specific case if `pk` is provided.
        """

        hospital = request.user.hospitals.first()
        if not hospital:
            return Response({"error": "You are not associated with a hospital."}, status=status.HTTP_403_FORBIDDEN)

        if pk:
            try:
                case = Case.objects.get(pk=pk, hospital=hospital)
                serializer = CaseSerializer(case)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Case.DoesNotExist:
                return Response({"error": "Case not found."}, status=status.HTTP_404_NOT_FOUND)

        cases = Case.objects.filter(hospital=hospital)
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def post(self, request):
        user = request.user
        print(f"Logged-in User post: {user} ({user.role})")
        try:
            hospital = user.hospitals.first()
            print(f"Associated Hospital in POST: {hospital}")
            if not hospital:
                return Response({"error": "You are not associated with a hospital."}, status=403)
        except Exception as e:
            print(f"Error fetching hospital: {e}")
            return Response({"error": "Error fetching hospital association."}, status=500)

        data = request.data.copy()
        data['hospital'] = hospital.id
        print(f"POST Data with Hospital: {data}")

        serializer = CaseSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(f"Serializer Errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        """
        Updte a specific case for the authenticated hospital.
        """
        try:
            if request.user.role != 'hospital':
                return Response({"error": "You are not authorized to update this case."}, status=403)

            hospital = request.user.hospitals.first()
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

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def delete(self, request, pk):
        """
        Delete a specific case for the authenticated hospital.
        """
        try:
            if request.user.role != 'hospital':
                return Response({"error": "You are not authorized to delete this case."}, status=403)

            hospital = request.user.hospitals.first()
            if not hospital:
                return Response({"error": "No associated hospital found."}, status=403)

            case = Case.objects.get(pk=pk, hospital=hospital)
            case.delete()
            return Response({"message": "Case deleted successfully."}, status=204)

        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        