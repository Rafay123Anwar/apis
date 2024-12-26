import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,serializers
from .models import User, Patient
from .serializers import UserSerializer, PatientSerializer

class SignupView(APIView):
    def post(self, request):
        try:
            user_data = {
                'email': request.data.get('email'),
                'password': request.data.get('password')
            }
            patient_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'contact_number': request.data.get('contact_number'),
                'address': request.data.get('address'),
                'gender': request.data.get('gender'),
                'date_of_birth': request.data.get('date_of_birth'),
                'medical_history': request.data.get('medical_history'),
                # 'image': request.FILES.get('image')  
            }
            image = request.data.get('image')
            if image:
                try:
                    # Ensure the image is Base64 encoded
                    decoded_image = base64.b64decode(image)
                    patient_data['image'] = image  # Store the Base64 string
                except Exception as e:
                    return Response({"error": "Invalid image format"}, status=status.HTTP_400_BAD_REQUEST)

            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()

                patient_serializer = PatientSerializer(data=patient_data)
                if patient_serializer.is_valid():
                    patient = patient_serializer.save()
                    return Response({
                        "message": "Signup successful!",
                        "patient": patient_serializer.data
                    }, status=status.HTTP_201_CREATED)
                else:
                    user.delete()
                    print("Patient serializer errors:", patient_serializer.errors)
                    return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("User serializer errors:", user_serializer.errors)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected error:", str(e))
            return Response({"error": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class SignupView(APIView):
#     def post(self, request):
#         # Extract the data from the request
#         user_data = {
#             'email': request.data.get('email'),
#             'password': request.data.get('password')
#         }
#         patient_data = {
#             'first_name': request.data.get('first_name'),
#             'last_name': request.data.get('last_name'),
#             'contact_number': request.data.get('contact_number'),
#             'address': request.data.get('address'),
#             'gender': request.data.get('gender'),
#             'date_of_birth': request.data.get('date_of_birth'),
#             'medical_history': request.data.get('medical_history'),
#             'image': request.data.get('image')
#         }

#         # Validate and create the User using the UserSerializer
#         user_serializer = UserSerializer(data=user_data)
#         if user_serializer.is_valid():
#             # Save the user
#             user = user_serializer.save()

#             # Add the created user to the patient data
#             patient_data['user'] = user

#             # Validate and create the Patient using the PatientSerializer
#             patient_serializer = PatientSerializer(data=patient_data)
#             if patient_serializer.is_valid():
#                 # Save the patient profile
#                 patient = patient_serializer.save()

#                 # Return success message and serialized patient data
#                 return Response({
#                     "message": "Signup successful!",
#                     "patient": patient_serializer.data
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 # Rollback: Delete user if patient creation fails
#                 user.delete()
#                 return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(f"Email: {email}, Password: {password}")

        try:
            user = User.objects.get(email=email)  # Find the user by email
            if user.check_password(password):  # Check if the password is correct
                # Find the associated Patient record by patient_id (linked to user_id)
                patient = Patient.objects.filter(patient_id=user.user_id).first()

                # Return the patient_id along with a success message
                return Response(
                    {
                        "message": "Login successful",
                        "patient_id": patient.patient_id if patient else None,  # Return patient_id if exists
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class ProfileView(APIView):
    def get(self, request, patient_id):
        print(f"Fetching profile for patient ID: {patient_id}")
        try:
            patient = Patient.objects.get(patient_id=patient_id)
            # print(f"Fetching profile for patient ID: {patient}")
            patient_serializer = PatientSerializer(patient)
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)



