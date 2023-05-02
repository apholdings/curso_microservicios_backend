from rest_framework_api.views import StandardAPIView
from rest_framework import permissions, status
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer

class ContactCreateView(StandardAPIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            contact = serializer.save()

            message_body = f"""
                            Name: {contact.name}
                            Email: {contact.email}
                            Phone: {contact.phone}
                            Budget: {contact.budget}

                            Message:
                            {contact.message}
                            """

            send_mail(
                contact.subject,
                message_body,
                'mail@solopython.com',
                ['mail@solopython.com'],
                fail_silently=False
            )

            return self.send_response('Message sent successfully')

        return self.send_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST)