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
    # Debugging: Log the logged-in user information
    print(f"Logged-in User: {request.user}, Role: {request.user.role}, Email: {request.user.email}")

    # Ensure the logged-in user is a hospital
    if request.user.role != 'hospital':
        return render(request, 'error.html', {'message': 'Access denied. Only hospitals can manage cases.'})

    # Fetch the hospital associated with the logged-in user by email
    try:
        hospital = Hospital.objects.get(email=request.user.email)
        print(f"Associated Hospital: {hospital.name}")
    except Hospital.DoesNotExist:
        return render(request, 'error.html', {'message': 'No hospital found for the logged-in user.'})

    # Generate or retrieve the token for the authenticated user
    token, _ = Token.objects.get_or_create(user=request.user)

    diseases = Disease.objects.all()

    context = {
        'diseases': diseases,
        'token': token.key,  # Pass token to the template
        'hospital': hospital,  # Add hospital object to context
    }


    if request.method == 'POST':
        # Prepare case data
        data = request.POST.copy()
        data['hospital'] = hospital.id  # Assign the hospital ID to the case
        serializer = CaseSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New case added successfully!")
            return redirect('hospital:hospital_dashboard')
        else:
            context['errors'] = serializer.errors  # Include errors in context
            return render(request, 'case/manage_case.html', context)
    else:
        return render(request, 'case/manage_case.html', context)


class CaseAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        """
        Retrieve all cases for the authenticated hospital or a specific case if `pk` is provided.
        """
        user = request.user
        if user.role != 'hospital':
            return Response({"error": "Access denied. Only hospitals can view cases."}, status=403)

        # Fetch the associated hospital
        hospital = Hospital.objects.filter(email=user.email).first()
        if not hospital:
            return Response({"error": "No hospital found for the logged-in user."}, status=403)

        # Debugging: Print the hospital associated
        print(f"Hospital for GET: {hospital.name}")

        # If `pk` is provided, retrieve the specific case
        if pk:
            case = Case.objects.filter(pk=pk, hospital=hospital).first()
            if not case:
                return Response({"error": "Case not found."}, status=404)
            serializer = CaseSerializer(case)
            return Response(serializer.data, status=200)

        # Otherwise, retrieve all cases for the hospital
        cases = Case.objects.filter(hospital=hospital)
        serializer = CaseSerializer(cases, many=True)

        # Debugging: Print the diseases in the cases
        for case in cases:
            print(f"Disease in Case: {case.disease}")

        return Response(serializer.data, status=200)

    def get_hospital(self, user):
        """
        Helper method to retrieve the associated hospital for the logged-in user.
        """
        if user.role == 'hospital':
            try:
                return Hospital.objects.get(email=user.email)
            except Hospital.DoesNotExist:
                return None
        return None

    def post(self, request):
        """
        Create a new case for the authenticated hospital.
        """
        user = request.user
 
        print(f"Logged-in User post: {user} ({user.role})")
        try:
            if user.role == 'hospital':
                hospital = Hospital.objects.filter(email=user.email).first()
            else:
                hospital = user.supervised_hospitals.first()

            print(f"Associated Hospital in POST: {hospital}")
            if not hospital:
                return Response({"error": "You are not associated with a hospital."}, status=403)
        except Exception as e:
            print(f"Error fetching hospital: {e}")
            return Response({"error": "Error fetching hospital association."}, status=500)

        data = request.data.copy()
        
        if not data.get('disease'):
            return Response({"error": "The disease field is required."}, status=400)

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
        Update a specific case for the authenticated hospital.
        """
        user = request.user
        print(f"Logged-in User PUT: {user} ({user.role})")
        print(f"PUT Data Received: {request.data}")

        hospital = self.get_hospital(user)
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

        print(f"Serializer Errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """
        Delete a specific case for the authenticated hospital.
        """
        user = request.user
        print(f"Logged-in User DELETE: {user} ({user.role})")
        hospital = self.get_hospital(user)
        if not hospital:
            return Response({"error": "No associated hospital found."}, status=403)

        try:
            case = Case.objects.get(pk=pk, hospital=hospital)
            case.delete()
            return Response({"message": "Case deleted successfully."}, status=204)
        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=404)
        except Exception as e:
            print(f"Error in DELETE: {e}")
            return Response({"error": str(e)}, status=500)
